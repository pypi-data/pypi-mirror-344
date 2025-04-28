# Standard Library
from abc import abstractmethod
from contextlib import AsyncExitStack
from dataclasses import field
import socket as std_socket
from socket import SOCK_RAW
import struct
from typing import AsyncIterator, Iterator, List, Optional

# Third-party
import anyio
import anyio.abc
import anyio.streams
import anyio.streams.memory
import anyio.to_thread
from anyio import move_on_after, create_memory_object_stream, create_task_group
from anyio.abc import SocketStream
from result import Result, Ok, Err
from toolz.curried import pipe, map, filter, reduceby, concat, groupby, reduce

# Internal
from oxitrait.trait import Trait
from oxitrait.impl import Impl
from oxitrait.struct import Struct
from oxitrait.enum import Enum, auto
from oxitrait.runtime import requires_traits

from ..log import logger
from .consts import (
    AF_NETLINK,
    NLMSG_ALIGN,
    NLMSG_DONE,
    NLMSG_HDR_FORMAT,
    NLMSG_HDR_SIZE,
)
from .rtnl.consts import (
    NDUSEROPT_MAX,
)
from .message import NetlinkHeaderTrait
from .parsing import parse_peek, parse_full_message

class NetlinkSyncContextTrait(metaclass=Trait):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

class NetlinkAsyncContextTrait(metaclass=Trait):
    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

class NetlinkSocketTrait(metaclass=Trait):
    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    async def send_message(self, message: NetlinkHeaderTrait) -> Result[None, str]:
        """
        Serialize and send a netlink message.
        """
        pass

    @abstractmethod
    async def receive_message(self, timeout: float = 5.0) -> Result[NetlinkHeaderTrait, str]:
        """
        Retrieve one netlink message from the buffer (populated by a background task).
        """
        pass

    @abstractmethod
    async def close(self) -> Result[None, str]:
        """
        Cancel any background tasks and close the underlying socket.
        """
        pass

#
# 2) Provide the Implementation for that Trait
#
class ImplNetlinkSocket(NetlinkSocketTrait, metaclass=Impl, target="NetlinkSocket"):
    """
    Implementation for the NetlinkSocket struct.
    """

    def __post_init__(self):
        self._group_mask = sum(1 << (g - 1) for g in self.groups)
        self.sock: Optional[std_socket.socket] = None
        self._message_buffer: dict[int, list[bytes]] = {}
    
        send_chan, recv_chan = create_memory_object_stream(100)
        self.inbound_send = send_chan
        self.inbound_recv = recv_chan

    @staticmethod
    def _concat(fragments: list[bytes]) -> bytes:
        return b"".join(fragments)

    @staticmethod
    def _log_and_discard(reason: str):
        logger.warning(f"_dispatch() skipped: {reason}")

    @staticmethod
    def _is_valid_frame(f: bytes) -> bool:
        return len(f) >= NLMSG_HDR_SIZE

    async def _dispatch(self, fragments: list[bytes]):
        logger.debug(f"_dispatch called with {len(fragments)} fragment(s)")

        def log_and_parse(raw: bytes):
            logger.debug(f"Raw message length: {len(raw)} bytes")
            logger.debug(f"Raw bytes (first 32): {raw[:32].hex()}")
            result = parse_full_message(raw)
            logger.debug("Called parse_full_message()")
            if result.is_ok():
                logger.debug("parse_full_message returned Ok")
            else:
                logger.error(f"parse_full_message returned Err: {result.unwrap_err()}")
            return result

        async def send_if_ok(result):
            if result.is_ok():
                logger.debug("Sending message to inbound channel")
                await self.inbound_send.send(result.unwrap())
            else:
                logger.error(f"Not sending, result was Err: {result.unwrap_err()}")

        return await pipe(
            fragments,
            b"".join,         # → bytes
            log_and_parse,    # → Result[dict, str]
            send_if_ok        # → awaitable effect
        )

    async def send_message(self, message: NetlinkHeaderTrait) -> Result[None, str]:
        """
        Send a serialized NetlinkMessage using a blocking system socket.
        """
        try:
            # Convert the message to bytes, if needed
            data = bytes(message)  # assuming message implements __bytes__()

            await anyio.to_thread.run_sync(self.sock.send, data)
            return Ok(None)
        except Exception as e:
            return Err(f"Send error: {e}")

    async def receive_message(self, timeout: float = 1.0) -> Result[dict, str]:
        """
        Retrieve one Netlink message from the inbound queue, subject to timeout.
        """
        if not self.inbound_recv:
            logger.error("inbound_recv channel is missing.")
            return Err("inbound_recv channel is missing.")

        logger.debug("Entering receive_message(), waiting for a message...")

        with move_on_after(timeout) as cancel_scope:
            try:
                msg = await self.inbound_recv.receive()

                if cancel_scope.cancelled_caught:
                    logger.warning("receive_message() timed out waiting for a message")
                    return Err("Timeout occurred waiting for Netlink message.")

                logger.debug("Message received in receive_message()")
                return Ok(msg)

            except Exception as e:
                logger.exception("Exception while receiving from inbound channel")
                return Err(e)

    async def listen(self) -> AsyncIterator[tuple[dict, bytes]]:
        """
        Yield unsolicited Netlink messages (header, payload) as they arrive.

        Assumes multicast groups were already set via the `groups` field
        and bound during __aenter__().
        """
        while self._running:
            try:
                msg = await self.inbound_recv.receive()
                if isinstance(msg, dict) and "header" in msg and "payload" in msg:
                    yield msg["header"], msg["payload"]
                else:
                    logger.warning("listen(): malformed msg")
            except anyio.get_cancelled_exc_class():
                logger.debug("listen(): cancelled")
                break
            except Exception as e:
                logger.warning(f"listen() error: {e}")

    async def close(self) -> Result[None, str]:
        """
        Stop the background loop, close the socket, and clean up channels.
        """
        self._running = False
        if self.sock:
            try:
                await self.sock.close()
            except Exception as e:
                return Err(f"Close error: {e}")
            finally:
                self.sock = None

        # If you want to also terminate the read loop more definitively:
        if self.tg:
            self.tg.cancel_scope.cancel()

        # Close the memory channel
        if self.inbound_send:
            await self.inbound_send.close()

        return Ok(None)

    async def _rx_chunks(self, sock):
        while True:
            try:
                logger.trace("Entering _rx_chunks")
                while sock is None:
                    logger.trace("Waiting for socket to be available")
                    await anyio.sleep(0.01)
                    sock = self.sock
                data = await anyio.to_thread.run_sync(sock.recv, 65536)
                logger.trace(f"Got {len(data)} bytes from kernel")
                yield data
            except OSError as e:
                if self._running:
                    logger.warning(f"Netlink recv OSError: {e}")
                break
            except anyio.get_cancelled_exc_class():
                break

    # 2) pure helpers
    @staticmethod
    def _is_valid_header(data: bytes, offset: int) -> bool:
        return len(data) - offset >= NLMSG_HDR_SIZE

    @staticmethod
    def _unpack_len(data: bytes, offset: int) -> int:
        return struct.unpack_from(NLMSG_HDR_FORMAT, data, offset)[0]

    @staticmethod
    def _can_fit_frame(data: bytes, offset: int, aligned_len: int) -> bool:
        return offset + aligned_len <= len(data)

    @staticmethod
    def split_frames(buf: bytes) -> Iterator[bytes]:
        """
        Yield Netlink-aligned message frames from a raw buffer.

        Ensures:
        - Header exists (min 16 bytes)
        - msg_len is >= header size
        - msg_len doesn't run past buffer end
        """
        def _next_offset(offset: int, msg_len: int) -> int:
            return NLMSG_ALIGN(offset + msg_len)

        offset = 0
        buflen = len(buf)

        while offset + NLMSG_HDR_SIZE <= buflen:
            try:
                (msg_len,) = struct.unpack_from("=I", buf, offset)
            except struct.error:
                logger.error(f"struct.unpack_from failed at offset={offset}")
                break

            if msg_len < NLMSG_HDR_SIZE:
                logger.error(f"Invalid Netlink length: {msg_len} < header size ({NLMSG_HDR_SIZE})")
                break

            end = offset + msg_len
            if end > buflen:
                logger.error(f"Truncated Netlink message: {end} > buffer length {buflen}")
                break

            yield buf[offset:end]
            offset = _next_offset(offset, msg_len)

    @staticmethod
    def parse_header(frame: bytes) -> Result[tuple[dict, bytes], str]:
        try:
            ln, ty, fl, seq, pid = struct.unpack_from(NLMSG_HDR_FORMAT, frame)
            hdr = {"len": ln, "type": ty, "flags": fl, "seq": seq, "pid": pid}
            return Ok((hdr, frame))             #  ← keep full bytes here
        except Exception as e:
            return Err(str(e))

    @staticmethod
    def _is_valid_chunk(raw: bytes) -> bool:
        return len(raw) >= NLMSG_HDR_SIZE

    async def _read_loop(self):
        logger.trace("Starting Netlink read loop")

        async for chunk in self._rx_chunks(self.sock):
            logger.debug(f"📥 Received {len(chunk)} bytes from socket")

            try:
                frames = pipe(
                    chunk,
                    self.split_frames,
                    filter(self._is_valid_chunk),
                    map(self.parse_header),
                    filter(self._is_ok),
                    map(self._unwrap),
                )
            except Exception as e:
                logger.exception("Exception during frame processing")
                continue

            frame_list = list(frames)  # materialize for logging & reuse
            logger.debug(f"Extracted {len(frame_list)} valid frame(s) from chunk")

            try:
                by_seq = pipe(
                    frame_list,
                    groupby(self._by_seq_key),
                )
            except Exception as e:
                logger.exception("Exception during sequence grouping")
                continue

            logger.debug(f"Grouped into {len(by_seq)} sequence(s): {list(by_seq.keys())}")

            for seq, group in by_seq.items():
                logger.debug(f"Processing seq {seq} with {len(group)} message(s)")

                if seq not in self._message_buffer:
                    logger.debug(f"Creating new buffer for seq {seq}")
                    self._message_buffer[seq] = []

                seen_done = False

                for hdr, full_frame in group:
                    logger.debug(f"Msg type={hdr['type']} len={hdr['len']} pid={hdr['pid']}")
                    self._message_buffer[seq].append(full_frame)

                    if hdr["type"] == NLMSG_DONE:
                        seen_done = True
                        logger.debug(f"Detected NLMSG_DONE in seq {seq}")

                if seen_done:
                    fragments = self._message_buffer.pop(seq)
                    logger.debug(f"Dispatching {len(fragments)} buffered frame(s) for seq {seq}")
                    try:
                        await self._dispatch(fragments)
                    except Exception as e:
                        logger.exception(f"Exception during dispatch of seq {seq}")

            logger.trace("Waiting for next Netlink message...")

    @staticmethod
    def _is_ok(result):
        return result.is_ok()

    @staticmethod
    def _unwrap(result):
        return result.unwrap()

    @staticmethod
    def _by_seq_key(tpl):
        header, _ = tpl
        return header["seq"]

class ImplNetlinkSyncContext(NetlinkSyncContextTrait, metaclass=Impl, target="NetlinkSocket"):
    def __enter__(self):
        proto: int = self.protocol
        assert isinstance(proto, int)
        assert isinstance(AF_NETLINK, int)
        self.sock = std_socket.socket(AF_NETLINK, SOCK_RAW, proto)
        return self  # Allow `with NetlinkSocket() as pyr:`

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock:
            self.sock.close()

class ImplNetlinkAsyncContext(NetlinkAsyncContextTrait, metaclass=Impl, target="NetlinkSocket"):
    async def __aenter__(self):
        # Structured async context manager stack
        self._exit_stack = AsyncExitStack()
        await self._exit_stack.__aenter__()

        # Create and bind the raw Netlink socket
        group_mask = getattr(self, "_group_mask", 0)
        proto: int = self.protocol
        assert isinstance(proto, int)
        assert isinstance(AF_NETLINK, int)
        self.sock = std_socket.socket(AF_NETLINK, SOCK_RAW, proto)
        self.sock.bind((0, group_mask))
        self._running = True

        # Launch background read loop under managed task group
        self.tg = await self._exit_stack.enter_async_context(create_task_group())
        self.tg.start_soon(self._read_loop)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._running = False

        # Safely close the socket, if open
        if self.sock:
            self.sock.close()
            self.sock = None

        # Exit all context managers in LIFO order
        return await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

class NetlinkSocket(metaclass=Struct):
    """
    A concrete struct (dataclass) that includes:
      - protocol: the netlink protocol to use (e.g., NETLINK_ROUTE)
      - sock: the actual Trio socket object
      - a background task group
      - channels for buffering inbound messages
      - a running flag
    """

    protocol: int
    groups: List[int] = field(default_factory=list)
    sock: Optional[std_socket.socket] = None
    tg: Optional[anyio.abc.TaskGroup] = None
    _running: bool = False
    _message_buffer: Optional[dict[int, list[bytes]]] = None

    inbound_send: Optional[anyio.streams.memory.MemoryObjectSendStream[NetlinkHeaderTrait]] = None
    inbound_recv: Optional[anyio.streams.memory.MemoryObjectReceiveStream[NetlinkHeaderTrait]] = None

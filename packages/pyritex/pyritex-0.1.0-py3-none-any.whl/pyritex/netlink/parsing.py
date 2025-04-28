from result import Ok, Err, Result
from toolz.curried import pipe

from ..log import logger
from .consts import *

def _unpack_header(raw: bytes) -> Result[tuple[int, int, int, int, int], str]:
    if len(raw) < NLMSG_HDR_SIZE:
        return Err("Message too short for Netlink header")
    try:
        return Ok(struct.unpack_from(NLMSG_HDR_FORMAT, raw))
    except Exception as e:
        return Err(f"Unpack failed: {e}")


def _validate_len(nlmsg_len: int, buf_len: int) -> Result[int, str]:
    if nlmsg_len < NLMSG_HDR_SIZE:
        return Err(f"Invalid Netlink length: {nlmsg_len} < header size")
    if nlmsg_len > buf_len:
        return Err(f"Netlink length {nlmsg_len} exceeds buffer length {buf_len}")
    return Ok(nlmsg_len)


def _build_dict(parsed: tuple[int, int, int, int, int], raw: bytes) -> dict:
    ln, ty, fl, seq, pid = parsed
    return {
        "len": ln,
        "type": ty,
        "flags": fl,
        "seq": seq,
        "pid": pid,
        "payload": raw[NLMSG_HDR_SIZE:ln],
    }


def parse_full_message(raw: bytes) -> Result[dict, str]:
    return pipe(
        raw,
        _unpack_header,                                       # → Result[(ln, ty, fl, seq, pid)]
        lambda r: r.and_then(lambda hdr:                      # Validate length
            _validate_len(hdr[0], len(raw)).map(lambda _: hdr)
        ),
        lambda r: r.map(lambda hdr: _build_dict(hdr, raw))    # Build parsed dict
    )

def parse_peek(data: bytes, offset: int) -> Result[tuple[int, dict], str]:
    """
    Read netlink header from data[offset:], returning:
      Ok((nlmsg_len, info_dict))
    or Err(...) if invalid.
    """
    return pipe(
        data[offset:],
        _step_check_min_length(offset),
        _step_unpack_header(offset),
        _step_validate_bounds(data, offset),
        _step_build_info(data, offset)
    )

def _step_check_min_length(offset: int):
    def inner(buf: bytes) -> Result[bytes, str]:
        if len(buf) < NLMSG_HDR_SIZE:
            return Err(f"Truncated at offset={offset}: only {len(buf)} bytes")
        return Ok(buf)
    return inner

def _step_unpack_header(offset: int):
    def inner(buf: bytes) -> Result[tuple[int, int, int, int, int], str]:
        try:
            header = struct.unpack_from(NLMSG_HDR_FORMAT, buf)
            return Ok(header)
        except Exception as e:
            logger.error(f"Unpack failed at offset {offset}: {e}")
            return Err(f"Unpack failed at offset {offset}: {e}")
    return inner

def _step_validate_bounds(data: bytes, offset: int):
    def inner(tup: tuple[int, int, int, int, int]) -> Result[tuple[int, int, int, int, int], str]:
        nlmsg_len = tup[0]
        if nlmsg_len < NLMSG_HDR_SIZE:
            return Err(f"Invalid nlmsg_len={nlmsg_len} < NLMSG_HDR_SIZE")
        if offset + nlmsg_len > len(data):
            return Err(f"Message length {nlmsg_len} extends beyond buffer size at offset={offset}")
        return Ok(tup)
    return inner

def _step_build_info(data: bytes, offset: int):
    def inner(tup: tuple[int, int, int, int, int]) -> Result[tuple[int, dict], str]:
        ln, ty, fl, seq, pid = tup
        info = {
            "len": ln,
            "type": ty,
            "flags": fl,
            "seq": seq,
            "pid": pid,
            "payload": data[offset + NLMSG_HDR_SIZE : offset + ln]
        }
        return Ok((ln, info))
    return inner

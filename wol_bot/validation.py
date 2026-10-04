"""Validation and normalisation of user input."""

from __future__ import annotations

import ipaddress
import re

_MAC_FORMATS = (
    re.compile(r"[0-9a-f]{2}(?::[0-9a-f]{2}){5}"),  # aa:bb:cc:dd:ee:ff
    re.compile(r"[0-9a-f]{2}(?:-[0-9a-f]{2}){5}"),  # aa-bb-cc-dd-ee-ff
    re.compile(r"[0-9a-f]{4}(?:\.[0-9a-f]{4}){2}"),  # aabb.ccdd.eeff
    re.compile(r"[0-9a-f]{12}"),  # aabbccddeeff
)
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,31}")
RESERVED_NAMES = frozenset({"all"})


def normalize_mac(value: str) -> str:
    """Return the MAC address as lowercase, colon-separated hex."""
    mac = value.strip().lower()
    if not any(fmt.fullmatch(mac) for fmt in _MAC_FORMATS):
        raise ValueError(f"Invalid MAC address: {value}")
    digits = re.sub(r"[^0-9a-f]", "", mac)
    return ":".join(digits[i : i + 2] for i in range(0, 12, 2))


def normalize_ip(value: str) -> str:
    """Return the canonical form of an IPv4 or IPv6 address."""
    try:
        return str(ipaddress.ip_address(value.strip()))
    except ValueError as err:
        raise ValueError(f"Invalid IP address: {value}") from err


def validate_name(value: str) -> str:
    """Device names are used as command arguments: no spaces, 32 characters max."""
    name = value.strip()
    if not _NAME.fullmatch(name):
        raise ValueError(
            f"Invalid name: {value}. Use up to 32 letters, digits, '.', '_' or '-', starting with a letter or digit."
        )
    if name.lower() in RESERVED_NAMES:
        raise ValueError(f"'{name}' is reserved")
    return name

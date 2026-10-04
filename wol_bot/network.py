"""Wake-on-LAN and reachability checks."""

from __future__ import annotations

import asyncio
import logging

import wakeonlan

log = logging.getLogger(__name__)


def wake(mac: str, broadcast_address: str, port: int) -> None:
    wakeonlan.wake(mac, host=broadcast_address, port=port)


async def _run(*args: str, timeout: float) -> tuple[int, str]:
    try:
        process = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL
        )
    except FileNotFoundError:
        log.error("%s is not installed", args[0])
        return -1, ""
    try:
        stdout, _ = await asyncio.wait_for(process.communicate(), timeout)
    except TimeoutError:
        process.kill()
        await process.wait()
        return -1, ""
    return process.returncode or 0, stdout.decode(errors="replace")


async def is_up(ip: str) -> bool:
    """Return True when the host answers a ping or ARP / NDP on the local network.

    Hosts that drop ICMP (for example Windows with its default firewall) still
    answer neighbour discovery, which the ping triggers.
    """
    code, _ = await _run("ping", "-c", "1", "-W", "1", "-n", ip, timeout=3)
    if code == 0:
        return True
    code, output = await _run("ip", "neigh", "show", ip, timeout=2)
    return code == 0 and "REACHABLE" in output.split()

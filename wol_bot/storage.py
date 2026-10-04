"""SQLite storage for registered devices.

The table layout matches the database of the former web backend, so an existing
``devices.db`` can be reused as is.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from dataclasses import dataclass
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS devices (
    hostname VARCHAR NOT NULL,
    mac VARCHAR NOT NULL PRIMARY KEY,
    ip VARCHAR NOT NULL UNIQUE
)
"""


@dataclass(frozen=True)
class Device:
    name: str
    mac: str
    ip: str


class DeviceExistsError(Exception):
    """A device with the same name, MAC or IP address is already registered."""


class DeviceStore:
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._transaction() as conn:
            conn.execute(_SCHEMA)

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with closing(sqlite3.connect(self._path)) as conn, conn:
            yield conn

    @staticmethod
    def _to_device(row: tuple[str, str, str]) -> Device:
        name, mac, ip = row
        return Device(name=name, mac=mac.lower(), ip=ip)

    def list(self) -> list[Device]:
        with self._transaction() as conn:
            rows = conn.execute("SELECT hostname, mac, ip FROM devices ORDER BY lower(hostname)").fetchall()
        return [self._to_device(row) for row in rows]

    def get(self, name: str) -> Device | None:
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT hostname, mac, ip FROM devices WHERE lower(hostname) = lower(?)", (name,)
            ).fetchone()
        return self._to_device(row) if row else None

    def add(self, device: Device) -> None:
        with self._transaction() as conn:
            checks = (
                ("name", "lower(hostname) = lower(?)", device.name),
                ("MAC address", "lower(mac) = lower(?)", device.mac),
                ("IP address", "ip = ?", device.ip),
            )
            for label, condition, value in checks:
                existing = conn.execute(f"SELECT hostname FROM devices WHERE {condition}", (value,)).fetchone()
                if existing:
                    raise DeviceExistsError(f"{existing[0]} already uses this {label}")
            conn.execute(
                "INSERT INTO devices (hostname, mac, ip) VALUES (?, ?, ?)",
                (device.name, device.mac, device.ip),
            )

    def delete(self, name: str) -> bool:
        with self._transaction() as conn:
            cursor = conn.execute("DELETE FROM devices WHERE lower(hostname) = lower(?)", (name,))
        return cursor.rowcount > 0

"""Runtime settings, read from environment variables."""

from __future__ import annotations

import ipaddress
import os
from collections.abc import Mapping
from dataclasses import dataclass


class ConfigError(Exception):
    """A required setting is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    bot_token: str
    allowed_user_ids: frozenset[int]
    database_path: str = "devices.db"
    broadcast_address: str = "255.255.255.255"
    wol_port: int = 9

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        env = os.environ if env is None else env

        token = env.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            raise ConfigError("TELEGRAM_BOT_TOKEN is required")

        raw_ids = env.get("ALLOWED_USER_IDS", "")
        try:
            user_ids = frozenset(int(item) for item in raw_ids.replace(" ", "").split(",") if item)
        except ValueError as err:
            raise ConfigError("ALLOWED_USER_IDS must be a comma-separated list of Telegram user IDs") from err

        broadcast = env.get("WOL_BROADCAST_ADDRESS", cls.broadcast_address).strip()
        try:
            ipaddress.ip_address(broadcast)
        except ValueError as err:
            raise ConfigError(f"WOL_BROADCAST_ADDRESS is not an IP address: {broadcast}") from err

        try:
            port = int(env.get("WOL_PORT", cls.wol_port))
        except ValueError as err:
            raise ConfigError("WOL_PORT must be an integer") from err
        if not 1 <= port <= 65535:
            raise ConfigError("WOL_PORT must be between 1 and 65535")

        return cls(
            bot_token=token,
            allowed_user_ids=user_ids,
            database_path=env.get("DATABASE_PATH", cls.database_path),
            broadcast_address=broadcast,
            wol_port=port,
        )

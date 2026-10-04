"""Entry point: python -m wol_bot"""

from __future__ import annotations

import logging
import os
import sys

from .bot import build_application
from .config import ConfigError, Settings
from .storage import DeviceStore


def main() -> int:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    )
    # httpx logs every request URL at INFO level, and those URLs contain the bot token.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    log = logging.getLogger("wol_bot")

    try:
        settings = Settings.from_env()
    except ConfigError as err:
        log.error("%s", err)
        return 1
    if not settings.allowed_user_ids:
        log.warning("ALLOWED_USER_IDS is empty: every request will be rejected")

    store = DeviceStore(settings.database_path)
    build_application(settings, store).run_polling(drop_pending_updates=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

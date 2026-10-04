import pytest

from wol_bot.config import ConfigError, Settings


def test_defaults():
    settings = Settings.from_env({"TELEGRAM_BOT_TOKEN": "123:abc", "ALLOWED_USER_IDS": "1, 22,333"})
    assert settings.bot_token == "123:abc"
    assert settings.allowed_user_ids == {1, 22, 333}
    assert settings.database_path == "/data/devices.db"
    assert settings.broadcast_address == "255.255.255.255"
    assert settings.wol_port == 9


def test_overrides():
    settings = Settings.from_env(
        {
            "TELEGRAM_BOT_TOKEN": "123:abc",
            "ALLOWED_USER_IDS": "",
            "DATABASE_PATH": "/tmp/x.db",
            "WOL_BROADCAST_ADDRESS": "192.168.1.255",
            "WOL_PORT": "7",
        }
    )
    assert settings.allowed_user_ids == frozenset()
    assert settings.database_path == "/tmp/x.db"
    assert settings.broadcast_address == "192.168.1.255"
    assert settings.wol_port == 7


@pytest.mark.parametrize(
    "env",
    [
        {},
        {"TELEGRAM_BOT_TOKEN": "  "},
        {"TELEGRAM_BOT_TOKEN": "t", "ALLOWED_USER_IDS": "me"},
        {"TELEGRAM_BOT_TOKEN": "t", "WOL_BROADCAST_ADDRESS": "lan"},
        {"TELEGRAM_BOT_TOKEN": "t", "WOL_PORT": "nine"},
        {"TELEGRAM_BOT_TOKEN": "t", "WOL_PORT": "70000"},
    ],
)
def test_invalid_settings(env):
    with pytest.raises(ConfigError):
        Settings.from_env(env)

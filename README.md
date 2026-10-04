# WOL Manager

Telegram bot to wake devices on your local network with Wake-on-LAN and check
whether they are up.

## Commands

| Command | Description |
|---|---|
| `/wake NAME` | Send a magic packet to a device. `/wake all` wakes every device. |
| `/status NAME` | Check whether a device is up. `/status all` checks every device. |
| `/devices` | List registered devices. |
| `/add NAME MAC IP` | Register a device, e.g. `/add desktop a1:b2:c3:d4:e5:f6 192.168.1.20`. |
| `/delete NAME` | Remove a device, after confirmation. |
| `/help` | Show the list of commands. |

Without a name, `/wake`, `/status` and `/delete` show a button for each device.
`/start NAME` is kept as an alias of `/wake NAME`.

Only the Telegram users listed in `ALLOWED_USER_IDS` can use the bot. Anyone else
gets a refusal with their user ID, which makes it easy to authorize a new user.

## Setup

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy its token.
2. Copy `.env.example` to `.env`, then set `TELEGRAM_BOT_TOKEN`.
3. Start the bot, send it any message and add the user ID it replies with to
   `ALLOWED_USER_IDS`. Restart the bot.

```bash
cp .env.example .env
docker compose up -d
```

The bot must run on a host of the network where the devices live: it uses host
networking to broadcast magic packets and to check the neighbour table.

`ping` has the `CAP_NET_RAW` file capability, because host networking uses the
`net.ipv4.ping_group_range` of the host, which often excludes unprivileged
users. On Kubernetes, keep `NET_RAW` in the container capabilities and
`allowPrivilegeEscalation: true`, otherwise file capabilities are ignored and
the status falls back to the neighbour table only.

### Settings

| Variable | Default | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | *(required)* | Token given by @BotFather. |
| `ALLOWED_USER_IDS` | *(empty)* | Comma-separated Telegram user IDs allowed to use the bot. |
| `WOL_BROADCAST_ADDRESS` | `255.255.255.255` | Destination of magic packets, e.g. the broadcast address of another subnet. |
| `WOL_PORT` | `9` | UDP port of magic packets. |
| `DATABASE_PATH` | `/data/devices.db` | SQLite database of registered devices. |
| `LOG_LEVEL` | `INFO` | Python log level. |

The database keeps the layout of previous versions. To keep your devices, copy
your former `backend/core/devices.db` into the `wol-data` volume:

```bash
docker compose cp backend/core/devices.db bot:/data/devices.db
docker compose restart bot
```

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
ruff check . && ruff format --check .
pytest
```

Run the bot locally with `python -m wol_bot`, with the variables above exported.

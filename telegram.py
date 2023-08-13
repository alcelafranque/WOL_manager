import json
import yaml
import requests

import ping_error
from status_checker import status_checker

from telethon import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)
import asyncio
from telethon.tl.types import (PeerChannel)
from telethon.errors import SessionPasswordNeededError

OFFSET_ID = 0
LIMIT = 100
MESSAGES = []
NB_MESSAGES = 0
TCL = 0
def get_config():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
    return config

def get_last_message():
    api_url = "https://api.telegram.org/bot5886610488:AAG711fMlHlbCByixJo0SUMe2MXgHuX-7Fk/getUpdates"
    messages = requests.get(api_url, timeout=10).text
    messages = json.loads(messages)
    return messages["result"][-1]

def run():
    if not status_checker():
        raise ping_error.PingError("Host unreachable")

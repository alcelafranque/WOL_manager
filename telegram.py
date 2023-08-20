import json
import yaml
import requests
import re

import errors
from wake_me_up import *

from status_checker import *

def get_config():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
    return config

def get_last_message(bot_id):
    api_url = "https://api.telegram.org/bot{}/getUpdates".format(bot_id)
    messages = requests.get(api_url, timeout=10).text
    messages = json.loads(messages)
    return messages["result"][-1]

def send_bot_message(bot_id, id, text):
    url_sending_message = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_id, id, text)
    print(url_sending_message)
    requests.get(url_sending_message)

def is_a_new_message(latest_message):
    with open("saving_last_timestamps", "r") as former_timestamp:
        timestamp1 = next(former_timestamp)
    print(timestamp1)
    print(str(latest_message["message"]["date"]))
    return True if timestamp1 != str(latest_message["message"]["date"]) else False


def is_a_valid_add_message(message_text):
    splited_message = message_text.split(" ")
    print(splited_message[3])
    return True if re.match(r"([0123456789a-fA-F]{2}:){5}[0123456789a-fA-F]{2}", splited_message[3]) else False




def telegram_run():
    config = get_config()
    ip = config["ip"]
    mac = config["mac"]
    id = config["id"]
    bot_id = config["bot_id"]
    last_message = get_last_message(bot_id)
    print(last_message)
    print(last_message["message"]["text"])

    if last_message['message']["text"] == "/start @wolol_bot" and is_a_new_message(last_message):

        wake_me_up(mac)
        refresh_arp_table(ip)
        ip = get_new_ip(mac)
        timestamps = str(last_message["message"]["date"])
        if not get_status(ip):
            started = status_checker(ip)

            if not started:
                text = "not started in due time"
                send_bot_message(bot_id, id, text)
            else:
                text = "done"
                send_bot_message(bot_id, id, text)
                with open("saving_last_timestamps", "w") as timestamp_file:
                    timestamp_file.write(timestamps)

        else:
            text = "already up"
            send_bot_message(bot_id, id, text)
            with open("saving_last_timestamps", "w") as timestamp_file:
                timestamp_file.write(timestamps)
    elif re.match(r"/add @wolol_bot [^\s]+ [^\s]+", last_message['message']['text']):
        if is_a_valid_add_message(last_message['message']['text']):


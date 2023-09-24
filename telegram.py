import json
import yaml
import requests
import re

import errors
from wake_me_up import *

from status_checker import *

from errors import *

last_instruction = None


def get_config():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
    return config


def get_last_message(bot_id):
    api_url = f"https://api.telegram.org/bot{bot_id}/getUpdates"
    messages = requests.get(api_url, timeout=10).text
    messages = json.loads(messages)
    if messages["result"]:
        return messages["result"][-1]
    else:
        raise(NoResultFound)


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
    print(splited_message[2])
    return True if re.match(r"([0123456789a-fA-F]{2}:){5}[0123456789a-fA-F]{2}", splited_message[2]) else False


def store_new_name_mac_pair(message, filename):
    splitted_message = message.split(" ")
    if not os.path.isfile(filename):
        with open(filename, "w"):
            pass
        name_to_mac = {}
    else:
        with open(filename, "r") as file1:
            try:
                name_to_mac = json.loads(file1.read())
            except json.decoder.JSONDecodeError:
                name_to_mac = {}
    name_to_mac[splitted_message[1]] = splitted_message[2]
    print(name_to_mac)
    with open(filename, 'w') as file1:
        file1.write(json.dumps(name_to_mac))


def get_devices(filename):
    with open(filename) as file1:
        all_pairs = json.loads(file1.read())
    return [k for k in all_pairs.keys()]


def get_mac_from_name(name, filename):
    with open(filename, "r") as file1:
        name_to_mac = json.loads(file1.read())
    try:
        return name_to_mac[name]
    except:
        return None


def delete_mac_from_name(name, filename):
    with open(filename, "r") as file1:
        name_to_mac = json.loads(file1.read())
    if name in name_to_mac.keys():
        del name_to_mac[name]
    with open(filename, "w") as file1:
        file1.write(json.dumps(name_to_mac))

def store_timestamps(last_message):
    timestamps = str(last_message["message"]["date"])
    with open("saving_last_timestamps", "w") as timestamp_file:
        timestamp_file.write(timestamps)

def telegram_run():
    global last_instruction
    config = get_config()
    ip = config["ip"]
    id = config["id"]
    bot_id = config["bot_id"]
    name_to_mac_file = config["name_to_mac_file"]
    last_message = get_last_message(bot_id)
    print(last_message)
    print(last_message["message"]["text"])

    if re.match(r"/start.*", last_message["message"]["text"]) and is_a_new_message(last_message):
        message_text = last_message["message"]["text"].split(" ")
        starting_time = message_text[-1] if message_text[-1].isdigit() else 30
        device_name = message_text[1]
        mac = get_mac_from_name(device_name, name_to_mac_file)
        if not mac:
            send_bot_message(bot_id, id, "ERROR: device_name_not_in_database send /devices to print known devices")
        refresh_arp_table(ip)
        wake_me_up(mac)
        if not get_status(ip):
            started = status_checker(mac, starting_time)

            if not started:
                text = "not started in due time"
                send_bot_message(bot_id, id, text)
            else:
                text = "done"
                send_bot_message(bot_id, id, text)
                store_timestamps(last_message)
        else:
            text = "already up"
            send_bot_message(bot_id, id, text)
            store_timestamps(last_message)

    elif re.match(r"/add [^\s]+ [^\s]+", last_message['message']['text']) and is_a_new_message(last_message):
        if is_a_valid_add_message(last_message['message']['text']):
            store_new_name_mac_pair(last_message["message"]["text"], name_to_mac_file)
            send_bot_message(bot_id,id, "Successfully Added")
        else:
            text = "ERROR: bad_message_format example: /add router_test a1:b6:23:dc:ff:99"
            send_bot_message(bot_id, id, text)

    elif re.match(r"/devices", last_message["message"]["text"]) and is_a_new_message(last_message):
        send_bot_message(bot_id, id, get_devices(name_to_mac_file))
        store_timestamps(last_message)

    elif re.match(r"/delete [^\s]+", last_message['message']['text']):
        delete_mac_from_name(last_message['message']['text'].split(" ")[1], name_to_mac_file)
        store_timestamps(last_message)

    elif re.match(r"/help", last_message["message"]["text"]) and is_a_new_message(last_message):
        text = "/add DEVICE_NAME DEVICE_MAC\n\n/delete DEVICE_NAME\n\n/devices\n\n/start DEVICE_NAME STARTING_TIME"
        send_bot_message(bot_id, id, text)
        store_timestamps(last_message)
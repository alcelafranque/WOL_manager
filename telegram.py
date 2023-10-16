import json
import yaml
import requests
import re

import errors
from wake_me_up import *

from status_checker import *

from errors import *


def get_config():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
    return config


def get_last_message(bot_id, nb_try):
    api_url = f"https://api.telegram.org/bot{bot_id}/getUpdates?offset=1"
    try:
        messages = requests.get(api_url, timeout=3).text
    except :
        messages = retry_get_last_message(bot_id, nb_try)
    messages = json.loads(messages)
    if messages["result"]:
        return messages["result"][-1]
    else:
        get_last_message(bot_id, nb_try)

def retry_get_last_message(bot_id, nb_try):
    api_url = f"https://api.telegram.org/bot{bot_id}/getUpdates?offset=1"
    try:
        messages = requests.get(api_url, timeout=3).text
    except:
        messages = retry_get_last_message(bot_id, nb_try)
    return messages

def send_bot_message(bot_id, id, text):
    url_sending_message = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_id, id, text)
    print(url_sending_message)
    try:
        requests.get(url_sending_message, timeout=2)
    except requests.exceptions.ReadTimeout:
        send_bot_message(bot_id, id, text)

def is_a_new_message(latest_message):
    try:
        with open("saving_last_timestamps", "r") as former_timestamp:
            timestamp1 = next(former_timestamp)
    except FileNotFoundError:
        return True
    return True if timestamp1 != str(latest_message["message"]["date"]) else False


def is_a_valid_add_message(message_text):
    splited_message = message_text.split(" ")
    print(splited_message[2])
    return True if re.match(r"([0123456789a-fA-F]{2}:){5}[0123456789a-fA-F]{2}", splited_message[2]) else False


def store_new_pair(message, filename):
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
    name_to_mac[splitted_message[1]] = {"mac": splitted_message[2], "interface": splitted_message[3]}
    with open(filename, 'w') as file1:
        file1.write(json.dumps(name_to_mac))


def get_devices(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file1:
            file1.write("{}")
    with open(filename) as file1:
        all_pairs = json.loads(file1.read())
    return [k for k in all_pairs.keys()]


def get_data_from_name(name, filename):
    """
    Get mac or interface from name.
    :param name: str
    :param filename: str
    :param data: str (mac | interface)
    :return: str
    """
    if not os.path.exists(filename):
        return None, None
    with open(filename, "r") as file1:
        name_to_mac = json.loads(file1.read())
    try:
        return name_to_mac[name]["mac"], name_to_mac[name]["interface"]
    except:
        return None, None


def delete_mac_from_name(name, filename):
    with open(filename, "r") as file1:
        name_to_mac = json.loads(file1.read())
    if name in name_to_mac.keys():
        del name_to_mac[name]
        with open(filename, "w") as file1:
            file1.write(json.dumps(name_to_mac))
        return True
    return False

def store_timestamps(last_message):
    timestamps = str(last_message["message"]["date"])
    with open("saving_last_timestamps", "w") as timestamp_file:
        timestamp_file.write(timestamps)

def telegram_run():
    try:
        nb_try = 0
        config = get_config()
        id = config["id"]
        ssh_file = config["path_to_private_key"]
        bot_id = config["bot_id"]
        ssh_password = config["ssh_password"]
        name_to_mac_file = config["name_to_mac_file"]
        last_message = get_last_message(bot_id, nb_try)
        print(last_message["message"]["text"])

        if re.match(r"/start.*", last_message["message"]["text"]) and is_a_new_message(last_message):
            message_text = last_message["message"]["text"].split(" ")
            starting_time = message_text[-1] if message_text[-1].isdigit() else 30
            device_name = message_text[1]
            mac, interface = get_data_from_name(device_name, name_to_mac_file)
            if not mac:
                send_bot_message(bot_id, id, "ERROR: device_name_not_in_database send /devices to print known devices")
            wake_me_up(mac, ssh_file, ssh_password, interface)
            started = status_checker(mac, starting_time, ssh_password, ssh_file)

            if not started:
                text = "not started in due time"
                send_bot_message(bot_id, id, text)
            else:
                text = "Up"
                send_bot_message(bot_id, id, text)
                store_timestamps(last_message)

        elif re.match(r"/add [^\s]+ [^\s]+", last_message['message']['text']) and is_a_new_message(last_message):
            if is_a_valid_add_message(last_message['message']['text']):
                store_new_pair(last_message["message"]["text"], name_to_mac_file)
                send_bot_message(bot_id, id, "Successfully Added")
            else:
                text = "ERROR: bad_message_format example: /add router_test a1:b6:23:dc:ff:99"
                send_bot_message(bot_id, id, text)
            store_timestamps(last_message)

        elif re.match(r"/devices", last_message["message"]["text"]) and is_a_new_message(last_message):
            send_bot_message(bot_id, id, get_devices(name_to_mac_file))
            store_timestamps(last_message)

        elif re.match(r"/delete [^\s]+", last_message['message']['text']) and is_a_new_message(last_message):
            if delete_mac_from_name(last_message['message']['text'].split(" ")[1], name_to_mac_file):
                text = "Device deleted"
                send_bot_message(bot_id, id, text)
            else:
                text = "Device not found. See /devices"
                send_bot_message(bot_id, id, text)
            store_timestamps(last_message)

        elif re.match(r"/help", last_message["message"]["text"]) and is_a_new_message(last_message):
            text = "/add NAME MAC ROUTER_INTERFACE\n\n/delete DEVICE_NAME\n\n/devices\n\n/start DEVICE_NAME STARTING_TIME"
            send_bot_message(bot_id, id, text)
            store_timestamps(last_message)
    except Exception as e:
        send_bot_message(bot_id, id, str(e))
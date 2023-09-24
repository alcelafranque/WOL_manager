from wakeonlan import send_magic_packet

import re
import subprocess
import threading
import os
from errors import NotFoundIp


def wake_me_up(mac):
    mac = mac.split(":")
    new_mac = ""
    for subpart in mac:
        new_mac += subpart + "-"
    send_magic_packet(new_mac[:-1])


def refresh_arp_table(ip):
    ip = ip.split(".")
    ip = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "."
    print("Refreshing arp table ")
    t = [threading.Thread(target=ping_target, args=(str(_), ip)) for _ in range(1, 256)]
    for p in t:
        p.start()
    for p in t:
        p.join()


def ping_target(_, ip):
    instr = "ping -c 1 " + ip + _ + " > /dev/null"
    os.system(instr)


def get_new_ip(mac):
    mac = format_mac(mac)
    arp_result = str(subprocess.check_output(["arp", "-a"])).split("\\n")
    for result in arp_result:
        fields = result.split(" ")
        # Change for if mac in fields
        if mac in fields:
            for field in fields:
                regex_ip = "^(\(?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\)?)$"
                if re.match(regex_ip, field):
                    return field[1:-1]
    raise NotFoundIp("mac not found in arp table")


def format_mac(mac):
    mac = mac.split("-")
    formated_mac = ""
    for elem in mac:
        formated_mac += elem.lower() + ":"
    return formated_mac[:-1]


def reformat_mac(mac):
    mac = mac.split(":")
    formated_mac = ""
    for elem in mac:
        formated_mac += elem.upper() + "-"
    return formated_mac[1:-2]

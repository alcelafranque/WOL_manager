from wakeonlan import send_magic_packet

import threading
import subprocess
import os
from errors import NotFoundIp

def wake_me_up(mac):
    send_magic_packet(mac)

def refresh_arp_table(ip):
    ip = ip.split(".")
    ip = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "."
    print("refreshing")
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
        if len(fields) > 3:
            if fields[3] == mac:
                return reformat_mac(fields[1])
    raise NotFoundIp("mac not found in arp table")


def format_mac(mac):
    mac = mac.split("-")
    formated_mac = ""
    for elem in mac:
        formated_mac += elem.lower() + ":"
    print(formated_mac[:-1])
    return formated_mac[:-1]


def reformat_mac(mac):
    mac = mac.split(":")
    formated_mac = ""
    for elem in mac:
        formated_mac += elem.upper() + "-"
    print(formated_mac[:-1])
    return formated_mac[1:-2]

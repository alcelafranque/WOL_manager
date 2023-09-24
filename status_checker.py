import os
import time
from telegram import get_new_ip, refresh_arp_table

NB_TRY = 6

def status_checker(mac, starting_time):
    nb_try = 0
    print("starting_time: ", starting_time)
    time.sleep(int(starting_time))
    ip = get_new_ip(mac)
    while not get_status(ip) and nb_try < NB_TRY:
        time.sleep(1)
        nb_try += 1
    return True if nb_try < NB_TRY else False

def get_status(ip):
    output = os.system("ping -c 1 -q " + ip)
    print(output)
    return True if output == 0 else False
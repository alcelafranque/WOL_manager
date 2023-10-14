import os
import sys
import time
from io import StringIO

import paramiko

NB_TRY = 6

def status_checker(mac, starting_time, mdp, ssh_filename):
    time.sleep(int(starting_time))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.240.128.254", username='wol', password=mdp, key_filename=ssh_filename)
    stdin, stdout, stderr = ssh.exec_command("ip neigh")
    buffer = StringIO()
    sys.stdout = buffer
    ip_neigh_output = buffer.getvalue()
    # restore stdout to default for print()
    sys.stdout = sys.__stdout__
    # This will be stored in the ip_neigh_output variable
    ssh.close()
    #FIXME: find a more complex way to check if it successed
    return True if mac.lower() in ip_neigh_output else False


def get_status(ip):
    output = os.system("ping -c 1 -q " + ip)
    return True if output == 0 else False
import os
import sys
import time
from io import StringIO

import paramiko

NB_TRY = 6

def status_checker(mac, starting_time, mdp, ssh_filename, ):
    time.sleep(int(starting_time))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.240.128.254", username='wol', password=mdp, key_filename=ssh_filename)
    stdin, stdout, stderr = ssh.exec_command("ip neigh")
    buffer = StringIO()
    sys.stdout = buffer
    print(stdout.read().decode())
    ip_neigh_output = buffer.getvalue()
    # restore stdout to default for print()
    sys.stdout = sys.__stdout__
    # This will be stored in the ip_neigh_output variable
    ssh.close()
    all_lines = ip_neigh_output.split("\n")
    for line in all_lines:
        line = line[:-1]
        if mac.lower() in line:
            if line.endswith("REACHABLE"):
                return True
    return False

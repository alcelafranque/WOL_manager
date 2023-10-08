import paramiko


def wake_me_up(mac, ssh_filename, mdp):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.240.128.254", username='wol', password=mdp, key_filename=ssh_filename)
    stdin, stdout, stderr = ssh.exec_command("sudo /usr/sbin/etherwake -i eth5.128 " + mac)
    ssh.close()
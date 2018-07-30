import json
import requests
import subprocess
import paramiko
import yaml
import time
import threading
def send_command(command,ip):
    username = "root"
    port = 22
    password="c0ntrail123"

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        client.connect(ip, port=port, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read())
    finally:
        client.close()

def config_file():
    f=open('data.yaml','r')
    default=f.read()
    defaults=yaml.load(default)
    defaults=defaults['Details']
    return defaults

def commands(ele):
    send_command("apt-get -y update",ele['ssh_ip'])
    time.sleep(2)
    send_command("apt-get -y install docker.io",ele['ssh_ip'])
    time.sleep(2)
    send_command(ele['docker'],ele['ssh_ip'])
defaults=config_file()
for ele in defaults:
    thread = threading.Thread(target=commands, args=(ele,))
    thread.start()

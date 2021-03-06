# @Author: Arohi Gupta <agupta>
# @Date:   2018-07-13T14:05:47-07:00
# @Email:  agupta@juniper.net
# @Filename: installdockerimages.py
# @Last modified by:   agupta
# @Last modified time: 2018-07-24T16:55:02-07:00

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
    f=open('/root/data.yaml','r')
    default=f.read()
    defaults=yaml.load(default)
    defaults=defaults['Details']
    return defaults

def commands(ele):
    send_command("kill $(ps -ef | grep apt | awk '{print $2}')",ele['meta_ip'])
    time.sleep(2)
    send_command("apt-get -y update",ele['meta_ip'])
    time.sleep(2)
    send_command("apt-get -y install docker.io",ele['meta_ip'])
    time.sleep(2)
    send_command(ele['docker'],ele['meta_ip'])
defaults=config_file()
for ele in defaults:
    thread = threading.Thread(target=commands, args=(ele,))
    thread.start()

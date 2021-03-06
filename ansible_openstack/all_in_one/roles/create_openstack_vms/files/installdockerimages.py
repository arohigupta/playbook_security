# @Author: Arohi Gupta <agupta>
# @Date:   2018-07-13T14:05:47-07:00
# @Email:  agupta@juniper.net
# @Filename: installdockerimages.py
# @Last modified by:   agupta
# @Last modified time: 2018-08-06T18:24:46-07:00

import json
import requests
import subprocess
import paramiko
import yaml
import time
import threading
import pprint

def issue_command(transport, pause, command):
    chan = transport.open_session()
    chan.exec_command(command)

    buff_size = 1024
    stdout = ""
    stderr = ""

    while not chan.exit_status_ready():
        time.sleep(pause)
        if chan.recv_ready():
            stdout += chan.recv(buff_size)

        if chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size)

    exit_status = chan.recv_exit_status()
    # Need to gobble up any remaining output after program terminates...
    while chan.recv_ready():
        stdout += chan.recv(buff_size)

    while chan.recv_stderr_ready():
        stderr += chan.recv_stderr(buff_size)

    return exit_status, stdout, stderr

def send_command(command,ip):
    username = "root"
    port = 22
    password="c0ntrail123"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password, timeout=3,)
    transport = client.get_transport()
    pause = 1
    exit_status, stdout, stderr=issue_command(transport, pause, command)
    print (exit_status)
    print (stdout)
    output=stderr
    if "dpkg was interrupted" in output:
        print ("************")
        exit_status, stdout, stderr = issue_command(transport, pause, "dpkg --configure -a")
    elif "apt-get -f -y install" in output:
        print ("!!!************!!!")
        exit_status, stdout, stderr = issue_command(transport, pause, "apt-get -f -y install")


def config_file():
    f=open('/root/data.yaml','r')
    default=f.read()
    defaults=yaml.load(default)
    defaults=defaults['Details']
    return defaults

def commands(ele):
    send_command("kill $(ps -ef | grep apt | awk '{print $2}')",ele['meta_ip'])
    print("1")
    send_command("apt-get -y update",ele['meta_ip'])
    print("2")
    send_command("apt-get -f -y install",ele['meta_ip'])

    send_command("apt-get -y install docker.io",ele['meta_ip'])
    print("3")

    send_command('docker pull '+ele['repo'],ele['meta_ip'])
    print("4")

defaults=config_file()

for ele in defaults:
    thread = threading.Thread(target=commands, args=(ele,))
    thread.start()
# sorted_order=sorted(defaults, key=lambda k: k['order'])#this ensures db -> app -> web is installed in order.
# pprint.pprint(sorted_order)
# for ele in sorted_order:
#     send_command(ele['docker'],ele['meta_ip'])

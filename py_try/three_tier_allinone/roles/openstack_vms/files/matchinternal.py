import json
import requests
import subprocess
import paramiko
import yaml

def get_ips():
    cmd = "netstat -rn  | grep vhost0 | grep 255.255.255.255 | awk -F '[ :]*' '{print $1}'"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    vhosts=output.splitlines()
    return vhosts[1::]

def make_dict(vhosts):

    deets={}
    deets['Details']=[]
    vns=matcheverything()
    for ele in vhosts:
        send_command('ifconfig ens3 | awk "/inet /" | cut -d":" -f 2 | cut -d" " -f1',ele,deets,vns)
    return deets

def send_command(command,ip,deets,vns):
    username = "root"
    port = 22
    password="c0ntrail123"

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        client.connect(ip, port=port, username=username, password=password)
        stdin, stdout, stderr = client.exec_command("ps -ef | grep apt | awk '{print $2}'")
        processes=stdout.read()
        if processes.splitlines()[0]:
            stdin, stdout, stderr = client.exec_command("kill -9 "+processes.splitlines()[0]+"")
            print (stdout.read())
        stdin, stdout, stderr = client.exec_command(command)
        vm_ip=stdout.read().strip("\n")
        for ele in vns:
            net=ele['ip_prefix']+'/'+str(ele['ip_prefix_len'])
            if addressInNetwork(vm_ip,net):
                docker_img=ele['docker']
            else:
                continue
        deets['Details'].append({'vm_ip':vm_ip,'ssh_ip':ip,'docker':docker_img})

    finally:
        client.close()

def addressInNetwork(ip, net):
   import socket,struct
   ipaddr = int(''.join([ '%02x' % int(x) for x in ip.split('.') ]), 16)
   netstr, bits = net.split('/')
   netaddr = int(''.join([ '%02x' % int(x) for x in netstr.split('.') ]), 16)
   mask = (0xffffffff << (32 - int(bits))) & 0xffffffff
   return (ipaddr & mask) == (netaddr & mask)

def matcheverything():
    f_def=open("roles/openstack_vms/defaults/main.yaml",'r')
    vns=yaml.load(f_def.read())['VNs']
    return vns
def main():
    vhosts=get_ips()
    deets=make_dict(vhosts)
    f=open("data.yaml",'w')
    f.write(yaml.dump(deets, explicit_start=True, default_flow_style=False))
    f.close()
    matcheverything()

if __name__ == '__main__':
    main()

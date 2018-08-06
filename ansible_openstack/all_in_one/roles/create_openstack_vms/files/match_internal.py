# @Author: Arohi Gupta <agupta>
# @Date:   2018-07-19T10:03:34-07:00
# @Email:  agupta@juniper.net
# @Last modified by:   agupta
# @Last modified time: 2018-08-05T23:09:43-07:00

import xml.etree.ElementTree as ET
import yaml
import requests

def parseoutput(URLs,instances_details):
    response = requests.get(URLs)
    root = ET.fromstring(response.content)
    for vals in root.findall("./ItfResp/itf_list/list/ItfSandeshData"):
        d={}
        if vals.find('vm_name').text:
            d['vm_name']= vals.find('vm_name').text
            d['meta_ip']=vals.find('mdata_ip_addr').text
            for ele in vals.findall('./vmi_tag_list/list/VmiTagData'):
                d['tier']=ele.find('name').text
            for ele in vals.findall('./fip_list/list/FloatingIpSandeshList'):
                d['ip_addr']=ele.find('ip_addr').text
            instances_details.append(d)
    return instances_details

def matcheverything():
    f_def=open("roles/create_openstack_vms/defaults/main.yaml",'r')
    vns=yaml.load(f_def.read())['VM_Data']
    return vns

def get_hosts():
    f_def=open("roles/create_openstack_vms/defaults/main.yaml",'r')
    hosts=yaml.load(f_def.read())['hosts']
    return hosts


def main():
    for ele in get_hosts():
        instances_details=[]
        deets={}
        deets['Details']=[]
        ip=ele['ip']
        api='http://'+ip+':8085/Snh_ItfReq?name=&type=&uuid=&vn=&mac=&ipv4_address=&ipv6_address=&parent_uuid=&ip_active=&ip6_active=&l2_active='
        instances_details=parseoutput(api,instances_details)
        for ele in matcheverything():
            for values in instances_details:
                if values['vm_name']==ele['name']:
                    values['docker']=ele['docker']
                    values['order']=ele['order']
                    deets['Details'].append(values)
                else:
                    continue
        f=open("roles/create_openstack_vms/files/data.yaml",'w')
        f.write(yaml.dump(deets, explicit_start=True, default_flow_style=False))
        f.close()

if __name__ == '__main__':
    main()

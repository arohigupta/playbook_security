This playbook brings up the security policies mentioned in this wiki.

cd /root/
git clone https://github.com/arohigupta/playbook_security.git
cd ansible_openstack
cd all_in_one
vi group_vars/all

Enter the IP address of the server.

# Variables here are applicable to all host groups

httpd_port: 8082
controlserver: <IP_address>


vi roles/create_openstack_vms/defaults/main.yaml
hosts:
  - ip: <ip_address>

Run: ansible_playbook playbook.yaml

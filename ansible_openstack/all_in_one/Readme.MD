# Contrail Security Example for all in one setup

This script creates security policies for a demo topology. <br />
Note: This procedure follows a specific demo topology and it's encouraged to use same or similar topology to effectively show case Contrail Security.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. This playbook performs the following tasks to demonstrate the functions to contrail security. <br />
1) Creates two projects and brings up three VMs (web,app,db) with respective containers on both the projects. <br />
2) It then applies the security polies on the fabric.

### Prerequisites

1)It is assumed that an all in one setup is pre-installed.
Refer the following page to install an all_in_one setup -> [ansible_deployer](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail-with-Kolla-Ocata)
<br />
2)Here is an example of [instance.yaml](./allinone_instance.yaml)<br />


### Installing

Clone the repo and edit these configuration files.

```
cd /root/
git clone https://github.com/arohigupta/playbook_security.git
cd ansible_openstack
cd all_in_one
vi group_vars/all
```

In the file `group_vars/all`.

```
httpd_port: 8082
controlserver: <IP_address_BMS>
```

Also change the following file with the same value:
```
vi roles/create_openstack_vms/defaults/main.yaml
```
```
hosts:
  - ip: <ip_address_BMS>
```
## Running the Playbook
To run the playbook run the following command. Ensure you are in the `all_in_one` directory

```
ansible_playbook playbook.yaml
```


## Testing the outcome.

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

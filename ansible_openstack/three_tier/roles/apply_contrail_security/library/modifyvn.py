# @Author: Arohi Gupta <agupta>
# @Date:   2018-07-16T10:20:11-07:00
# @Email:  agupta@juniper.net
# @Filename: modifyvn.py
# @Last modified by:   agupta
# @Last modified time: 2018-07-25T13:33:11-07:00

from ansible.module_utils.basic import AnsibleModule
import json
import requests
from jinja2 import Environment, FileSystemLoader,select_autoescape, PackageLoader


def find_vn(module):
    headers = {"Content-Type": module.params['Content_Type'],"X-Auth-Token": module.params['X_Auth_Token']}
    vn_name=module.params['vn_name']
    URL=module.params['URL']
    response = requests.get(URL+"virtual-networks",headers=headers)
    if response.status_code == 404:
        return None
    elif response.status_code < 200 or response.status_code > 299 or response.status_code == 401 or response.status_code== 409:
        raise requests.exceptions.RequestException(response.content)
    else:
        request=json.loads(response.text)
        context={}
        for ele in request["virtual-networks"]:
            if vn_name in ele['fq_name']:
                url=ele['href']
                context['href_url']=url
            else:
                continue
        return context

def run_module():
    # Define the argument specification
    module_args = dict(
        X_Auth_Token=dict(type='str', required=True),
        Content_Type=dict(type='str', required=True),
        vn_name=dict(type='str', required=True),
        URL=dict(type='str', required=True)
    )

    # Declare the module results
    result = dict(
        changed=False,
        details='',
        status_code='',
        href_url=''
    )

    # Load the module and populate the parameters
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    try:
        # Used for ansible-playbook --check
        if module.check_mode:
            return result

        headers = {
            "Content-Type": module.params['Content_Type'],
            "X-Auth-Token": module.params['X_Auth_Token']
        }

        news = find_vn(module)
        if news is not None:
            result['href_url'] = news['href_url']
        disable_snat='{"virtual-network": {"parent_type": "project","fabric_snat": false}}'
        response=requests.put(url=str(news['href_url']),headers=headers,data=disable_snat)
        result['details'] = response.content

        if response.status_code < 200 or response.status_code > 299 or response.status_code == 401 or response.status_code== 409:
            module.fail_json(msg="Failed (%s)" % response.status_code, **result)

        result['changed'] = True

        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        result['details'] = str(e)
        module.fail_json(msg="Connection to Server failed", **result)

def main():
    run_module()

if __name__ == '__main__':
    main()

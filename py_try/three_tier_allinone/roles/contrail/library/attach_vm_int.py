from ansible.module_utils.basic import AnsibleModule
import json
import requests
from jinja2 import Environment, FileSystemLoader,select_autoescape, PackageLoader


def find_vmi(module):
    headers = {"Content-Type": module.params['Content_Type'],"X-Auth-Token": module.params['X_Auth_Token']}
    URL=module.params['URL']

    response = requests.get("http://10.87.5.8:8082/virtual-machine-interfaces",headers=headers)
    if response.status_code == 404:
        return None
    elif response.status_code < 200 or response.status_code > 299 or response.status_code == 401 or response.status_code== 409:
        raise requests.exceptions.RequestException(response.content)
    else:
        request=json.loads(response.text)
        context={}
        for ele in request["virtual-machine-interfaces"]:
            if "vhost0" in ele['fq_name']:
                val=ele['fq_name'][1]
                context['hostname']=val
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
        URL=dict(type='str', required=True),
        name=dict(type='str', required=True),
        tags=dict(type='str', required=True),
        label=dict(type='str', required=True)
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

        data = {
            "name": module.params['name'],
            "tags": module.params['tags'],
            "label": module.params['label']
        }

        news = find_vmi(module)
        if news is not None:
            result['href_url'] = news['href_url']
            result['hostname'] = news['hostname']
            data['hostname']=news['hostname']
        tag='{"virtual-machine-interface":{"name": "{{name}}","fq_name": ["default-global-system-config", "{{hostname}}", "{{name}}"],"virtual_network_refs":  [{"to":  ["default-domain","default-project","{{label}}"],"attr": "null"}],"tag_refs":  [{"to":  ["tier={{tags}}"],"attr": "null"}]}}'
        response=requests.put(url=str(news['href_url']),headers=headers,data=(Environment().from_string(tag).render(data)))
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

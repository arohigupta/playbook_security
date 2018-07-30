# @Author: Arohi Gupta <agupta>
# @Date:   2018-07-06T13:26:26-07:00
# @Email:  agupta@juniper.net
# @Filename: attach_project.py
# @Last modified by:   agupta
# @Last modified time: 2018-07-25T13:31:17-07:00

from ansible.module_utils.basic import AnsibleModule
import json
import requests
from jinja2 import Environment, FileSystemLoader,select_autoescape, PackageLoader


def find_projs(module):
    headers = {"Content-Type": module.params['Content_Type'],"X-Auth-Token": module.params['X_Auth_Token']}
    URL=module.params['URL']
    proj_name=module.params['proj_name']
    response = requests.get(URL+"projects",headers=headers)

    if response.status_code == 404:
        return None
    elif response.status_code < 200 or response.status_code > 299 or response.status_code == 401 or response.status_code== 409:
        raise requests.exceptions.RequestException(response.content)
    else:
        data=json.loads(response.text)
        context={}
        for ele in data['projects']:
            if proj_name in ele['fq_name']:
                context['href_project']=ele['href']
                context['project_name']=proj_name
        return context

def run_module():
    # Define the argument specification
    module_args = dict(
        X_Auth_Token=dict(type='str', required=True),
        Content_Type=dict(type='str', required=True),
        URL=dict(type='str', required=True),
        proj_name=dict(type='str', required=True),
        tag_name1=dict(type='str', required=True),
        tag_name2=dict(type='str', required=True),
        tag_name3=dict(type='str', required=True),
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
            "proj_name": module.params['proj_name'],
            "tag_name1": module.params['tag_name1'],
            "tag_name2": module.params['tag_name2'],
            "tag_name3": module.params['tag_name3']
        }

        news = find_projs(module)
        if news is not None:
            result['href_project'] = news['href_project']
            result['project_name'] = news['project_name']
            data['href_project']=news['href_project']
        attachproj='{"project":{"href":"{{href_project}}","display_name":"{{project_name}}","name":"{{project_name}}","fq_name":["default-domain","{{project_name}}"],"tag_refs":[{"to":["{{tag_name1}}"],"attr":null},{"to":["{{tag_name2}}"],"attr":null},{"to":["{{tag_name3}}"],"attr":null}]}}'
        response=requests.put(url=str(news['href_project']),headers=headers,data=(Environment().from_string(attachproj).render(data)))
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

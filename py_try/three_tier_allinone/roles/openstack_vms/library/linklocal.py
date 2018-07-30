from ansible.module_utils.basic import AnsibleModule
import json
import requests
from jinja2 import Environment, FileSystemLoader,select_autoescape, PackageLoader


def find_uuid(module):
    headers = {"Content-Type": module.params['Content_Type'],"X-Auth-Token": module.params['X_Auth_Token']}
    URL=module.params['URL']

    response = requests.get("http://10.87.5.8:8082/global-vrouter-configs",headers=headers)
    if response.status_code == 404:
        return None
    elif response.status_code < 200 or response.status_code > 299 or response.status_code == 401 or response.status_code== 409:
        raise requests.exceptions.RequestException(response.content)
    else:
        request=json.loads(response.text)
        context={}
        for ele in request["global-vrouter-configs"]:
            if "default-global-system-config" in ele['fq_name']:
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
        news = find_uuid(module)
        if news is not None:
            result['href_url'] = news['href_url']
        news['URL']=module.params['URL']
        put_sec='{"global-vrouter-config":{"flow_export_rate":-1,"flow_aging_timeout_list":{"flow_aging_timeout":[{"timeout_in_seconds":2147483647,"protocol":"tcp","port":9161},{"timeout_in_seconds":2147483647,"protocol":"tcp","port":5673},{"timeout_in_seconds":2147483647,"protocol":"tcp","port":8082}]},"encryption_mode":"none","ecmp_hashing_include_fields":{"destination_ip":true,"ip_protocol":true,"source_ip":true,"hashing_configured":true,"source_port":true,"destination_port":true},"vxlan_network_identifier_mode":"automatic","enable_security_logging":true,"name":"default-global-vrouter-config","forwarding_mode":null,"port_translation_pools":{"port_translation_pool":[{"port_count":"1024","protocol":"tcp"},{"port_count":"1024","protocol":"udp"}]},"linklocal_services":{"linklocal_service_entry":[{"linklocal_service_name":"LinkLocalVrouterAgent","ip_fabric_service_ip":["127.0.0.1"],"linklocal_service_ip":"10.10.10.1","ip_fabric_service_port":9091,"ip_fabric_DNS_service_name":"","linklocal_service_port":9091},{"linklocal_service_name":"metadata","ip_fabric_service_ip":["{{IP}}"],"linklocal_service_ip":"169.254.169.254","ip_fabric_service_port":8775,"ip_fabric_DNS_service_name":"","linklocal_service_port":80}]},"encapsulation_priorities":{"encapsulation":["MPLSoUDP","MPLSoGRE","VXLAN"]}}}'
        response=requests.put(url=str(news['href_url']),headers=headers,data=(Environment().from_string(put_sec).render(news)))
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

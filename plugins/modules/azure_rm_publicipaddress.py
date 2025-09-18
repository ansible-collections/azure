#!/usr/bin/python
#
# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_publicipaddress

version_added: "0.1.0"

short_description: Manage Azure Public IP Addresses

description:
    - Create, update and delete a Public IP address.
    - Allows setting and updating the address allocation method and domain name label.
    - Use the M(azure.azcollection.azure_rm_networkinterface) module to associate a Public IP with a network interface.

options:
    resource_group:
        description:
            - Name of resource group with which the Public IP is associated.
        required: true
        type: str
    allocation_method:
        description:
            - Control whether the assigned Public IP remains permanently assigned to the object.
            - If not set to C(Static), the IP address may changed anytime an associated virtual machine is power cycled.
        type: str
        choices:
            - dynamic
            - static
            - Static
            - Dynamic
        default: dynamic
    domain_name:
        description:
            - The customizable portion of the FQDN assigned to public IP address. This is an explicit setting.
            - If no value is provided, any existing value will be removed on an existing public IP.
        type: str
        aliases:
            - domain_name_label
    reverse_fqdn:
        description:
            - The reverse FQDN.
            - A user-visible, fully qualified domain name that resolves to this public IP address.
            - If the reverseFqdn is specified, then a PTR DNS record is created pointing from the IP address in the in-addr.arpa domain to the reverse FQDN.
        type: str
    name:
        description:
            - Name of the Public IP.
        type: str
        required: true
    public_ip_prefix:
        description:
            - The Public IP Prefix this Public IP Address should be allocated from.
            - Once set, it cannot be updated.
        type: dict
        suboptions:
            id:
                description:
                    - The Public IP Prefix ID.
                type: str
    state:
        description:
            - Assert the state of the Public IP. Use C(present) to create or update a and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    sku:
        description:
            - The public IP address SKU.
            - When I(version=ipv6), if I(sku=standard) then set I(allocation_method=static).
            - When I(version=ipv4), if I(sku=standard) then set I(allocation_method=static).
            - The I(sku=basic) will be retired on September 30, 2025.
            - New I(sku=basic) SKU resource cannot be deployed after March 31, 2025.
        type: str
        choices:
            - standard
            - Standard
    ip_tags:
        description:
            - List of IpTag associated with the public IP address.
            - Each element should contain type:value pair.
        type: list
        elements: dict
        suboptions:
            type:
                description:
                    - Sets the ip_tags type.
                type: str
                required: true
            value:
                description:
                    - Sets the ip_tags value.
                type: str
                required: true
    idle_timeout:
        description:
            - Idle timeout in minutes.
        type: int
    version:
        description:
            - The public IP address version.
        type: str
        choices:
            - ipv4
            - ipv6
        default: ipv4
    zones:
        description:
            - A list of availability zones denoting the IP allocated for the resource needs to come from.
        type: list
        elements: str
        choices:
            - '1'
            - '2'
            - '3'

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Chris Houseknecht (@chouseknecht)
    - Matt Davis (@nitzmahone)
'''

EXAMPLES = '''
- name: Create a public ip address
  azure_rm_publicipaddress:
    resource_group: myResourceGroup
    name: my_public_ip
    allocation_method: static
    domain_name: foobar

- name: Delete public ip
  azure_rm_publicipaddress:
    resource_group: myResourceGroup
    name: my_public_ip
    state: absent
'''

RETURN = '''
state:
    description:
        - Facts about the current state of the object.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource's ID.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Network/publicIPAddresses/pip01
        dns_settings:
            description:
                - The FQDN of the DNS record associated with the public IP address.
            returned: always
            type: dict
            sample: {
            "domain_name_label": "ansible-b57dc95985712e45eb8b9c2e",
            "fqdn": "ansible-b57dc95985712e45eb8b9c2e.eastus.cloudapp.azure.com",
            "reverse_fqdn": "ansible-b57dc95985712e45eb8b9c2f.eastus.cloudapp.azure.com"
        }
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "W/'1905ee13-7623-45b1-bc6b-4a12b2fb9d15'"
        idle_timeout_in_minutes:
            description:
                - The idle timeout of the public IP address.
            returned: always
            type: int
            sample: 4
        ip_address:
            description:
                - The Public IP Prefix this Public IP Address should be allocated from.
            returned: always
            type: str
            sample: 52.160.103.93
        location:
            description:
                - Resource location.
            returned: always
            type: str
            example: eastus
        name:
            description:
                - Name of the Public IP Address.
            returned: always
            type: str
            example: publicip002
        provisioning_state:
            description:
                - The provisioning state of the Public IP resource.
            returned: always
            type: str
            example: Succeeded
        public_ip_allocation_method:
             description:
                 - The public IP allocation method.
             returned: always
             type: str
             sample: static
        public_ip_address_version:
             description:
                 - The public IP address version.
             returned: always
             type: str
             sample: ipv4
        public_ip_prefix:
            description:
                - The Public IP Prefix this Public IP Address should be allocated from.
            type: dict
            returned: when-used
            sample: {"id": "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Network/publicIPPrefixes/prefix01"}
        sku:
            description:
                - The public IP address SKU.
            returned: always
            type: str
            sample: Standard
        tags:
            description:
                - The resource tags.
            returned: always
            type: dict
            sample: {
                "delete": "on-exit",
                "testing": "testing"
                }
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: "Microsoft.Network/publicIPAddresses"
        zones:
            description:
                - A list of availability zones denoting the IP allocated for the resource needs to come from.
            returned: always
            type: list
            sample: ['1', '2']
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils._text import to_native

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


def pip_to_dict(pip):
    result = dict(
        name=pip.name,
        id=pip.id,
        type=pip.type,
        location=pip.location,
        tags=pip.tags,
        public_ip_allocation_method=pip.public_ip_allocation_method.lower(),
        public_ip_address_version=pip.public_ip_address_version.lower(),
        dns_settings=dict(),
        ip_address=pip.ip_address,
        idle_timeout_in_minutes=pip.idle_timeout_in_minutes,
        provisioning_state=pip.provisioning_state,
        etag=pip.etag,
        sku=pip.sku.name,
        zones=pip.zones,
        public_ip_prefix=None
    )
    if pip.dns_settings:
        result['dns_settings']['domain_name_label'] = pip.dns_settings.domain_name_label
        result['dns_settings']['fqdn'] = pip.dns_settings.fqdn
        result['dns_settings']['reverse_fqdn'] = pip.dns_settings.reverse_fqdn
    if pip.ip_tags:
        result['ip_tags'] = [dict(type=to_native(x.ip_tag_type), value=to_native(x.tag)) for x in pip.ip_tags]
    if pip.public_ip_prefix:
        result['public_ip_prefix'] = dict(id=pip.public_ip_prefix.id)

    return result


ip_tag_spec = dict(
    type=dict(type='str', required=True),
    value=dict(type='str', required=True)
)


class AzureRMPublicIPAddress(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            version=dict(type='str', default='ipv4', choices=['ipv4', 'ipv6']),
            allocation_method=dict(type='str', default='dynamic', choices=['Dynamic', 'Static', 'dynamic', 'static']),
            domain_name=dict(type='str', aliases=['domain_name_label']),
            reverse_fqdn=dict(type='str'),
            sku=dict(type='str', choices=['Standard', 'standard']),
            ip_tags=dict(type='list', elements='dict', options=ip_tag_spec),
            idle_timeout=dict(type='int'),
            public_ip_prefix=dict(type='dict', options=dict(id=dict(type='str'))),
            zones=dict(type='list', elements='str', choices=['1', '2', '3'])
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.tags = None
        self.zones = None
        self.allocation_method = None
        self.domain_name = None
        self.reverse_fqdn = None
        self.sku = None
        self.version = None
        self.ip_tags = None
        self.idle_timeout = None
        self.public_ip_prefix = None

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMPublicIPAddress, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        results = dict()
        changed = False
        pip = None

        # capitalize the sku and allocation_method. standard => Standard, Standard => Standard.
        self.allocation_method = self.allocation_method.capitalize() if self.allocation_method else None
        self.sku = self.sku.capitalize() if self.sku else None
        self.version = 'IPv4' if self.version == 'ipv4' else 'IPv6'

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        try:
            self.log("Fetch public ip {0}".format(self.name))
            pip = self.network_client.public_ip_addresses.get(self.resource_group, self.name)
            self.check_provisioning_state(pip, self.state)
            self.log("PIP {0} exists".format(self.name))
            if self.state == 'present':
                results = pip_to_dict(pip)
                domain_lable = results['dns_settings'].get('domain_name_label')
                if self.domain_name is not None and ((self.domain_name or domain_lable) and self.domain_name != domain_lable):
                    self.log('CHANGED: domain_name_label')
                    changed = True
                    results['dns_settings']['domain_name_label'] = self.domain_name

                if self.reverse_fqdn is not None and self.reverse_fqdn != results['dns_settings'].get('reverse_fqdn'):
                    changed = True
                    self.log('CHANGED: reverse_fqdn')
                else:
                    self.reverse_fqdn = results['dns_settings'].get('reverse_fqdn')

                if self.allocation_method.lower() != results['public_ip_allocation_method'].lower():
                    self.log("CHANGED: allocation_method")
                    changed = True
                    results['public_ip_allocation_method'] = self.allocation_method

                if self.sku and self.sku != results['sku']:
                    self.log("CHANGED: sku")
                    changed = True
                    results['sku'] = self.sku

                if self.version.lower() != results['public_ip_address_version'].lower():
                    self.log("CHANGED: version")
                    changed = True
                    results['public_ip_address_version'] = self.version

                if self.idle_timeout and self.idle_timeout != results['idle_timeout_in_minutes']:
                    self.log("CHANGED: idle_timeout")
                    changed = True
                    results['idle_timeout_in_minutes'] = self.idle_timeout

                if self.zones and self.zones != results['zones']:
                    self.log("Zones defined do not same with existing zones")
                    changed = False
                    self.fail("ResourceAvailabilityZonesCannotBeModified: defines is {0}, existing is {1}".format(self.zones, results['zones']))

                if str(self.ip_tags or []) != str(results.get('ip_tags') or []):
                    self.log("CHANGED: ip_tags")
                    changed = True
                    results['ip_tags'] = self.ip_tags

                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True

            elif self.state == 'absent':
                self.log("CHANGED: public ip {0} exists but requested state is 'absent'".format(self.name))
                changed = True
        except ResourceNotFoundError:
            self.log('Public ip {0} does not exist'.format(self.name))
            if self.state == 'present':
                self.log("CHANGED: pip {0} does not exist but requested state is 'present'".format(self.name))
                changed = True

        self.results['state'] = results
        self.results['changed'] = changed

        if self.check_mode:
            return dict(state=results)

        if changed:
            if self.state == 'present':
                if not pip:
                    self.log("Create new Public IP {0}".format(self.name))
                    pip = self.network_models.PublicIPAddress(
                        location=self.location,
                        public_ip_address_version=self.version,
                        public_ip_prefix=self.public_ip_prefix,
                        public_ip_allocation_method=self.allocation_method,
                        sku=self.network_models.PublicIPAddressSku(name=self.sku) if self.sku else None,
                        idle_timeout_in_minutes=self.idle_timeout if self.idle_timeout and self.idle_timeout > 0 else None,
                        zones=self.zones
                    )
                    if self.ip_tags:
                        pip.ip_tags = [self.network_models.IpTag(ip_tag_type=x['type'], tag=x['value']) for x in self.ip_tags]
                    if self.tags:
                        pip.tags = self.tags
                    if self.domain_name or self.reverse_fqdn:
                        pip.dns_settings = self.network_models.PublicIPAddressDnsSettings(
                            domain_name_label=self.domain_name,
                            reverse_fqdn=self.reverse_fqdn
                        )
                else:
                    self.log("Update Public IP {0}".format(self.name))
                    pip = self.network_models.PublicIPAddress(
                        location=results['location'],
                        public_ip_allocation_method=results['public_ip_allocation_method'],
                        sku=self.network_models.PublicIPAddressSku(name=self.sku) if self.sku else None,
                        tags=results['tags'],
                        public_ip_prefix=self.public_ip_prefix,
                        zones=results['zones']
                    )
                    if self.domain_name or self.reverse_fqdn:
                        pip.dns_settings = self.network_models.PublicIPAddressDnsSettings(
                            domain_name_label=self.domain_name,
                            reverse_fqdn=self.reverse_fqdn
                        )
                self.results['state'] = self.create_or_update_pip(pip)
            elif self.state == 'absent':
                self.log('Delete public ip {0}'.format(self.name))
                self.delete_pip()

        return self.results

    def create_or_update_pip(self, pip):
        try:
            poller = self.network_client.public_ip_addresses.begin_create_or_update(self.resource_group, self.name, pip)
            pip = self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error creating or updating {0} - {1}".format(self.name, str(exc)))
        return pip_to_dict(pip)

    def delete_pip(self):
        try:
            poller = self.network_client.public_ip_addresses.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting {0} - {1}".format(self.name, str(exc)))
        # Delete returns nada. If we get here, assume that all is well.
        self.results['state']['status'] = 'Deleted'
        return True


def main():
    AzureRMPublicIPAddress()


if __name__ == '__main__':
    main()

#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_webappaccessrestriction
version_added: "1.8.0"
short_description: Manage web app network access restrictions
description:
    - Add, remove, or update network access restrictions for a web app.
options:
    name:
        description:
            - Name of the web app.
        required: true
        type: str
    resource_group:
        description:
            - Resource group of the web app.
        required: true
        type: str
    state:
        description:
            - State of the access restrictions. Use C(present) to create or update and C(absent) to delete.
        type: str
        default: present
        choices:
            - absent
            - present
    ip_security_restrictions:
        description:
            - The web app's HTTP access restrictions.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the access restriction.
                type: str
            description:
                description:
                    - Description of the access restriction.
                type: str
            action:
                description:
                    - Traffic action for the access restriction.
                type: str
                default: Allow
                choices:
                    - Allow
                    - Deny
            priority:
                description:
                    - Numerical priority of the access restriction.
                type: int
                required: true
            ip_address:
                description:
                    - IPv4 address (with subnet mask) of the access restriction.
                type: str
                required: true
    scm_ip_security_restrictions:
        description:
            - >-
                The web app's SCM access restrictions. If C(scm_ip_security_restrictions_use_main) is set to C(true),
                the SCM restrictions will be configured but not used.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the access restriction.
                type: str
            description:
                description:
                    - Description of the access restriction.
                type: str
            action:
                description:
                    - Traffic action for the access restriction.
                type: str
                default: Allow
                choices:
                    - Allow
                    - Deny
            priority:
                description:
                    - Numerical priority of the access restriction.
                type: int
                required: true
            ip_address:
                description:
                    - IPv4 address (with subnet mask) of the access restriction.
                type: str
                required: true
    scm_ip_security_restrictions_use_main:
        description:
            - >-
                Set to C(true) to have the HTTP access restrictions also apply to the SCM site.
                If C(scm_ip_security_restrictions) are also applied, they will configured but not used.
        default: false
        type: bool

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
    - name: Configure web app access restrictions.
      azure.azcollection.azure_rm_webappaccessrestriction:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
        ip_security_restrictions:
          - name: "Datacenter 1"
            action: "Allow"
            ip_address: "1.1.1.1/24"
            priority: 1
          - name: "Datacenter 2"
            action: "Allow"
            ip_address: "2.2.2.2/24"
            priority: 2
        scm_ip_security_restrictions_use_main: true

    - name: Delete web app network access restrictions.
      azure.azcollection.azure_rm_webappaccessrestriction:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
        state: "absent"
'''

RETURN = '''
ip_security_restrictions:
    description:
        - The web app's HTTP access restrictions.
    returned: always
    type: list
    elements: dict
    contains:
        name:
            description:
                - Name of the access restriction.
            returned: always
            type: str
            sample: my-access-restriction
        description:
            description:
               - Description of the access restriction.
            returned: always
            type: str
            sample: my-access-restriction-description
        action:
            description:
               - Traffic action of the access restriction.
            returned: always
            type: str
            sample: Allow
        priority:
            description:
               - Numerical priority of the access restriction.
            returned: always
            type: int
            sample: 1
        ip_address:
            description:
               - IP address of the access restriction.
            returned: always
            type: str
            sample: 1.1.1.1/32
scm_ip_security_restrictions:
    description:
        - The web app's SCM access restrictions.
    returned: always
    type: list
    elements: dict
    contains:
        name:
            description:
                - Name of the access restriction.
            returned: always
            type: str
            sample: my-access-restriction
        description:
            description:
               - Description of the access restriction.
            returned: always
            type: str
            sample: my-access-restriction-description
        action:
            description:
               - Traffic action of the access restriction.
            returned: always
            type: str
            sample: Allow
        priority:
            description:
               - Numerical priority of the access restriction.
            returned: always
            type: int
            sample: 1
        ip_address:
            description:
               - IP address of the access restriction.
            returned: always
            type: str
            sample: 1.1.1.1/32
scm_ip_security_restrictions_use_main:
    description:
        - Whether the HTTP access restrictions are used for SCM access.
    returned: always
    type: bool
    sample: false
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.web.models import IpSecurityRestriction
except Exception:
    # This is handled in azure_rm_common
    pass

ip_restriction_spec = dict(
    name=dict(type='str'),
    description=dict(type='str'),
    action=dict(type='str', default='Allow', choices=['Allow', 'Deny']),
    priority=dict(type='int', required=True),
    ip_address=dict(type='str', required=True),
)


class AzureRMWebAppAccessRestriction(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            ip_security_restrictions=dict(type='list', default=[], elements='dict', options=ip_restriction_spec),
            scm_ip_security_restrictions=dict(type='list', default=[], elements='dict', options=ip_restriction_spec),
            scm_ip_security_restrictions_use_main=dict(type='bool', default=False),
        )

        self.results = dict(
            changed=False,
            ip_security_restrictions=[],
            scm_ip_security_restrictions=[],
            scm_ip_security_restrictions_use_main=False,
        )

        self.state = None
        self.name = None
        self.resource_group = None
        self.ip_security_restrictions = []
        self.scm_ip_security_restrictions = []
        self.scm_ip_security_restrictions_use_main = False

        super(AzureRMWebAppAccessRestriction, self).__init__(self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        changed = False
        site_config = self.get_webapp_config()
        self.results.update(self.set_results(site_config))

        if self.state == 'absent' and self.has_access_restrictions(site_config):
            changed = True
            if not self.check_mode:
                self.log('Removing all access restrictions for webapp {0}'.format(self.name))
                site_config.ip_security_restrictions = []
                site_config.scm_ip_security_restrictions = []
                site_config.scm_ip_security_restrictions_use_main = False
                self.update_webapp_config(site_config)
                self.results['ip_security_restrictions'] = []
                self.results['scm_ip_security_restrictions'] = []
                self.results['scm_ip_security_restrictions_use_main'] = False
        elif self.state == 'present':
            if not self.has_access_restrictions(site_config) and (self.ip_security_restrictions or self.scm_ip_security_restrictions):
                self.log('Adding new access restrictions for webapp {0}'.format(self.name))
                changed = True
            elif self.has_updates(site_config):
                self.log('Detected change in existing access restrictions for webapp {0}'.format(self.name))
                changed = True

            if changed:
                site_config = self.get_updated_config(site_config)
                if not self.check_mode:
                    self.log('Updating site config for webapp {0}'.format(self.name))
                    site_config = self.update_webapp_config(site_config)

                self.results.update(self.set_results(site_config))

        self.results['changed'] = changed

        return self.results

    def get_updated_config(self, site_config):
        site_config.ip_security_restrictions = [] if not self.ip_security_restrictions else self.to_restriction_obj_list(self.ip_security_restrictions)
        site_config.scm_ip_security_restrictions = [] if not self.scm_ip_security_restrictions else (
            self.to_restriction_obj_list(self.scm_ip_security_restrictions))
        site_config.scm_ip_security_restrictions_use_main = self.scm_ip_security_restrictions_use_main
        return site_config

    def has_updates(self, site_config):
        return (site_config.scm_ip_security_restrictions_use_main != self.scm_ip_security_restrictions_use_main or self.ip_security_restrictions and
                self.ip_security_restrictions != self.to_restriction_dict_list(site_config.ip_security_restrictions) or self.scm_ip_security_restrictions and
                self.scm_ip_security_restrictions != self.to_restriction_dict_list(site_config.scm_ip_security_restrictions))

    def has_access_restrictions(self, site_config):
        return site_config.ip_security_restrictions or site_config.scm_ip_security_restrictions

    def get_webapp_config(self):
        try:
            return self.web_client.web_apps.get_configuration(resource_group_name=self.resource_group, name=self.name)
        except Exception as exc:
            self.fail("Error getting webapp config {0} (rg={1}) - {2}".format(self.name, self.resource_group, str(exc)))

    def update_webapp_config(self, param):
        try:
            return self.web_client.web_apps.create_or_update_configuration(resource_group_name=self.resource_group, name=self.name, site_config=param)
        except Exception as exc:
            self.fail("Error creating/updating webapp config {0} (rg={1}) - {2}".format(self.name, self.resource_group, str(exc)))

    def set_results(self, site_config):
        output = dict()
        if site_config.ip_security_restrictions:
            output['ip_security_restrictions'] = self.to_restriction_dict_list(site_config.ip_security_restrictions)
        if site_config.scm_ip_security_restrictions:
            output['scm_ip_security_restrictions'] = self.to_restriction_dict_list(site_config.scm_ip_security_restrictions)
        output['scm_ip_security_restrictions_use_main'] = site_config.scm_ip_security_restrictions_use_main
        return output

    def to_restriction_obj_list(self, restriction_dict_list):
        return [] if not restriction_dict_list else [self.to_restriction_obj(restriction) for restriction in restriction_dict_list]

    def to_restriction_obj(self, restriction_dict):
        return IpSecurityRestriction(
            name=restriction_dict['name'],
            description=restriction_dict['description'],
            action=restriction_dict['action'],
            priority=restriction_dict['priority'],
            ip_address=restriction_dict['ip_address'],
        )

    def to_restriction_dict_list(self, restriction_obj_list):
        restrictions = []
        if restriction_obj_list:
            for r in restriction_obj_list:
                restriction = self.to_restriction_dict(r)
                if not self.is_azure_default_restriction(restriction):
                    restrictions.append(restriction)

        return restrictions

    def is_azure_default_restriction(self, restriction_obj):
        return (restriction_obj["action"] == "Allow" and restriction_obj["ip_address"] == "Any" and restriction_obj["priority"] == 1) or \
            (restriction_obj["action"] == "Deny" and restriction_obj["ip_address"] == "Any" and restriction_obj["priority"] == 2147483647)

    def to_restriction_dict(self, restriction_obj):
        return dict(
            name=restriction_obj.name,
            description=restriction_obj.description,
            action=restriction_obj.action,
            priority=restriction_obj.priority,
            ip_address=restriction_obj.ip_address,
        )


def main():
    AzureRMWebAppAccessRestriction()


if __name__ == '__main__':
    main()

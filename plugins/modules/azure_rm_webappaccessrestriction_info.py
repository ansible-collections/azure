#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_webappaccessrestriction_info
version_added: "1.8.0"
short_description: Retrieve web app network access restriction facts
description:
    - Get facts for a web app's network access restrictions.
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

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
    - name: View web app access restrictions.
      azure.azcollection.azure_rm_webappaccessrestriction_info:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
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


class AzureRMWebAppAccessRestrictionInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
        )

        self.results = dict(
            changed=False,
            ip_security_restrictions=[],
            scm_ip_security_restrictions=[],
            scm_ip_security_restrictions_use_main=False,
        )

        self.name = None
        self.resource_group = None

        super(AzureRMWebAppAccessRestrictionInfo, self).__init__(self.module_arg_spec,
                                                                 supports_check_mode=True,
                                                                 supports_tags=False,
                                                                 facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        site_config = self.get_webapp_config()
        self.results.update(self.set_results(site_config))

        return self.results

    def get_webapp_config(self):
        try:
            return self.web_client.web_apps.get_configuration(resource_group_name=self.resource_group, name=self.name)
        except Exception as exc:
            self.fail("Error getting webapp config {0} (rg={1}) - {2}".format(self.name, self.resource_group, str(exc)))

    def set_results(self, site_config):
        output = dict()
        if site_config.ip_security_restrictions:
            output['ip_security_restrictions'] = self.to_restriction_dict_list(site_config.ip_security_restrictions)
        if site_config.scm_ip_security_restrictions:
            output['scm_ip_security_restrictions'] = self.to_restriction_dict_list(site_config.scm_ip_security_restrictions)
        output['scm_ip_security_restrictions_use_main'] = site_config.scm_ip_security_restrictions_use_main
        return output

    def to_restriction_dict_list(self, restriction_obj_list):
        return [] if not restriction_obj_list else [self.to_restriction_dict(restriction) for restriction in restriction_obj_list]

    def to_restriction_dict(self, restriction_obj):
        return dict(
            name=restriction_obj.name,
            description=restriction_obj.description,
            action=restriction_obj.action,
            priority=restriction_obj.priority,
            ip_address=restriction_obj.ip_address,
        )


def main():
    AzureRMWebAppAccessRestrictionInfo()


if __name__ == '__main__':
    main()

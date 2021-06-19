#!/usr/bin/python
#
# Copyright (c) 2021 Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '''
---
module: azure_rm_ddosprotectionplan
version_added: "1.7.0"
short_description: Manage DDoS protection plan
description:
    - Create, update and delete instance of DDoS protection plan.
options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: true
        type: str
    name:
        description:
            - Unique name of the app service plan to create or update.
        required: true
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    state:
      description:
          - Assert the state of the DDoS protection plan.
          - Use C(present) to create or update an DDoS protection plan and C(absent) to delete it.
      type: str
      default: present
      choices:
          - absent
          - present
    log_path:
        description:
            - parent argument.
        type: str
    log_mode:
        description:
            - parent argument.
        type: str
extends_documentation_fragment:
   - azure.azcollection.azure
   - azure.azcollection.azure_tags
author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldasan)
'''
EXAMPLES = '''
- name: "Create DDoS protection plan"
  azure_rm_ddosprotectionplan:
    resource_group: rg
    location: eastus
    name: ddosplan
- name: Delete DDoS protection plan
  azure_rm_ddosprotectionplan:
    resource_group: rg
    name: ddosplan
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the DDoS protection plan.
    returned: always
    type: dict
    sample: {
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/ddosProtectionPlans/ddosplan",
        "location": "eastus",
        "name": "ddosplan",
        "etag": "W/60ac0480-44dd-4881-a2ed-680d20b3978e",
        "provisioning_state": "Succeeded",
        "resource_guid": null,
        "type": "Microsoft.Network/ddosProtectionPlans",
        "tags": {"a": "b"},
        "virtual_networks": []
    }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureDDoSProtectionPlan(AzureRMModuleBase):

    def __init__(self):
        # define user inputs from playbook

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            state=dict(choices=['present', 'absent'],
                       default='present', type='str'),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.tags = None
        self.log_path = None
        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureDDoSProtectionPlan, self).__init__(self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.results['check_mode'] = self.check_mode

        # retrieve resource group to make sure it exists
        self.get_resource_group(self.resource_group)

        results = dict()
        changed = False

        try:
            self.log('Fetching DDoS protection plan {0}'.format(self.name))
            ddos_protection_plan = self.network_client.ddos_protection_plans.get(
                self.resource_group, self.name)

            results = ddos_protection_plan_to_dict(ddos_protection_plan)

            # don't change anything if creating an existing zone, but change if deleting it
            if self.state == 'present':
                changed = False

                update_tags, results['tags'] = self.update_tags(
                    results['tags'])
                if update_tags:
                    changed = True

            elif self.state == 'absent':
                changed = True

        except CloudError:
            # the DDoS protection plan does not exist so create it
            if self.state == 'present':
                changed = True
            else:
                # you can't delete what is not there
                changed = False

        self.results['changed'] = changed
        self.results['state'] = results

        # return the results if you are only gathering information
        if self.check_mode:
            return self.results

        if changed:
            if self.state == "present":
                self.results['state'] = self.create_or_update_ddos_protection_plan(
                    self.module.params)
            elif self.state == "absent":
                # delete DDoS protection plan
                self.delete_ddos_protection_plan()
                self.results['state']['status'] = 'Deleted'

        return self.results

    def create_or_update_ddos_protection_plan(self, params):
        '''
        Create or update DDoS protection plan.
        :return: create or update DDoS protection plan instance state dictionary
        '''
        self.log("create or update DDoS protection plan {0}".format(self.name))
        try:
            poller = self.network_client.ddos_protection_plans.create_or_update(
                resource_group_name=params.get("resource_group"),
                location=self.location,
                ddos_protection_plan_name=params.get("name"),
                tags=self.tags)
            result = self.get_poller_result(poller)
            self.log("Response : {0}".format(result))
        except CloudError as ex:
            self.fail("Failed to create DDoS protection plan {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))
        return ddos_protection_plan_to_dict(result)

    def delete_ddos_protection_plan(self):
        '''
        Deletes specified DDoS protection plan
        :return True
        '''
        self.log("Deleting the DDoS protection plan {0}".format(self.name))
        try:
            poller = self.network_client.ddos_protection_plans.delete(
                self.resource_group, self.name)
            result = self.get_poller_result(poller)
        except CloudError as e:
            self.log('Error attempting to delete DDoS protection plan.')
            self.fail(
                "Error deleting the DDoS protection plan : {0}".format(str(e)))
        return result


def ddos_protection_plan_to_dict(item):
    # turn DDoS protection plan object into a dictionary (serialization)
    ddos_protection_plan = item.as_dict()

    result = dict(
        additional_properties=ddos_protection_plan.get('additional_properties', None),
        id=ddos_protection_plan.get('id', None),
        name=ddos_protection_plan.get('name', None),
        type=ddos_protection_plan.get('type', None),
        location=ddos_protection_plan.get('location', None),
        tags=ddos_protection_plan.get('tags', None),
        etag=ddos_protection_plan.get('etag', None),
        resource_guid=ddos_protection_plan.get('resource_guid', None),
        provisioning_state=ddos_protection_plan.get('provisioning_state', None),
        virtual_networks=ddos_protection_plan.get('virtual_networks', None)
    )
    return result


def main():
    AzureDDoSProtectionPlan()


if __name__ == '__main__':
    main()

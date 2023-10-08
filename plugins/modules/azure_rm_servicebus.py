#!/usr/bin/python
#
# Copyright (c) 2018 Yuwei Zhou, <yuwzho@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_servicebus
version_added: "0.1.2"
short_description: Manage Azure Service Bus
description:
    - Create, update or delete an Azure Service Bus namespaces.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
    name:
        description:
            - Name of the servicebus namespace.
        required: true
    state:
        description:
            - Assert the state of the servicebus. Use C(present) to create or update and use C(absen) to delete.
        default: present
        choices:
            - absent
            - present
    location:
        description:
            - The servicebus's location.
    sku:
        description:
            - Namespace SKU.
        choices:
            - standard
            - basic
            - premium
        default: standard

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Yuwei Zhou (@yuwzho)

'''

EXAMPLES = '''
- name: Create a namespace
  azure_rm_servicebus:
      name: deadbeef
      location: eastus
      tags:
        key1: value1
'''
RETURN = '''
id:
    description:
        - Current state of the service bus.
    returned: success
    type: str
    sample: "/subscriptions/xxx...xxx/resourceGroups/myResourceGroup/providers/Microsoft.ServiceBus/namespaces/myServicebus"
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible.module_utils._text import to_native
from datetime import datetime, timedelta


class AzureRMServiceBus(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            sku=dict(type='str', choices=['basic', 'standard', 'premium'], default='standard')
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.sku = None
        self.location = None

        self.results = dict(
            changed=False,
            id=None
        )

        super(AzureRMServiceBus, self).__init__(self.module_arg_spec,
                                                supports_tags=True,
                                                supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        original = self.get()

        if not original:
            self.check_name()

        if self.state == 'present':
            if not self.check_mode:
                if original:
                    update_tags, new_tags = self.update_tags(original.tags)
                    if update_tags:
                        changed = True
                        self.tags = new_tags
                        original = self.create()
                    else:
                        changed = False
                else:
                    changed = True
                    original = self.create()
            else:
                changed = True
        elif self.state == 'absent' and original:
            changed = True
            original = None
            if not self.check_mode:
                self.delete()
                self.results['deleted'] = True

        if original:
            self.results = self.to_dict(original)
        self.results['changed'] = changed
        return self.results

    def check_name(self):
        try:
            check_name = self.servicebus_client.namespaces.check_name_availability(parameters={'name': self.name})
            if not check_name or not check_name.name_available:
                self.fail("Error creating namespace {0} - {1}".format(self.name, check_name.message or str(check_name)))
        except Exception as exc:
            self.fail("Error creating namespace {0} - {1}".format(self.name, exc.message or str(exc)))

    def create(self):
        self.log('Cannot find namespace, creating a one')
        try:
            sku = self.servicebus_models.SBSku(name=str.capitalize(self.sku))
            poller = self.servicebus_client.namespaces.begin_create_or_update(self.resource_group,
                                                                              self.name,
                                                                              self.servicebus_models.SBNamespace(location=self.location,
                                                                                                                 tags=self.tags,
                                                                                                                 sku=sku))
            ns = self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error creating namespace {0} - {1}'.format(self.name, str(exc.inner_exception) or str(exc)))
        return ns

    def delete(self):
        try:
            self.servicebus_client.namespaces.begin_delete(self.resource_group, self.name)
            return True
        except Exception as exc:
            self.fail("Error deleting route {0} - {1}".format(self.name, str(exc)))

    def get(self):
        try:
            return self.servicebus_client.namespaces.get(self.resource_group, self.name)
        except Exception:
            return None

    def to_dict(self, instance):
        result = dict()
        attribute_map = self.servicebus_models.SBNamespace._attribute_map
        for attribute in attribute_map.keys():
            value = getattr(instance, attribute)
            if not value:
                continue
            if isinstance(value, self.servicebus_models.SBSku):
                result[attribute] = value.name.lower()
            elif isinstance(value, datetime):
                result[attribute] = str(value)
            elif isinstance(value, str):
                result[attribute] = to_native(value)
            elif attribute == 'max_size_in_megabytes':
                result['max_size_in_mb'] = value
            else:
                result[attribute] = value
        return result


def is_valid_timedelta(value):
    if value == timedelta(10675199, 10085, 477581):
        return None
    return value


def main():
    AzureRMServiceBus()


if __name__ == '__main__':
    main()

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
        type: str
    name:
        description:
            - Name of the servicebus namespace.
        required: true
        type: str
    state:
        description:
            - Assert the state of the servicebus. Use C(present) to create or update and use C(absen) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - The servicebus's location.
        type: str
    sku:
        description:
            - Namespace SKU.
        type: str
        choices:
            - standard
            - basic
            - premium
        default: standard
    minimum_tls_version:
        description:
            - The minimum TLS version for the cluster to support.
        type: str
        choices:
            - '1.0'
            - '1.1'
            - '1.2'
    zone_redundant:
        description:
            - Enabling this property creates a Premium Service Bus Namespace in regions supported availability zones.
        type: bool
    disable_local_auth:
        description:
            - This property disables SAS authentication for the Service Bus namespace.
        type: bool
    public_network_access:
        description:
            - This determines if traffic is allowed over public network.
            - By default it is C(Enabled).
        type: str
        default: Enabled
        choices:
            - Enabled
            - Disabled
            - SecuredByPerimeter
    premium_messaging_partitions:
        description:
            - The number of partitions of a Service Bus namespace.
            - This property is only applicable to C(premium) SKU namespaces.
            - It default value is C(1) for C(premium) namespaces.
        type: int
        choices:
            - 1
            - 2
            - 4

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple

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
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.mgmt.servicebus.v2022_10_01_preview.models import (Identity, UserAssignedIdentity)
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible.module_utils._text import to_native
from datetime import datetime, timedelta


class AzureRMServiceBus(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            sku=dict(type='str', choices=['basic', 'standard', 'premium'], default='standard'),
            identity=dict(
                type="dict",
                options=self.managed_identity_multiple_spec
            ),
            minimum_tls_version=dict(type='str', choices=['1.0', '1.1', '1.2']),
            zone_redundant=dict(type='bool'),
            disable_local_auth=dict(type='bool'),
            public_network_access=dict(type='str', default='Enabled', choices=["Enabled", "Disabled", "SecuredByPerimeter"]),
            premium_messaging_partitions=dict(type='int', choices=[1, 2, 4])
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.sku = None
        self.location = None
        self._managed_identity = None
        self.identity = None
        self.update_identity = False
        self.minimum_tls_version = None
        self.zone_redundant = None
        self.disable_local_auth = None
        self.public_network_access = None
        self.premium_messaging_partitions = None

        self.results = dict(
            changed=False,
            id=None
        )

        super(AzureRMServiceBus, self).__init__(self.module_arg_spec,
                                                supports_tags=True,
                                                supports_check_mode=True)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {
                "identity": Identity,
                "user_assigned": UserAssignedIdentity,
            }
        return self._managed_identity

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

        curr_identity = original.identity.as_dict() if original and original.identity else None

        if self.identity:
            self.update_identity, identity_result = self.update_managed_identity(curr_identity=curr_identity,
                                                                                 new_identity=self.identity)
            self.identity = identity_result.as_dict()

        if self.state == 'present':
            if self.sku != 'premium' and self.premium_messaging_partitions is not None:
                self.fail("The premium_messaging_partitions is only applicable to C(premium) SKU namespaces.")

            if not self.check_mode:
                if original:
                    update_tags, new_tags = self.update_tags(original.tags)
                    if update_tags:
                        changed = True
                        self.tags = new_tags
                    if self.update_identity:
                        changed = True
                    if self.minimum_tls_version is not None and self.minimum_tls_version != original.minimum_tls_version:
                        changed = True
                    else:
                        self.minimum_tls_version = original.minimum_tls_version
                    if self.premium_messaging_partitions is not None and self.premium_messaging_partitions != original.premium_messaging_partitions:
                        changed = True
                    else:
                        self.premium_messaging_partitions = original.premium_messaging_partitions
                    if self.public_network_access is not None and self.public_network_access != original.public_network_access:
                        changed = True
                    else:
                        self.public_network_access = original.public_network_access
                    if self.zone_redundant is not None and bool(self.zone_redundant) != bool(original.zone_redundant):
                        # changed = True
                        # self.fail("The zone_redundant is an immutable property")
                        self.log("The default value of zone_redundant is True and cannot be set")
                    else:
                        self.zone_redundant = original.zone_redundant
                    if self.disable_local_auth is not None and bool(self.disable_local_auth) != bool(original.disable_local_auth):
                        changed = True
                    else:
                        self.disable_local_auth = original.disable_local_auth
                    if changed:
                        original = self.create()
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
            parameters = self.servicebus_models.SBNamespace(location=self.location,
                                                            tags=self.tags,
                                                            sku=sku,
                                                            minimum_tls_version=self.minimum_tls_version,
                                                            zone_redundant=self.zone_redundant,
                                                            disable_local_auth=self.disable_local_auth,
                                                            public_network_access=self.public_network_access,
                                                            premium_messaging_partitions=self.premium_messaging_partitions,
                                                            identity=self.identity)
            poller = self.servicebus_client.namespaces.begin_create_or_update(self.resource_group, self.name, parameters)
            ns = self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error creating namespace {0} - {1}'.format(self.name, str(exc)))
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
            elif isinstance(value, Identity):
                result['identity'] = value.as_dict()
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

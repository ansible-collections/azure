#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_managedapplication_info
version_added: "4.3.0"
short_description: Get Azure managed application facts
description:
    - Get facts of an Azure managed application, or list managed applications in a resource group or subscription.
options:
    resource_group:
        description:
            - Name of the resource group.
            - Required when I(name) is set.
        type: str
    name:
        description:
            - Name of the managed application.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get a managed application
  azure_rm_managedapplication_info:
    resource_group: myResourceGroup
    name: myManagedApplication

- name: List managed applications in a resource group
  azure_rm_managedapplication_info:
    resource_group: myResourceGroup

- name: List managed applications in the subscription filtered by tag
  azure_rm_managedapplication_info:
    tags:
      - environment:test
'''

RETURN = '''
managed_applications:
    description:
        - List of managed applications.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - Resource ID of the managed application.
            type: str
            returned: always
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Solutions/applications/myManagedApplication"
        name:
            description:
                - Name of the managed application.
            type: str
            returned: always
            sample: myManagedApplication
        resource_group:
            description:
                - Name of the resource group that contains the managed application.
            type: str
            returned: always
            sample: myResourceGroup
        type:
            description:
                - Resource type.
            type: str
            returned: always
            sample: Microsoft.Solutions/applications
        location:
            description:
                - Resource location.
            type: str
            returned: always
            sample: eastus
        kind:
            description:
                - The kind of the managed application.
            type: str
            returned: always
            sample: ServiceCatalog
        managed_resource_group_id:
            description:
                - Resource ID of the managed resource group.
            type: str
            returned: always
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myManagedResourceGroup"
        application_definition_id:
            description:
                - Resource ID of the managed application definition.
            type: str
            returned: when the application kind is C(ServiceCatalog)
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Solutions/applicationDefinitions/myDefinition"
        plan:
            description:
                - The Azure Marketplace plan of the managed application.
            type: dict
            returned: when the application kind is C(MarketPlace)
            sample: {"name": "myPlan", "publisher": "myPublisher", "product": "myProduct", "version": "1.0.0"}
        parameters:
            description:
                - Parameters of the main template, as returned by Azure.
            type: dict
            returned: always
            sample: {"storageAccountNamePrefix": {"type": "String", "value": "mystorage"}}
        outputs:
            description:
                - Outputs of the main template.
            type: dict
            returned: always
            sample: {"storageEndpoint": {"type": "String", "value": "https://mystorage.blob.core.windows.net/"}}
        provisioning_state:
            description:
                - Provisioning state of the managed application.
            type: str
            returned: always
            sample: Succeeded
        management_mode:
            description:
                - Management mode of the managed application.
            type: str
            returned: always
            sample: Managed
        tags:
            description:
                - Resource tags.
            type: dict
            returned: always
            sample: {"environment": "test"}
'''  # NOQA

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
    from azure.mgmt.core.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagedApplicationInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
            managed_applications=[]
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureRMManagedApplicationInfo, self).__init__(self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False,
                                                            facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            if not self.resource_group:
                self.fail('resource_group is required when name is set')
            item = self.get_application()
            response = [item] if item else []
        elif self.resource_group:
            response = self.list_by_resource_group()
        else:
            response = self.list_by_subscription()

        self.results['managed_applications'] = [self.to_dict(x) for x in response if self.has_tags(x.tags, self.tags)]
        return self.results

    def get_application(self):
        try:
            return self.managedapplication_client.applications.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            return None
        except HttpResponseError as exc:
            self.fail('Error getting managed application {0} - {1}'.format(self.name, str(exc)))

    def list_by_resource_group(self):
        try:
            return list(self.managedapplication_client.applications.list_by_resource_group(self.resource_group))
        except HttpResponseError as exc:
            self.fail('Error listing managed applications in resource group {0} - {1}'.format(self.resource_group, str(exc)))

    def list_by_subscription(self):
        try:
            return list(self.managedapplication_client.applications.list_by_subscription())
        except HttpResponseError as exc:
            self.fail('Error listing managed applications in subscription - {0}'.format(str(exc)))

    def to_dict(self, application):
        result = application.as_dict()
        result['resource_group'] = parse_resource_id(result['id'])['resource_group']
        return result


def main():
    AzureRMManagedApplicationInfo()


if __name__ == '__main__':
    main()

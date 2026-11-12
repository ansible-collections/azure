#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_managedapplication
version_added: "4.3.0"
short_description: Manage Azure managed applications
description:
    - Create, update or delete an Azure managed application.
    - Supports applications deployed from Azure Marketplace and from a service catalog application definition.
options:
    resource_group:
        description:
            - Name of the resource group that contains the managed application.
        required: true
        type: str
    name:
        description:
            - Name of the managed application.
        required: true
        type: str
    state:
        description:
            - Assert the state of the managed application. Use C(present) to create or update and C(absent) to delete.
            - Deleting a managed application also deletes its managed resource group.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Resource location.
            - Defaults to the location of I(resource_group) on create, and to the existing location on update.
            - Cannot be changed after creation.
        type: str
    kind:
        description:
            - The kind of the managed application.
            - Use C(MarketPlace) for an application from Azure Marketplace, which requires I(plan).
            - Use C(ServiceCatalog) for an application from a service catalog definition, which requires I(application_definition_id).
            - Required when I(state=present). Cannot be changed after creation.
        type: str
        choices:
            - MarketPlace
            - ServiceCatalog
    managed_resource_group_id:
        description:
            - Resource ID of the managed resource group, for example C(/subscriptions/xxx/resourceGroups/myManagedResourceGroup).
            - Azure creates this resource group when the managed application is created.
            - Required when I(state=present). Cannot be changed after creation.
        type: str
    application_definition_id:
        description:
            - Resource ID of the managed application definition.
            - Required when I(kind=ServiceCatalog).
        type: str
    plan:
        description:
            - The Azure Marketplace plan of the managed application.
            - Required when I(kind=MarketPlace).
        type: dict
        suboptions:
            name:
                description:
                    - The plan name.
                type: str
                required: true
            publisher:
                description:
                    - The publisher ID.
                type: str
                required: true
            product:
                description:
                    - The product code.
                type: str
                required: true
            version:
                description:
                    - The plan version.
                type: str
                required: true
            promotion_code:
                description:
                    - The promotion code.
                type: str
    parameters:
        description:
            - Parameters for the main template of the managed application, in ARM template parameter format.
            - 'For example C({"adminUsername": {"value": "azureuser"}}).'
            - Parameters that Azure does not return, such as C(secureString) and C(secureObject) parameters,
              and parameters given without a C(value) key are not compared for idempotence.
            - Any change, including a I(tags) change, resubmits the managed application with these parameters,
              so include every required parameter, including secure ones, on each run.
        type: dict
notes:
    - This module does not accept Azure Marketplace terms. Accept the offer terms before creating a C(MarketPlace) managed application.
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a managed application from a service catalog definition
  azure_rm_managedapplication:
    resource_group: myResourceGroup
    name: myManagedApplication
    kind: ServiceCatalog
    application_definition_id: >-
      /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Solutions/applicationDefinitions/myDefinition
    managed_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myManagedResourceGroup"
    parameters:
      storageAccountNamePrefix:
        value: mystorage
    tags:
      environment: test

- name: Create a managed application from Azure Marketplace
  azure_rm_managedapplication:
    resource_group: myResourceGroup
    name: myMarketplaceApplication
    location: eastus
    kind: MarketPlace
    managed_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myMarketplaceManagedResourceGroup"
    plan:
      name: myPlan
      publisher: myPublisher
      product: myProduct
      version: 1.0.0
    parameters:
      adminPassword:
        value: "{{ admin_password }}"
      location:
        value: eastus

- name: Delete a managed application
  azure_rm_managedapplication:
    resource_group: myResourceGroup
    name: myManagedApplication
    state: absent
'''  # NOQA

RETURN = '''
id:
    description:
        - Resource ID of the managed application.
    type: str
    returned: when I(state=present)
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Solutions/applications/myManagedApplication"
name:
    description:
        - Name of the managed application.
    type: str
    returned: when I(state=present)
    sample: myManagedApplication
type:
    description:
        - Resource type.
    type: str
    returned: when I(state=present)
    sample: Microsoft.Solutions/applications
location:
    description:
        - Resource location.
    type: str
    returned: when I(state=present)
    sample: eastus
kind:
    description:
        - The kind of the managed application.
    type: str
    returned: when I(state=present)
    sample: ServiceCatalog
managed_resource_group_id:
    description:
        - Resource ID of the managed resource group.
    type: str
    returned: when I(state=present)
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myManagedResourceGroup"
application_definition_id:
    description:
        - Resource ID of the managed application definition.
    type: str
    returned: when I(state=present) and I(kind=ServiceCatalog)
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Solutions/applicationDefinitions/myDefinition"
plan:
    description:
        - The Azure Marketplace plan of the managed application.
    type: dict
    returned: when I(state=present) and I(kind=MarketPlace)
    sample: {"name": "myPlan", "publisher": "myPublisher", "product": "myProduct", "version": "1.0.0"}
parameters:
    description:
        - Parameters of the main template, as returned by Azure.
    type: dict
    returned: when I(state=present)
    sample: {"storageAccountNamePrefix": {"type": "String", "value": "mystorage"}}
outputs:
    description:
        - Outputs of the main template.
    type: dict
    returned: when I(state=present)
    sample: {"storageEndpoint": {"type": "String", "value": "https://mystorage.blob.core.windows.net/"}}
provisioning_state:
    description:
        - Provisioning state of the managed application.
    type: str
    returned: when I(state=present)
    sample: Succeeded
management_mode:
    description:
        - Management mode of the managed application.
    type: str
    returned: when I(state=present)
    sample: Managed
tags:
    description:
        - Resource tags.
    type: dict
    returned: when I(state=present)
    sample: {"environment": "test"}
'''  # NOQA

import copy

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagedApplication(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            kind=dict(type='str', choices=['MarketPlace', 'ServiceCatalog']),
            managed_resource_group_id=dict(type='str'),
            application_definition_id=dict(type='str'),
            plan=dict(
                type='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    publisher=dict(type='str', required=True),
                    product=dict(type='str', required=True),
                    version=dict(type='str', required=True),
                    promotion_code=dict(type='str'),
                )
            ),
            parameters=dict(type='dict'),
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.kind = None
        self.managed_resource_group_id = None
        self.application_definition_id = None
        self.plan = None
        self.parameters = None
        self.tags = None

        self.results = dict(changed=False)

        required_if = [
            ('state', 'present', ['kind', 'managed_resource_group_id']),
            ('kind', 'MarketPlace', ['plan']),
            ('kind', 'ServiceCatalog', ['application_definition_id']),
        ]

        super(AzureRMManagedApplication, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=True,
                                                        required_if=required_if)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        old_application = self.get_application()

        if self.state == 'present':
            if not old_application:
                if not self.location:
                    self.location = self.get_resource_group(self.resource_group).location
                changed = True
            else:
                if self.kind.lower() != (old_application.kind or '').lower():
                    self.fail('The kind of managed application {0} cannot be changed from {1} to {2}'.format(self.name, old_application.kind, self.kind))
                if not self.location:
                    self.location = old_application.location
                tags_changed, self.tags = self.update_tags(old_application.tags)
                desired = self.build_application().as_dict()
                desired['parameters'] = self.comparable_parameters(old_application.parameters)
                changed = tags_changed or not self.default_compare({}, desired, old_application.as_dict(), '', dict(compare=[]))
        elif old_application:
            changed = True

        self.results['changed'] = changed

        if self.check_mode or not changed:
            if old_application:
                self.results.update(old_application.as_dict())
            return self.results

        if self.state == 'present':
            self.results.update(self.create_or_update_application(self.build_application()).as_dict())
        else:
            self.delete_application()
        return self.results

    def comparable_parameters(self, existing_parameters):
        if self.parameters is None:
            return None
        existing_parameters = existing_parameters or {}
        comparable = {}
        for key, value in self.parameters.items():
            current = existing_parameters.get(key)
            if not isinstance(value, dict) or 'value' not in value:
                continue
            if not isinstance(current, dict) or 'value' not in current:
                continue
            if str(current.get('type', '')).lower().startswith('secure'):
                continue
            comparable[key] = copy.deepcopy(value)
        return comparable

    def build_application(self):
        models = self.managedapplication_models
        plan = None
        if self.plan:
            plan = models.Plan(name=self.plan['name'],
                               publisher=self.plan['publisher'],
                               product=self.plan['product'],
                               version=self.plan['version'],
                               promotion_code=self.plan.get('promotion_code'))
        return models.Application(location=self.location,
                                  tags=self.tags,
                                  kind=self.kind,
                                  managed_resource_group_id=self.managed_resource_group_id,
                                  application_definition_id=self.application_definition_id,
                                  plan=plan,
                                  parameters=self.parameters)

    def get_application(self):
        try:
            return self.managedapplication_client.applications.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            return None
        except HttpResponseError as exc:
            self.fail('Error getting managed application {0} - {1}'.format(self.name, str(exc)))

    def create_or_update_application(self, application):
        try:
            poller = self.managedapplication_client.applications.begin_create_or_update(self.resource_group,
                                                                                        self.name,
                                                                                        application)
            return self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error creating or updating managed application {0} - {1}'.format(self.name, str(exc)))

    def delete_application(self):
        try:
            poller = self.managedapplication_client.applications.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error deleting managed application {0} - {1}'.format(self.name, str(exc)))


def main():
    AzureRMManagedApplication()


if __name__ == '__main__':
    main()

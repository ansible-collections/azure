#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_apimanagementproduct
version_added: "4.2.0"
short_description: Manage a product in an Azure API Management service
description:
    - Create, update and delete a product in an Azure API Management service.
    - Products group one or more APIs, and control developer visibility,
      subscription and terms of use.
    - The API Management service is managed with
      M(azure.azcollection.azure_rm_apimanagementservice), the APIs with
      M(azure.azcollection.azure_rm_apimanagement).
options:
    resource_group:
        description:
            - Name of the resource group containing the API Management service.
        required: true
        type: str
    service_name:
        description:
            - Name of the API Management service.
        required: true
        type: str
    product_id:
        description:
            - Product identifier. Must be unique in the current API Management
              service instance.
        required: true
        type: str
    display_name:
        description:
            - Product name. Required when creating the product.
        type: str
    description:
        description:
            - Product description. May include HTML formatting tags.
        type: str
    terms:
        description:
            - Product terms of use. Developers trying to subscribe to the
              product will be presented and required to accept these terms
              before they can complete the subscription process.
        type: str
    product_state:
        description:
            - Whether the product is published or not.
            - Published products are visible to developers in the developer
              portal, not published ones only to administrators.
        type: str
        choices:
            - published
            - notPublished
    subscription_required:
        description:
            - Whether a product subscription is required for accessing APIs
              included in this product.
            - If C(true), the product is protected and a valid subscription
              key is required; if C(false), the product is open.
        type: bool
    approval_required:
        description:
            - Whether subscription approval is required. If C(false), new
              subscriptions are approved automatically.
            - Only valid when I(subscription_required=true).
        type: bool
    subscriptions_limit:
        description:
            - The number of subscriptions a user can have to this product at
              the same time. Leave unset to allow unlimited subscriptions.
            - Only valid when I(subscription_required=true).
        type: int
    apis:
        description:
            - Identifiers of the APIs included in this product.
            - When set, the module reconciles the product's API associations
              to exactly this list; APIs not listed are removed from the
              product (they remain in the service).
            - When omitted, the existing API associations are left untouched.
        type: list
        elements: str
    state:
        description:
            - Assert the state of the product. Use C(present) to create or
              update, C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent
notes:
    - On update, fields that are omitted are carried forward from the existing
      product.
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a published, open product containing two APIs
  azure.azcollection.azure_rm_apimanagementproduct:
    resource_group: myResourceGroup
    service_name: myService
    product_id: starter
    display_name: Starter
    description: Free tier with rate limiting
    product_state: published
    subscription_required: false
    apis:
      - echo-api
      - status-api

- name: Publish a protected product requiring approved subscriptions
  azure.azcollection.azure_rm_apimanagementproduct:
    resource_group: myResourceGroup
    service_name: myService
    product_id: premium
    display_name: Premium
    terms: Terms and conditions for the premium tier
    product_state: published
    subscription_required: true
    approval_required: true
    subscriptions_limit: 1

- name: Remove an API from the product
  azure.azcollection.azure_rm_apimanagementproduct:
    resource_group: myResourceGroup
    service_name: myService
    product_id: starter
    apis:
      - echo-api

- name: Delete a product
  azure.azcollection.azure_rm_apimanagementproduct:
    resource_group: myResourceGroup
    service_name: myService
    product_id: starter
    state: absent
'''

RETURN = '''
product:
    description:
        - The product definition.
        - When I(apis) is set, also holds the reconciled list of API identifiers.
    returned: when I(state=present)
    type: dict
    sample: {
        "name": "starter",
        "display_name": "Starter",
        "product_state": "published",
        "subscription_required": false,
        "apis": ["echo-api"]
    }
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.apimanagement import ApiManagementClient
    from azure.mgmt.apimanagement.models import ProductContract
except ImportError:
    pass

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

# Fields Azure fills on its own on read.
READ_ONLY_FIELDS = ('id', 'name', 'type')


class AzureRMApiManagementProduct(AzureRMModuleBaseExt):
    """Manage a product in an API Management service."""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            service_name=dict(type='str', required=True),
            product_id=dict(type='str', required=True),
            display_name=dict(type='str'),
            description=dict(type='str'),
            terms=dict(type='str'),
            product_state=dict(type='str', choices=['published', 'notPublished']),
            subscription_required=dict(type='bool'),
            approval_required=dict(type='bool'),
            subscriptions_limit=dict(type='int'),
            apis=dict(type='list', elements='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.service_name = None
        self.product_id = None
        self.display_name = None
        self.description = None
        self.terms = None
        self.product_state = None
        self.subscription_required = None
        self.approval_required = None
        self.subscriptions_limit = None
        self.apis = None
        self.state = None

        self.results = dict(changed=False)
        self.apim_client = None

        super(AzureRMApiManagementProduct, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.apim_client = self.get_mgmt_svc_client(
            ApiManagementClient, base_url=self._cloud_environment.endpoints.resource_manager)

        existing = self.get_resource()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_resource()
            return self.results

        if existing is None:
            if self.display_name is None:
                self.fail("display_name is required to create product '{0}' in service "
                          "'{1}'".format(self.product_id, self.service_name))
            body = self._build_body()
            self.results['changed'] = True
            if not self.check_mode:
                self.results['product'] = self.create_update_resource(body, create=True)
            else:
                self.results['product'] = self._finalize(self._format_body(body))
        else:
            # Update: carry forward readable fields the user omitted, then
            # compare against the fetched state.
            body = self._merge_existing(existing)
            if not self._is_current(body, existing):
                self.results['changed'] = True
                if not self.check_mode:
                    self.results['product'] = self.create_update_resource(body, create=False)
                else:
                    self.results['product'] = self._finalize(self._format_body(body))
            else:
                self.results['product'] = existing

        # Reconcile the product's API associations when apis is supplied.
        if self.apis is not None:
            if not self.check_mode:
                if self._reconcile_apis():
                    self.results['changed'] = True
                # Report the associations as they are now.
                self.results['product'] = self.get_resource() or self.results.get('product')
                self.results['product']['apis'] = self._list_api_ids()
            else:
                current = self._list_api_ids()
                if set(current) != set(self.apis):
                    self.results['changed'] = True
                self.results['product']['apis'] = sorted(self.apis)
        elif 'product' in self.results and self.results['product'] is not None:
            # Do not touch the associations when apis is omitted, but report
            # the current ones for convenience.
            self.results['product']['apis'] = self._list_api_ids()

        # Present the ARM 'state' property under the module option name.
        if self.state == 'present' and self.results.get('product') is not None:
            item = self.results['product']
            if item.get('state') is not None:
                item['product_state'] = item.pop('state')

        return self.results

    def get_resource(self):
        try:
            response = self.apim_client.product.get(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                product_id=self.product_id,
            )
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving product {0}: {1}".format(self.product_id, str(exc)))
        return self.format_item(response)

    def create_update_resource(self, body, create):
        self.log("Creating / updating product {0}".format(self.product_id))
        try:
            response = self.apim_client.product.create_or_update(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                product_id=self.product_id,
                parameters=ProductContract(**body),
                if_match=None if create else '*',
            )
        except Exception as exc:
            self.fail("Error creating / updating product {0}: {1}".format(self.product_id, str(exc)))
        return self.format_item(response)

    def delete_resource(self):
        self.log("Deleting product {0}".format(self.product_id))
        try:
            self.apim_client.product.delete(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                product_id=self.product_id,
                if_match='*',
            )
        except Exception as exc:
            self.fail("Error deleting product {0}: {1}".format(self.product_id, str(exc)))
        return True

    def _build_body(self):
        """Wire body holding the user-supplied (non C(None)) options."""
        body = dict()
        if self.display_name is not None:
            body['display_name'] = self.display_name
        if self.description is not None:
            body['description'] = self.description
        if self.terms is not None:
            body['terms'] = self.terms
        if self.product_state is not None:
            body['state'] = self.product_state
        if self.subscription_required is not None:
            body['subscription_required'] = self.subscription_required
        if self.approval_required is not None:
            body['approval_required'] = self.approval_required
        if self.subscriptions_limit is not None:
            body['subscriptions_limit'] = self.subscriptions_limit
        return body

    def _merge_existing(self, existing):
        """Full-replace PUT body: carry forward fields the user omitted."""
        body = {k: copy.deepcopy(v) for k, v in existing.items()
                if k not in READ_ONLY_FIELDS and k != 'apis' and v is not None}
        body.update(self._build_body())
        return body

    def _is_current(self, body, existing):
        result = dict(compare=[])
        return self.default_compare({}, copy.deepcopy(body), existing, '', result)

    def _reconcile_apis(self):
        """Align the product's API associations with self.apis. Returns changed."""
        current = set(self._list_api_ids())
        desired = set(self.apis)
        changed = False
        for api_id in desired - current:
            changed = True
            try:
                self.apim_client.product_api.create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.service_name,
                    product_id=self.product_id,
                    api_id=api_id,
                )
            except Exception as exc:
                self.fail("Error adding api {0} to product {1}: {2}".format(api_id, self.product_id, str(exc)))
        for api_id in current - desired:
            changed = True
            try:
                self.apim_client.product_api.delete(
                    resource_group_name=self.resource_group,
                    service_name=self.service_name,
                    product_id=self.product_id,
                    api_id=api_id,
                )
            except Exception as exc:
                self.fail("Error removing api {0} from product {1}: {2}".format(api_id, self.product_id, str(exc)))
        return changed

    def _list_api_ids(self):
        try:
            return [api.name for api in self.apim_client.product_api.list_by_product(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                product_id=self.product_id,
            )]
        except ResourceNotFoundError:
            # The product does not exist (yet), e.g. in check mode on create.
            return []
        except Exception as exc:
            self.fail("Error listing apis of product {0}: {1}".format(self.product_id, str(exc)))

    def _format_body(self, body):
        # Check mode: shape the wire body like a fetched resource.
        item = copy.deepcopy(body)
        item['name'] = self.product_id
        return item

    def format_item(self, item):
        if item is None:
            return None
        return self._finalize(as_attribute_dict(item, exclude_readonly=False))

    def _finalize(self, normalized):
        if normalized is None:
            return None
        normalized['resource_group'] = self.resource_group
        normalized['service_name'] = self.service_name
        normalized['name'] = normalized.get('name') or self.product_id
        return normalized


def main():
    AzureRMApiManagementProduct()


if __name__ == '__main__':
    main()

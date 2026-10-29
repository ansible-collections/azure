#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_apimanagementproduct_info
version_added: "4.2.0"
short_description: Get products in an Azure API Management service
description:
    - Get details of a single product, or list all products in an Azure API
      Management service.
    - Every returned product includes the identifiers of the APIs associated
      with it in I(apis).
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
            - Identifier of a specific product to fetch. If omitted, all
              products of the service are listed.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get a specific product
  azure.azcollection.azure_rm_apimanagementproduct_info:
    resource_group: myResourceGroup
    service_name: myService
    product_id: starter
  register: product

- name: List all products of the service
  azure.azcollection.azure_rm_apimanagementproduct_info:
    resource_group: myResourceGroup
    service_name: myService
  register: products
'''

RETURN = '''
products:
    description:
        - List of products.
        - Each product includes the identifiers of its associated APIs in I(apis).
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "name": "starter",
            "display_name": "Starter",
            "product_state": "published",
            "subscription_required": false,
            "apis": ["echo-api"]
        }
    ]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.apimanagement import ApiManagementClient
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMApiManagementProductInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            service_name=dict(type='str', required=True),
            product_id=dict(type='str'),
        )

        self.resource_group = None
        self.service_name = None
        self.product_id = None

        self.results = dict(
            changed=False,
            products=[],
        )

        super(AzureRMApiManagementProductInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.apim_client = self.get_mgmt_svc_client(
            ApiManagementClient, base_url=self._cloud_environment.endpoints.resource_manager)

        if self.product_id:
            items = self._get()
        else:
            items = self._list()

        self.results['products'] = [self._format(item, with_apis=True) for item in items]
        return self.results

    def _get(self):
        try:
            return [self.apim_client.product.get(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                product_id=self.product_id,
            )]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error retrieving product {0}: {1}".format(self.product_id, str(exc)))

    def _list(self):
        try:
            return list(self.apim_client.product.list_by_service(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
            ))
        except Exception as exc:
            self.fail("Error listing products of service {0}: {1}".format(self.service_name, str(exc)))

    def _format(self, item, with_apis):
        normalized = as_attribute_dict(item, exclude_readonly=False) if item else None
        if normalized is None:
            return None
        normalized['resource_group'] = self.resource_group
        normalized['service_name'] = self.service_name
        normalized['name'] = normalized.get('name')
        # Present the ARM 'state' property under the module option name.
        if normalized.get('state') is not None:
            normalized['product_state'] = normalized.pop('state')
        if with_apis:
            normalized['apis'] = self._list_api_ids(normalized['name'])
        return normalized

    def _list_api_ids(self, product_id):
        try:
            return [api.name for api in self.apim_client.product_api.list_by_product(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                product_id=product_id,
            )]
        except Exception as exc:
            self.fail("Error listing apis of product {0}: {1}".format(product_id, str(exc)))


def main():
    AzureRMApiManagementProductInfo()


if __name__ == '__main__':
    main()

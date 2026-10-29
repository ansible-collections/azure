#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_subscriptiondeployment_info
version_added: "4.2.0"
short_description: Get Azure Resource Manager template deployment facts at subscription scope
description:
    - Get facts of a specific subscription-scope deployment, or list all subscription-scope deployments in the subscription.
options:
    name:
        description:
            - The name of the deployment.
            - If not set, all subscription-scope deployments in the subscription are listed.
        type: str
        aliases:
            - deployment_name
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
- name: Get a subscription-scope deployment
  azure.azcollection.azure_rm_subscriptiondeployment_info:
    name: create-rg-deployment

- name: List subscription-scope deployments filtered by tag
  azure.azcollection.azure_rm_subscriptiondeployment_info:
    tags:
      - environment:test
'''

RETURN = '''
deployments:
    description:
        - A list of subscription-scope deployments.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - The resource ID of the deployment.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Resources/deployments/create-rg-deployment
        name:
            description:
                - The name of the deployment.
            returned: always
            type: str
            sample: create-rg-deployment
        type:
            description:
                - The resource type.
            returned: always
            type: str
            sample: Microsoft.Resources/deployments
        location:
            description:
                - The location of the deployment data.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - The tags of the deployment.
            returned: always
            type: dict
            sample: { "environment": "test" }
        properties:
            description:
                - The deployment properties.
            returned: always
            type: complex
            contains:
                provisioning_state:
                    description:
                        - The provisioning state of the deployment.
                    returned: always
                    type: str
                    sample: Succeeded
                correlation_id:
                    description:
                        - The correlation ID of the deployment.
                    returned: always
                    type: str
                    sample: 2fd1a0b2-5c7e-4f19-9a6c-0a3c7e9d1b1e
                timestamp:
                    description:
                        - The timestamp of the template deployment.
                    returned: always
                    type: str
                    sample: "2026-10-13T07:00:00.123456Z"
                duration:
                    description:
                        - The duration of the template deployment.
                    returned: always
                    type: str
                    sample: PT12.345S
                mode:
                    description:
                        - The deployment mode.
                    returned: always
                    type: str
                    sample: Incremental
                outputs:
                    description:
                        - The outputs of the deployment.
                    returned: when the template defines outputs
                    type: dict
                    sample: { "rgId": { "type": "String", "value": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup" } }
                parameters:
                    description:
                        - The deployment parameters, including their types. Values of secure parameters are not returned.
                    returned: always
                    type: dict
                    sample: { "rgName": { "type": "String", "value": "myResourceGroup" } }
                template_link:
                    description:
                        - The reference to the deployed template.
                    returned: when the deployment uses a linked template
                    type: dict
                    sample: { "uri": "https://example.com/templates/azuredeploy.json", "content_version": "1.0.0.0" }
                parameters_link:
                    description:
                        - The reference to the parameters file.
                    returned: when the deployment uses a parameters file
                    type: dict
                    sample: { "uri": "https://example.com/templates/azuredeploy.parameters.json" }
                template_hash:
                    description:
                        - The hash produced for the template.
                    returned: always
                    type: str
                    sample: "11223344556677889900"
                output_resources:
                    description:
                        - The list of resources created by the deployment.
                    returned: always
                    type: list
                    sample: [{ "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup" }]
                dependencies:
                    description:
                        - The list of deployment dependencies.
                    returned: always
                    type: list
                    sample: []
                providers:
                    description:
                        - The list of resource providers needed for the deployment.
                    returned: always
                    type: list
                    sample: [{ "namespace": "Microsoft.Resources", "resource_types": [{ "locations": ["eastus"], "resource_type": "resourceGroups" }] }]
                debug_setting:
                    description:
                        - The debug setting of the deployment.
                    returned: when set
                    type: dict
                    sample: { "detail_level": "RequestContent, ResponseContent" }
                on_error_deployment:
                    description:
                        - The deployment on error behavior.
                    returned: when set
                    type: dict
                    sample: { "type": "LastSuccessful", "deployment_name": "previous-deployment", "provisioning_state": "Succeeded" }
                error:
                    description:
                        - The deployment error.
                    returned: when the deployment failed
                    type: dict
                    sample: { "code": "DeploymentFailed", "message": "At least one resource deployment operation failed." }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSubscriptionDeploymentInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', aliases=['deployment_name']),
            tags=dict(type='list', elements='str'),
        )

        self.name = None
        self.tags = None

        self.results = dict(changed=False)

        super(AzureRMSubscriptionDeploymentInfo, self).__init__(self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=False,
                                                                facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            results = self.get_item()
        else:
            results = self.list_items()

        self.results['deployments'] = [item for item in results if self.has_tags(item.get('tags'), self.tags)]

        return self.results

    def get_item(self):
        try:
            item = self.rm_client.deployments.get_at_subscription_scope(self.name)
        except ResourceNotFoundError:
            return []
        except HttpResponseError as exc:
            self.fail("Failed to get subscription deployment {0} - {1}".format(self.name, str(exc)))
        return [as_attribute_dict(item, exclude_readonly=False)]

    def list_items(self):
        try:
            response = self.rm_client.deployments.list_at_subscription_scope()
            return [as_attribute_dict(item, exclude_readonly=False) for item in response]
        except HttpResponseError as exc:
            self.fail("Failed to list subscription deployments - {0}".format(str(exc)))


def main():
    AzureRMSubscriptionDeploymentInfo()


if __name__ == '__main__':
    main()

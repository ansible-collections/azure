#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_subscriptiondeployment
version_added: "4.2.0"
short_description: Manage Azure Resource Manager template deployments at subscription scope
description:
    - Create, update and delete an Azure Resource Manager (ARM) template deployment at subscription scope.
    - Use M(azure.azcollection.azure_rm_deployment) for template deployments scoped to a resource group.
    - Subscription-scope deployments always use the C(Incremental) deployment mode.
    - Deleting a deployment removes only the deployment record. Resources created by the template are not deleted.
    - The module waits for the deployment to finish. Use the Ansible C(async) keyword to run long deployments in the background.
options:
    name:
        description:
            - The name of the deployment.
        type: str
        required: true
        aliases:
            - deployment_name
    location:
        description:
            - The location to store the deployment data.
            - Required when I(state=present).
            - The location of an existing deployment cannot be changed.
        type: str
    template:
        description:
            - The template content, as a dictionary. A JSON string is also accepted.
            - Mutually exclusive with I(template_link).
            - One of I(template) or I(template_link) is required when I(state=present).
        type: dict
    template_link:
        description:
            - Reference to the template to deploy.
            - Mutually exclusive with I(template).
        type: dict
        suboptions:
            uri:
                description:
                    - The URI of the template to deploy.
                    - Mutually exclusive with I(id). One of I(uri) or I(id) is required.
                type: str
            id:
                description:
                    - The resource ID of a template spec version to deploy.
                    - Mutually exclusive with I(uri). One of I(uri) or I(id) is required.
                type: str
            relative_path:
                description:
                    - Deploys a linked template at a location relative to the parent template.
                    - If the parent template was linked with a template spec, this references an artifact in the template spec.
                    - If the parent template was linked with a URI, the child deployment combines the parent URI and I(relative_path).
                type: str
            content_version:
                description:
                    - If set, must match the C(contentVersion) of the template.
                type: str
            query_string:
                description:
                    - The query string, for example a SAS token, to use with I(uri).
                    - Not compared when deciding whether to redeploy.
                type: str
    parameters:
        description:
            - The deployment parameters, as a dictionary of parameter name to parameter definition. A JSON string is also accepted.
            - Each parameter definition is a dictionary with either a C(value) key, or a C(reference) key that points to a Key Vault secret.
            - A C(reference) requires C(keyVault.id) and C(secretName), and optionally accepts C(secretVersion).
            - Parameters of type C(securestring) or C(secureobject) and Key Vault references are not compared when deciding whether to redeploy,
              because Azure does not return their values.
            - Only parameters set in I(parameters) are compared. Removing a parameter so that the template default applies does not trigger a redeployment.
            - Values are visible in task output and logs. Pass secret values in I(secure_parameters) or as Key Vault references instead.
            - Mutually exclusive with I(parameters_link).
        type: dict
    secure_parameters:
        description:
            - Deployment parameters that hold secret values, in the same format as I(parameters).
            - Merged with I(parameters) when deploying. Values are hidden from task output and logs.
            - Not compared when deciding whether to redeploy for parameters of type C(securestring) or C(secureobject),
              because Azure does not return their values. Change another option or the deployment name to apply a new secret value.
            - A parameter name cannot be set in both I(parameters) and I(secure_parameters).
            - Mutually exclusive with I(parameters_link).
        type: dict
    parameters_link:
        description:
            - Reference to a parameters file.
            - Mutually exclusive with I(parameters).
        type: dict
        suboptions:
            uri:
                description:
                    - The URI of the parameters file.
                type: str
                required: true
            content_version:
                description:
                    - If set, must match the C(contentVersion) of the parameters file.
                type: str
    debug_setting:
        description:
            - The debug setting of the deployment.
            - If not set, the existing debug setting of the deployment is kept when it is updated.
        type: dict
        suboptions:
            detail_level:
                description:
                    - The type of information to log for debugging.
                    - Permitted values are C(none), C(requestContent), C(responseContent), or C(requestContent,responseContent).
                    - Azure defaults to C(none) when not set. Use C(none) to remove an existing debug setting.
                    - Logging request or response content may expose sensitive data retrieved through the deployment operations.
                type: str
    on_error_deployment:
        description:
            - The deployment to run when this deployment fails.
            - If not set, the existing on error behavior of the deployment is kept when it is updated.
            - Set to an empty dictionary to remove an existing on error behavior.
        type: dict
        suboptions:
            type:
                description:
                    - The deployment on error behavior.
                type: str
                choices:
                    - LastSuccessful
                    - SpecificDeployment
            deployment_name:
                description:
                    - The deployment to use when I(type=SpecificDeployment).
                type: str
    expression_evaluation_options:
        description:
            - Specifies whether template expressions are evaluated within the scope of the parent template or nested template.
            - Only applicable to nested templates. Azure defaults to the outer scope when not set.
            - Not returned by Azure, so it cannot be kept from the existing deployment. Set it on every run that relies on it.
            - Changing only this option does not trigger a redeployment.
        type: dict
        suboptions:
            scope:
                description:
                    - The scope used to evaluate parameters, variables and functions in a nested template.
                type: str
                choices:
                    - NotSpecified
                    - Outer
                    - Inner
    state:
        description:
            - Assert the state of the deployment. Use C(present) to create or update and C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Deploy a subscription-scope template that creates a resource group
  azure.azcollection.azure_rm_subscriptiondeployment:
    name: create-rg-deployment
    location: eastus
    template:
      $schema: "https://schema.management.azure.com/schemas/2018-05-01/subscriptionDeploymentTemplate.json#"
      contentVersion: "1.0.0.0"
      parameters:
        rgName:
          type: string
      resources:
        - type: Microsoft.Resources/resourceGroups
          apiVersion: "2022-09-01"
          name: "[parameters('rgName')]"
          location: eastus
    parameters:
      rgName:
        value: myResourceGroup
    tags:
      environment: test

- name: Deploy a linked template with a Key Vault secret reference parameter
  azure.azcollection.azure_rm_subscriptiondeployment:
    name: linked-template-deployment
    location: eastus
    template_link:
      uri: https://example.com/templates/azuredeploy.json
    parameters:
      adminPassword:
        reference:
          keyVault:
            id: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/myVault
          secretName: adminPassword

- name: Delete a subscription-scope deployment
  azure.azcollection.azure_rm_subscriptiondeployment:
    name: create-rg-deployment
    state: absent
'''

RETURN = '''
state:
    description:
        - The current state of the deployment.
    returned: when I(state=present) and the deployment exists
    type: complex
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, normalize_location_name

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


def _detail_levels(value):
    levels = set(item.strip().lower() for item in (value or '').split(',') if item.strip())
    levels.discard('none')
    return levels


def _normalize_parameter_value(value, parameter_type):
    parameter_type = (parameter_type or '').lower()
    if parameter_type == 'bool' and isinstance(value, (bool, str)):
        return str(value).lower()
    if parameter_type == 'int' and isinstance(value, (int, str)) and not isinstance(value, bool):
        return str(value)
    return value


class AzureRMSubscriptionDeployment(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True, aliases=['deployment_name']),
            location=dict(type='str'),
            template=dict(type='dict'),
            template_link=dict(
                type='dict',
                options=dict(
                    uri=dict(type='str'),
                    id=dict(type='str'),
                    relative_path=dict(type='str'),
                    content_version=dict(type='str'),
                    query_string=dict(type='str', no_log=True),
                ),
                required_one_of=[('uri', 'id')],
                mutually_exclusive=[('uri', 'id')],
            ),
            parameters=dict(type='dict'),
            secure_parameters=dict(type='dict', no_log=True),
            parameters_link=dict(
                type='dict',
                options=dict(
                    uri=dict(type='str', required=True),
                    content_version=dict(type='str'),
                ),
            ),
            debug_setting=dict(
                type='dict',
                options=dict(
                    detail_level=dict(type='str'),
                ),
            ),
            on_error_deployment=dict(
                type='dict',
                options=dict(
                    type=dict(type='str', choices=['LastSuccessful', 'SpecificDeployment']),
                    deployment_name=dict(type='str'),
                ),
                required_by=dict(deployment_name='type'),
            ),
            expression_evaluation_options=dict(
                type='dict',
                options=dict(
                    scope=dict(type='str', choices=['NotSpecified', 'Outer', 'Inner']),
                ),
            ),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        mutually_exclusive = [
            ('template', 'template_link'),
            ('parameters', 'parameters_link'),
            ('secure_parameters', 'parameters_link'),
        ]
        required_if = [
            ('state', 'present', ['location']),
            ('state', 'present', ['template', 'template_link'], True),
        ]

        self.name = None
        self.location = None
        self.template = None
        self.template_link = None
        self.parameters = None
        self.secure_parameters = None
        self.parameters_link = None
        self.debug_setting = None
        self.on_error_deployment = None
        self.expression_evaluation_options = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False)

        super(AzureRMSubscriptionDeployment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=True,
                                                            mutually_exclusive=mutually_exclusive,
                                                            required_if=required_if)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.check_parameter_names()

        old_response = self.get_deployment()
        response = old_response
        changed = False

        if self.state == 'present':
            tags_changed, new_tags = self.update_tags(old_response.get('tags') if old_response else None)
            if old_response:
                self.check_location(old_response)
                changed = tags_changed or self.is_update_required(old_response)
            else:
                changed = True

            if changed and not self.check_mode:
                response = self.create_or_update_deployment(new_tags, old_response)
            if response:
                self.results['state'] = response
        elif old_response:
            changed = True
            if not self.check_mode:
                self.delete_deployment()

        self.results['changed'] = changed
        return self.results

    def check_parameter_names(self):
        duplicates = set(key.lower() for key in (self.parameters or {})) & set(key.lower() for key in (self.secure_parameters or {}))
        if duplicates:
            self.fail("Parameters {0} are set in both parameters and secure_parameters; set each parameter in only one of them.".format(
                ', '.join(sorted(duplicates))))

    def get_inline_parameters(self):
        if self.parameters is None and self.secure_parameters is None:
            return None
        merged = dict(self.parameters or {})
        merged.update(self.secure_parameters or {})
        return merged

    def check_location(self, old_response):
        old_location = old_response.get('location') or ''
        if normalize_location_name(old_location) != normalize_location_name(self.location):
            self.fail("Deployment {0} already exists in location {1}. The location of an existing deployment cannot be changed; "
                      "use a different deployment name or the original location.".format(self.name, old_location))

    def is_update_required(self, old_response):
        properties = old_response.get('properties') or {}

        if properties.get('provisioning_state') in ('Failed', 'Canceled'):
            return True

        if self.template is not None:
            if properties.get('template_link'):
                return True
            if self.get_template_hash() != properties.get('template_hash'):
                return True
        elif self.is_subset_changed(self.template_link, properties.get('template_link'), exclude=('query_string',)):
            return True

        inline_parameters = self.get_inline_parameters()
        if inline_parameters is not None:
            if properties.get('parameters_link') or self.is_parameters_changed(inline_parameters, properties.get('parameters')):
                return True
        elif self.is_subset_changed(self.parameters_link, properties.get('parameters_link')):
            return True

        if self.on_error_deployment is not None:
            if self.on_error_deployment.get('type') is None:
                if (properties.get('on_error_deployment') or {}).get('type'):
                    return True
            elif self.is_subset_changed(self.on_error_deployment, properties.get('on_error_deployment')):
                return True

        if self.debug_setting and self.debug_setting.get('detail_level') is not None:
            old_detail_level = (properties.get('debug_setting') or {}).get('detail_level')
            if _detail_levels(self.debug_setting['detail_level']) != _detail_levels(old_detail_level):
                return True

        return False

    @staticmethod
    def is_subset_changed(desired, actual, exclude=()):
        if not desired:
            return False
        actual = actual or {}
        return any(value is not None and key not in exclude and actual.get(key) != value for key, value in desired.items())

    def is_parameters_changed(self, desired_parameters, old_parameters):
        old_parameters = dict((key.lower(), value) for key, value in (old_parameters or {}).items())
        for key, value in desired_parameters.items():
            if isinstance(value, dict) and 'reference' in value:
                continue
            old_parameter = old_parameters.get(key.lower())
            if not isinstance(old_parameter, dict):
                return True
            parameter_type = old_parameter.get('type')
            if (parameter_type or '').lower() in ('securestring', 'secureobject'):
                continue
            desired_value = value.get('value') if isinstance(value, dict) else value
            if _normalize_parameter_value(old_parameter.get('value'), parameter_type) != _normalize_parameter_value(desired_value, parameter_type):
                return True
        return False

    def get_deployment(self):
        self.log("Checking if subscription deployment {0} is present".format(self.name))
        try:
            response = self.rm_client.deployments.get_at_subscription_scope(self.name)
        except ResourceNotFoundError:
            self.log("Did not find subscription deployment {0}".format(self.name))
            return None
        except Exception as exc:
            self.fail("Error retrieving subscription deployment {0} - {1}".format(self.name, str(exc)))
        return as_attribute_dict(response, exclude_readonly=False)

    def get_template_hash(self):
        try:
            return self.rm_client.deployments.calculate_template_hash(template=self.template).template_hash
        except Exception as exc:
            self.fail("Error calculating the template hash of subscription deployment {0} - {1}".format(self.name, str(exc)))

    def get_debug_setting(self, old_properties):
        models = self.rm_models
        if self.debug_setting and self.debug_setting.get('detail_level') is not None:
            return models.DebugSetting(**self.debug_setting)
        levels = _detail_levels((old_properties.get('debug_setting') or {}).get('detail_level'))
        if not levels:
            return None
        names = dict(requestcontent='requestContent', responsecontent='responseContent')
        return models.DebugSetting(detail_level=','.join(names.get(level, level) for level in sorted(levels)))

    def get_on_error_deployment(self, old_properties):
        models = self.rm_models
        if self.on_error_deployment is not None:
            if self.on_error_deployment.get('type') is None:
                return None
            return models.OnErrorDeployment(**self.on_error_deployment)
        old_on_error = old_properties.get('on_error_deployment') or {}
        if not old_on_error.get('type'):
            return None
        deployment_name = old_on_error.get('deployment_name') if old_on_error['type'] == 'SpecificDeployment' else None
        return models.OnErrorDeployment(type=old_on_error['type'], deployment_name=deployment_name)

    def create_or_update_deployment(self, tags, old_response=None):
        self.log("Creating or updating subscription deployment {0}".format(self.name))
        models = self.rm_models
        old_properties = (old_response or {}).get('properties') or {}
        properties = models.DeploymentProperties(
            mode='Incremental',
            template=self.template,
            template_link=models.TemplateLink(**self.template_link) if self.template_link else None,
            parameters=self.get_inline_parameters(),
            parameters_link=models.ParametersLink(**self.parameters_link) if self.parameters_link else None,
            debug_setting=self.get_debug_setting(old_properties),
            on_error_deployment=self.get_on_error_deployment(old_properties),
            expression_evaluation_options=(models.ExpressionEvaluationOptions(**self.expression_evaluation_options)
                                           if self.expression_evaluation_options else None),
        )
        deployment = models.Deployment(location=self.location, tags=tags, properties=properties)
        try:
            poller = self.rm_client.deployments.begin_create_or_update_at_subscription_scope(self.name, deployment)
            response = self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error creating or updating subscription deployment {0} - {1}".format(self.name, str(exc)),
                      failed_deployment_operations=self.get_failed_operations())

        result = as_attribute_dict(response, exclude_readonly=False)
        provisioning_state = (result.get('properties') or {}).get('provisioning_state')
        if provisioning_state != 'Succeeded':
            self.fail("Subscription deployment {0} finished with provisioning state {1}".format(self.name, provisioning_state), state=result,
                      failed_deployment_operations=self.get_failed_operations())
        return result

    def get_failed_operations(self):
        try:
            operations = self.rm_client.deployment_operations.list_at_subscription_scope(self.name)
            failed = []
            for operation in operations:
                item = as_attribute_dict(operation, exclude_readonly=False)
                properties = item.get('properties') or {}
                if properties.get('provisioning_state') != 'Failed':
                    continue
                properties.pop('request', None)
                properties.pop('response', None)
                failed.append(item)
            return failed
        except Exception as exc:
            self.log("Could not list failed operations of subscription deployment {0} - {1}".format(self.name, str(exc)))
            return []

    def delete_deployment(self):
        self.log("Deleting subscription deployment {0}".format(self.name))
        try:
            poller = self.rm_client.deployments.begin_delete_at_subscription_scope(self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting subscription deployment {0} - {1}".format(self.name, str(exc)))


def main():
    AzureRMSubscriptionDeployment()


if __name__ == '__main__':
    main()

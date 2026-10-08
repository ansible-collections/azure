#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cognitiveservicesdeployment
version_added: "4.2.0"
short_description: Manage model deployments in an Azure AI / OpenAI account
description:
    - Create, update, and delete a model deployment within an Azure AI Services
      or Azure OpenAI (Cognitive Services) account.
    - An Azure OpenAI account is a Cognitive Services account with I(kind=OpenAI);
      create it with M(azure.azcollection.azure_rm_cognitiveservicesaccount).
options:
    resource_group:
        description:
            - Name of the resource group containing the account.
        required: true
        type: str
        aliases:
            - resource_group_name
    account_name:
        description:
            - Name of the Cognitive Services / Azure OpenAI account that hosts the deployment.
        required: true
        type: str
    name:
        description:
            - Name of the model deployment.
        required: true
        type: str
    model:
        description:
            - The model to deploy.
            - Required when creating a deployment.
        type: dict
        suboptions:
            name:
                description:
                    - Name of the model to deploy, e.g. C(gpt-4o-mini).
                type: str
                required: true
            format:
                description:
                    - The format of the model, e.g. C(OpenAI).
                type: str
                default: OpenAI
            version:
                description:
                    - The version of the model. If omitted, Azure selects the default version.
                type: str
    sku:
        description:
            - The resource SKU controlling the deployment type and capacity.
        type: dict
        suboptions:
            name:
                description:
                    - SKU name, e.g. C(Standard), C(GlobalStandard), C(DataZoneStandard).
                type: str
            capacity:
                description:
                    - Capacity (quota) assigned to the deployment, in units of
                      thousands of tokens-per-minute for most OpenAI models.
                type: int
    rai_policy_name:
        description:
            - Name of the responsible-AI (content filter) policy to apply.
        type: str
    version_upgrade_option:
        description:
            - Deployment model version upgrade option.
        type: str
        choices:
            - OnceNewDefaultVersionAvailable
            - OnceCurrentVersionExpired
            - NoAutoUpgrade
    state:
        description:
            - Assert the state of the deployment. Use C(present) to create/update,
              C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Deploy a GPT-4.1 mini model (Standard)
  azure.azcollection.azure_rm_cognitiveservicesdeployment:
    resource_group: myResourceGroup
    account_name: myopenaiaccount
    name: gpt-4.1-mini
    model:
      name: gpt-4.1-mini
      version: "2025-04-14"
    sku:
      name: Standard
      capacity: 10
    version_upgrade_option: OnceNewDefaultVersionAvailable

- name: Scale the deployment capacity (idempotent re-run after changing capacity)
  azure.azcollection.azure_rm_cognitiveservicesdeployment:
    resource_group: myResourceGroup
    account_name: myopenaiaccount
    name: gpt-4.1-mini
    model:
      name: gpt-4.1-mini
      version: "2025-04-14"
    sku:
      name: Standard
      capacity: 50

- name: Delete a model deployment
  azure.azcollection.azure_rm_cognitiveservicesdeployment:
    resource_group: myResourceGroup
    account_name: myopenaiaccount
    name: gpt-4.1-mini
    state: absent
'''

RETURN = '''
state:
    description:
        - The model deployment as returned by Azure.
    returned: when I(state=present)
    type: dict
    sample: {
        "id": "/subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.CognitiveServices/accounts/myopenaiaccount/deployments/gpt-4.1-mini",
        "name": "gpt-4.1-mini",
        "sku": {"name": "Standard", "capacity": 10},
        "properties": {
            "model": {"format": "OpenAI", "name": "gpt-4.1-mini", "version": "2025-04-14"},
            "provisioning_state": "Succeeded",
            "version_upgrade_option": "OnceNewDefaultVersionAvailable"
        },
        "type": "Microsoft.CognitiveServices/accounts/deployments"
    }
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCognitiveServicesDeployment(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True, aliases=['resource_group_name']),
            account_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            model=dict(type='dict', options=dict(
                name=dict(type='str', required=True),
                format=dict(type='str', default='OpenAI'),
                version=dict(type='str'),
            )),
            sku=dict(type='dict', options=dict(
                name=dict(type='str'),
                capacity=dict(type='int'),
            )),
            rai_policy_name=dict(type='str'),
            version_upgrade_option=dict(type='str', choices=[
                'OnceNewDefaultVersionAvailable',
                'OnceCurrentVersionExpired',
                'NoAutoUpgrade',
            ]),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.account_name = None
        self.name = None
        self.model = None
        self.sku = None
        self.rai_policy_name = None
        self.version_upgrade_option = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False, compare=[])

        super(AzureRMCognitiveServicesDeployment, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        existing = self.get_deployment()

        if self.state == 'present':
            if not existing:
                if not self.model:
                    self.module.fail_json(
                        msg="model is required to create deployment '{0}'; "
                            "it does not exist yet".format(self.name))
                params = self.build_deployment_parameters()
                if self.tags:
                    params['tags'] = self.update_tags(None)[1]
                if not self.check_mode:
                    self.results['state'] = self.create_or_update_deployment(params)
                else:
                    self.results['state'] = params
                self.results['changed'] = True
            else:
                params = self.build_deployment_parameters()
                if self.check_update_needed(existing, params):
                    # begin_create_or_update issues a PUT (full replace), so
                    # carry forward the existing model/sku the user did not
                    # resupply; otherwise the PUT would be incomplete.
                    body = self._merge_for_update(existing, params)
                    if not self.check_mode:
                        self.results['state'] = self.create_or_update_deployment(body)
                    else:
                        self.results['state'] = body
                    self.results['changed'] = True
                else:
                    self.results['state'] = existing
        else:  # absent
            if existing:
                if not self.check_mode:
                    self.delete_deployment()
                self.results['changed'] = True
            self.results['state'] = dict()

        return self.results

    def get_deployment(self):
        """Return the deployment as a dict, or None if it does not exist."""
        self.log("Getting deployment {0} on account {1}".format(self.name, self.account_name))
        try:
            obj = self.cognitive_services_management_client.deployments.get(
                self.resource_group,
                self.account_name,
                self.name
            )
            return obj.as_dict()
        except ResourceNotFoundError:
            self.log("Deployment {0} not found".format(self.name))
            return None

    def build_deployment_parameters(self):
        """Build the deployment body (snake_case keys matching the SDK model)."""
        properties = {}
        if self.model is not None:
            model = {}
            for key in ('format', 'name', 'version'):
                value = self.model.get(key)
                if value is not None:
                    model[key] = value
            properties['model'] = model
        if self.rai_policy_name is not None:
            properties['rai_policy_name'] = self.rai_policy_name
        if self.version_upgrade_option is not None:
            properties['version_upgrade_option'] = self.version_upgrade_option

        params = {}
        if self.sku is not None:
            sku = {}
            for key in ('name', 'capacity'):
                value = self.sku.get(key)
                if value is not None:
                    sku[key] = value
            if sku:
                params['sku'] = sku
        if properties:
            params['properties'] = properties
        return params

    def check_update_needed(self, existing, params):
        """Return True when the existing deployment differs from the desired params."""
        changed = False

        update_tags, newtags = self.update_tags(existing.get('tags'))
        if newtags:
            params['tags'] = newtags
        if update_tags:
            changed = True

        # default_compare mutates the "new" dict it is given (it fills unset
        # keys from "old"), so compare against a copy to keep params clean.
        if not self.default_compare({}, copy.deepcopy(params), existing, '', self.results):
            changed = True

        return changed

    def _merge_for_update(self, existing, params):
        """Build the PUT body, carrying forward existing model/sku when the
        user did not resupply them (begin_create_or_update is a full replace)."""
        body = copy.deepcopy(params)
        existing_props = existing.get('properties') or {}
        props = body.setdefault('properties', {})
        if 'model' not in props and existing_props.get('model') is not None:
            existing_model = existing_props['model']
            props['model'] = {k: existing_model[k]
                              for k in ('format', 'name', 'version')
                              if existing_model.get(k) is not None}
        if not props:
            body.pop('properties', None)
        if 'sku' not in body and existing.get('sku') is not None:
            existing_sku = existing['sku']
            sku = {k: existing_sku[k] for k in ('name', 'capacity')
                   if existing_sku.get(k) is not None}
            if sku:
                body['sku'] = sku
        return body

    def create_or_update_deployment(self, params):
        """Create or update the deployment and return it as a dict."""
        self.log("Creating/updating deployment {0}".format(self.name))
        try:
            poller = self.cognitive_services_management_client.deployments.begin_create_or_update(
                self.resource_group,
                self.account_name,
                self.name,
                params
            )
            obj = self.get_poller_result(poller)
            return obj.as_dict()
        except Exception as exc:
            self.module.fail_json(msg="Failed to create/update deployment {0}: {1}".format(self.name, str(exc)))

    def delete_deployment(self):
        """Delete the deployment."""
        self.log("Deleting deployment {0}".format(self.name))
        try:
            poller = self.cognitive_services_management_client.deployments.begin_delete(
                self.resource_group,
                self.account_name,
                self.name
            )
            self.get_poller_result(poller)
        except Exception as exc:
            self.module.fail_json(msg="Failed to delete deployment {0}: {1}".format(self.name, str(exc)))


def main():
    AzureRMCognitiveServicesDeployment()


if __name__ == '__main__':
    main()

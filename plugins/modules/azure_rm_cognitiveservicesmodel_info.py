#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_cognitiveservicesmodel_info

version_added: "3.20.0"

short_description: List cognitiveservices models facts

description:
    - List all model details under location.

options:
    location:
        description:
            - The location of the models.
        type: str
        required: true

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - bpeck@redhat.com (@p3ck)
'''

EXAMPLES = '''
- name: List all models at location
  azure_rm_cognitiveservicesmodel_info:
    location: eastus
'''

RETURN = '''
models:
    description:
        - List of model details.
    returned: always
    type: dict
    sample: [
        {
            "kind": "OpenAI",
            "model": {
                "capabilities": {
                    "imageGenerations": "true",
                    "inference": "true"
                },
                "deprecation": {
                    "inference": "2026-03-04T00:00:00Z"
                },
                "format": "OpenAI",
                "is_default_version": true,
                "lifecycle_status": "Deprecated",
                "max_capacity": 2,
                "name": "dall-e-3",
                "skus": [
                    {
                        "capacity": {
                            "default": 1,
                            "maximum": 1000
                        },
                        "deprecation_date": "2026-03-04T00:00:00.000Z",
                        "name": "Standard",
                        "rate_limits": [
                            {
                                "count": 3.0,
                                "renewal_period": 60.0
                            }
                        ],
                        "usage_name": "OpenAI.Standard.Dalle"
                    }
                ],
                "system_data": {
                    "created_at": "2023-08-11T00:00:00.000Z",
                    "created_by": "Microsoft",
                    "last_modified_at": "2023-08-11T00:00:00.000Z",
                    "last_modified_by": "Microsoft"
                },
                "version": "3.0"
            },
            "sku_name": "S0"
        },
        {
            "kind": "OpenAI",
            "model": {
                "capabilities": {
                    "imageGenerations": "true",
                    "inference": "true"
                },
                "deprecation": {
                    "inference": "2025-01-27T00:00:00Z"
                },
                "format": "OpenAI",
                "is_default_version": true,
                "lifecycle_status": "Deprecated",
                "max_capacity": 2,
                "name": "dall-e-2",
                "skus": [
                    {
                        "capacity": {
                            "default": 1,
                            "maximum": 1000
                        },
                        "deprecation_date": "2025-01-27T00:00:00.000Z",
                        "name": "Standard",
                        "rate_limits": [
                            {
                                "count": 3.0,
                                "renewal_period": 60.0
                            }
                        ],
                        "usage_name": "OpenAI.Standard.Dalle-2"
                    }
                ],
                "system_data": {
                    "created_at": "2024-04-15T00:00:00.000Z",
                    "created_by": "Microsoft",
                    "last_modified_at": "2024-04-15T00:00:00.000Z",
                    "last_modified_by": "Microsoft"
                },
                "version": "2.0"
            },
            "sku_name": "S0"
        },
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMCognitiveServicesModelInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            location=dict(
                type='str',
                required=True,
            ),
        )

        self.results = dict(
            changed=False,
            models=[],
        )

        super(AzureRMCognitiveServicesModelInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.results['models'] = self.list_all(self.location)

        return self.results

    def list_all(self, location):
        results = []
        try:
            models = self.cognitive_services_management_client.models.list(
                location=location
            )
            for model in models:
                results.append(model.as_dict())
        except Exception as exc:
            self.fail('Error when listing all models under subscription got Exception as {0}'.format(str(exc)))
        return results


def main():
    AzureRMCognitiveServicesModelInfo()


if __name__ == '__main__':
    main()

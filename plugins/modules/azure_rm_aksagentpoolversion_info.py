#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_aksagentpoolversion_info

version_added: "1.14.0"

short_description: Gets a list of supported versions for the specified agent pool

description:
    - Gets a list of supported versions for the specified agent pool.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    cluster_name:
        description:
            - The name of the managed cluster resource.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
    - name: Get  available versions an AKS can be upgrade to
      azure_rm_aksagentpoolversion_info:
        resource_group: myResourceGroup
        cluster_name: myAKSName
'''

RETURN = '''
azure_orchestrator_version:
    description:
        - List of supported kubernetes versions.
    returned: always
    type: list
    sample: ['1.22.6', '1.22.11']
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMAksAgentPoolVersion(AzureRMModuleBase):

    def __init__(self):

        self.module_args = dict(
            resource_group=dict(type='str', required=True),
            cluster_name=dict(type='str', required=True),
        )

        self.results = dict(
            changed=False,
            azure_orchestrator_version=[]
        )

        self.resource_group = None
        self.cluster_name = None

        super(AzureRMAksAgentPoolVersion, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        self.results['azure_orchestrator_version'] = self.get_all_versions()

        return self.results

    def get_all_versions(self):
        '''
        Get all avaliable orchestrator version
        '''
        try:
            result = list()
            response = self.managedcluster_client.agent_pools.get_available_agent_pool_versions(self.resource_group, self.cluster_name)
            orchestrators = response.agent_pool_versions
            for item in orchestrators:
                result.append(item.kubernetes_version)
            return result
        except Exception as exc:
            self.fail('Error when getting Agentpool supported orchestrator version list for locatio', exc)


def main():
    """Main module execution code path"""

    AzureRMAksAgentPoolVersion()


if __name__ == '__main__':
    main()

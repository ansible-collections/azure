#!/usr/bin/python
#
# Copyright (c) 2021 Andrii Bilorus, <andrii.bilorus@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_aksupgrade_info

version_added: "1.4.0"

short_description: Get the upgrade versions available for a AKS instance

description:
    - Get the upgrade versions available for a managed Azure Container Service (AKS) instance.

options:
    resource_group:
        description:
            - Name of a resource group where the managed Azure Container Services (AKS) exists.
        required: true
        type: str
    name:
        description:
            - Name of the managed Azure Container Services (AKS) instance.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Andrii Bilorus (@ewscat)
'''

EXAMPLES = '''
    - name: Get available upgrade versions for AKS instance
      azure_rm_aksupgrade_info:
        name: myAKS
        resource_group: myResourceGroup
      register: myAKSupgrades
'''

RETURN = '''
azure_aks_upgrades:
    description: Supported AKS instance versions for upgrade by agent pools and control plane.
    returned: always
    type: complex
    contains:
        agent_pool_profiles:
            description: Available upgrade versions for agent pools
            returned: always
            type: complex
            contains:
                upgrades:
                    description: List of orchestrator types and versions available for upgrade.
                    type: complex
                    contains:
                        is_preview:
                            description: Is the version available in preview
                            type: bool
                        kubernetes_version:
                            description: Kubernetes version
                            type: str
                            sample: "1.19.3"
                os_type:
                    description: Operating system type
                    type: str
                    sample: "Linux"
                name:
                    description: Pool name
                    type: str
                    sample: "my_pool"
                kubernetes_version:
                    description: Current kubernetes version
                    type: str
                    sample: "1.18.1"
        control_plane_profile:
            description: Available upgrade versions for control plane
            returned: always
            type: complex
            contains:
                upgrades:
                    description: List of orchestrator types and versions available for upgrade.
                    type: complex
                    contains:
                        is_preview:
                            description: Is the version available in preview
                            type: bool
                        kubernetes_version:
                            description: Kubernetes version
                            type: str
                            sample: "1.19.3"
                os_type:
                    description: Operating system type
                    type: str
                    sample: "Linux"
                name:
                    description: Pool name
                    type: str
                    sample: "my_pool"
                kubernetes_version:
                    description: Current kubernetes version
                    type: str
                    sample: "1.18.1"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureHttpError
except Exception:
    # handled in azure_rm_common
    pass


class AzureRMAKSUpgrade(AzureRMModuleBase):
    '''
    Utility class to get Azure Kubernetes Service upgrades
    '''

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True)
        )

        self.results = dict(
            changed=False,
            azure_aks_upgrades=[]
        )

        self.name = None
        self.resource_group = None

        super(AzureRMAKSUpgrade, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):
        for key in self.module_args:
            setattr(self, key, kwargs[key])

        self.results['azure_aks_upgrades'] = self.get_upgrades(self.name, self.resource_group)

        return self.results

    def get_upgrades(self, name, resource_group):
        '''
        Get supported upgrade version for AKS
        :param: name: str with name of AKS cluster instance
        :param: resource_group: str with resource group containing AKS instance
        :return: dict with available versions for pool profiles and control plane
        '''
        cluster = None
        upgrade_profiles = None

        self.log('Get properties for {0}'.format(self.name))
        try:
            cluster = self.managedcluster_client.managed_clusters.get(resource_group_name=resource_group, resource_name=name)
        except CloudError as err:
            self.fail('Error when getting AKS cluster information for {0} : {1}'.format(self.name, err.message or str(err)))

        self.log('Get available upgrade versions for {0}'.format(self.name))
        try:
            upgrade_profiles = self.managedcluster_client.managed_clusters.get_upgrade_profile(resource_group_name=resource_group,
                                                                                               resource_name=name)
        except CloudError as err:
            self.fail('Error when getting upgrade versions for {0} : {1}'.format(self.name, err.message or str(err)))

        return dict(
            agent_pool_profiles=[self.parse_profile(profile)
                                 if profile.upgrades else self.default_profile(cluster)
                                 for profile in upgrade_profiles.agent_pool_profiles]
            if upgrade_profiles.agent_pool_profiles else None,
            control_plane_profile=self.parse_profile(upgrade_profiles.control_plane_profile)
            if upgrade_profiles.control_plane_profile.upgrades
            else self.default_profile(cluster)
        )

    def default_profile(self, cluster):
        '''
        Used when upgrade profile returned by Azure in None
        (i.e. when the cluster runs latest version)
        :param: cluster: ManagedCluster with AKS instance information
        :return: dict containing upgrade profile with current cluster version
        '''
        return dict(
            upgrades=None,
            kubernetes_version=cluster.kubernetes_version,
            name=None,
            os_type=None
        )

    def parse_profile(self, profile):
        '''
        Transform cluster profile object to dict
        :param: profile: ManagedClusterUpgradeProfile with AKS upgrade profile info
        :return: dict with upgrade profiles
        '''
        return dict(
            upgrades=[dict(
                is_preview=upgrade.is_preview,
                kubernetes_version=upgrade.kubernetes_version
            ) for upgrade in profile.upgrades],
            kubernetes_version=profile.kubernetes_version,
            name=profile.name,
            os_type=profile.os_type
        )


def main():
    '''
    Main module execution code path
    '''
    AzureRMAKSUpgrade()


if __name__ == '__main__':
    main()

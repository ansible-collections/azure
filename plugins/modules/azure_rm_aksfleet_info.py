#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_aksfleet_info
version_added: "4.3.0"
short_description: Get Fleet Managers and their cluster memberships
description:
    - Get details of a single Fleet Manager and its member clusters, or list
      all fleets in a resource group.
    - Every returned fleet includes its members in I(members).
options:
    resource_group:
        description:
            - Name of the resource group containing the fleet.
        required: true
        type: str
    name:
        description:
            - Name of a specific fleet to fetch. If omitted, all fleets of
              the resource group are listed.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get a specific fleet with its members
  azure.azcollection.azure_rm_aksfleet_info:
    resource_group: myResourceGroup
    name: myFleet
  register: fleet

- name: List all fleets of a resource group
  azure.azcollection.azure_rm_aksfleet_info:
    resource_group: myResourceGroup
  register: fleets
'''

RETURN = '''
fleets:
    description:
        - List of fleets.
        - Each fleet includes its member clusters in I(members).
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "name": "myFleet",
            "location": "eastus",
            "provisioning_state": "Succeeded",
            "members": [
                {
                    "name": "aks1",
                    "cluster_resource_id":
                      "/subscriptions/xxx/resourceGroups/rg1/providers/Microsoft.ContainerService/managedClusters/aks1",
                    "provisioning_state": "Succeeded"
                }
            ]
        }
    ]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.containerservicefleet import ContainerServiceFleetMgmtClient
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMAksFleetInfo(AzureRMModuleBaseExt):
    """Get Fleet Managers and their cluster memberships."""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.resource_group = None
        self.name = None

        self.results = dict(
            changed=False,
            fleets=[],
        )

        super(AzureRMAksFleetInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.fleet_client = self.get_mgmt_svc_client(
            ContainerServiceFleetMgmtClient, base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name:
            items = self._get()
        else:
            items = self._list()

        self.results['fleets'] = [self._format(item) for item in items]
        return self.results

    def _get(self):
        try:
            return [self.fleet_client.fleets.get(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
            )]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error retrieving fleet {0}: {1}".format(self.name, str(exc)))

    def _list(self):
        try:
            return list(self.fleet_client.fleets.list_by_resource_group(
                resource_group_name=self.resource_group,
            ))
        except Exception as exc:
            self.fail("Error listing fleets in resource group {0}: {1}".format(self.resource_group, str(exc)))

    def _format(self, item):
        normalized = as_attribute_dict(item, exclude_readonly=False)
        if normalized.get('properties'):
            normalized.update(normalized.pop('properties'))
        normalized['resource_group'] = self.resource_group
        normalized['members'] = self._member_list(normalized['name'])
        return normalized

    def _member_list(self, fleet_name):
        try:
            members = list(self.fleet_client.fleet_members.list_by_fleet(
                resource_group_name=self.resource_group,
                fleet_name=fleet_name,
            ))
        except Exception as exc:
            self.fail("Error listing members of fleet {0}: {1}".format(fleet_name, str(exc)))
        result = []
        for member in members:
            normalized = as_attribute_dict(member, exclude_readonly=False)
            properties = normalized.pop('properties', None) or {}
            normalized.update(properties)
            normalized.pop('system_data', None)
            result.append(normalized)
        return result


def main():
    AzureRMAksFleetInfo()


if __name__ == '__main__':
    main()

#!/usr/bin/python
#
# Copyright (c) 2018 Yuwei Zhou, <yuwzho@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_routetable
version_added: "0.1.2"
short_description: Manage Azure route table resource
description:
    - Create, update or delete a route table.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - Name of the route table.
        required: true
        type: str
    state:
        description:
            - Assert the state of the route table. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    disable_bgp_route_propagation:
        description:
            - Specified whether to disable the routes learned by BGP on that route table.
        type: bool
        default: False
    location:
        description:
            - Region of the resource.
            - Derived from I(resource_group) if not specified.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Yuwei Zhou (@yuwzho)

'''

EXAMPLES = '''
- name: Create a route table
  azure_rm_routetable:
    resource_group: myResourceGroup
    name: myRouteTable
    disable_bgp_route_propagation: false
    tags:
      purpose: testing

- name: Delete a route table
  azure_rm_routetable:
    resource_group: myResourceGroup
    name: myRouteTable
    state: absent
'''
RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: true
id:
    description:
        - Resource ID.
    returned: success
    type: str
    sample: "/subscriptions/xxx...xxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/routeTables/tableb57dc95642/routes/routeb57dc95986"
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, normalize_location_name


class AzureRMRouteTable(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            disable_bgp_route_propagation=dict(type='bool', default=False)
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.tags = None
        self.disable_bgp_route_propagation = None

        self.results = dict(
            changed=False
        )

        super(AzureRMRouteTable, self).__init__(self.module_arg_spec,
                                                supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location
        self.location = normalize_location_name(self.location)

        result = dict()
        changed = False

        result = self.get_table()
        if self.state == 'absent' and result:
            changed = True
            if not self.check_mode:
                self.delete_table()
        elif self.state == 'present':
            routes = []
            subnets = None
            if not result:
                changed = True  # create new route table
            else:  # check update
                routes = result.routes
                subnets = result.subnets
                update_tags, self.tags = self.update_tags(result.tags)
                if update_tags:
                    changed = True
                if self.disable_bgp_route_propagation != result.disable_bgp_route_propagation:
                    changed = True

            if changed:
                result = self.network_models.RouteTable(location=self.location,
                                                        tags=self.tags,
                                                        routes=routes,
                                                        subnets=subnets,
                                                        disable_bgp_route_propagation=self.disable_bgp_route_propagation)
                if not self.check_mode:
                    result = self.create_or_update_table(result)

        self.results['id'] = result.id if result else None
        self.results['changed'] = changed
        return self.results

    def create_or_update_table(self, param):
        try:
            poller = self.network_client.route_tables.begin_create_or_update(self.resource_group, self.name, param)
            return self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error creating or updating route table {0} - {1}".format(self.name, str(exc)))

    def delete_table(self):
        try:
            poller = self.network_client.route_tables.begin_delete(self.resource_group, self.name)
            result = self.get_poller_result(poller)
            return result
        except Exception as exc:
            self.fail("Error deleting virtual network {0} - {1}".format(self.name, str(exc)))

    def get_table(self):
        try:
            return self.network_client.route_tables.get(self.resource_group, self.name)
        except ResourceNotFoundError as cloud_err:
            # Return None iff the resource is not found
            if cloud_err.status_code == 404:
                self.log('{0}'.format(str(cloud_err)))
                return None
            self.fail('Error: failed to get resource {0} - {1}'.format(self.name, str(cloud_err)))
        except Exception as exc:
            self.fail('Error: failed to get resource {0} - {1}'.format(self.name, str(exc)))


def main():
    AzureRMRouteTable()


if __name__ == '__main__':
    main()

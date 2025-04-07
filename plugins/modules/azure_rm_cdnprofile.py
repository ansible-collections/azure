#!/usr/bin/python
#
# Copyright (c) 2018 Hai Cao, <t-haicao@microsoft.com>, Yunge Zhu <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cdnprofile
version_added: "0.1.2"
short_description: Manage a Azure CDN profile
description:
    - Create, update and delete a Azure CDN profile.

options:
    resource_group:
        description:
            - Name of a resource group where the CDN profile exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of the CDN profile.
        required: true
        type: str
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    sku:
        description:
            - The pricing tier, defines a CDN provider, feature list and rate of the CDN profile.
            - Detailed pricing can be find at U(https://azure.microsoft.com/en-us/pricing/details/cdn/).
        type: str
        choices:
            - standard_verizon
            - premium_verizon
            - custom_verizon
            - standard_akamai
            - standard_chinacdn
            - standard_microsoft
            - standard_azurefrontdoor
            - premium_azurefrontdoor
            - standard_955bandwidth_chinacdn
            - standard_avgbandwidth_chinacdn
            - standardplus_chinacdn
            - standardplus_955bandwidth_chinacdn
            - standardplus_avgbandwidth_chinacdn
    state:
        description:
            - Assert the state of the CDN profile. Use C(present) to create or update a CDN profile and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple

author:
    - Hai Cao (@caohai)
    - Yunge Zhu (@yungezz)
'''

EXAMPLES = '''
- name: Create a CDN profile
  azure_rm_cdnprofile:
    resource_group: myResourceGroup
    name: myCDN
    sku: standard_akamai
    tags:
      testing: testing

- name: Delete the CDN profile
  azure_rm_cdnprofile:
    resource_group: myResourceGroup
    name: myCDN
    state: absent
'''
RETURN = '''
id:
    description: Current state of the CDN profile.
    returned: always
    type: dict
    example:
            id: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myResourceGroup/providers/Microsoft.Cdn/profiles/myCDN
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import uuid

try:
    from azure.mgmt.cdn.models import Profile, Sku, ManagedServiceIdentity, UserAssignedIdentity, ProfileUpdateParameters
except ImportError as ec:
    # This is handled in azure_rm_common
    pass


def cdnprofile_to_dict(cdnprofile):
    return dict(
        id=cdnprofile.id,
        name=cdnprofile.name,
        type=cdnprofile.type,
        location=cdnprofile.location,
        sku=cdnprofile.sku.name,
        resource_state=cdnprofile.resource_state,
        provisioning_state=cdnprofile.provisioning_state,
        tags=cdnprofile.tags,
        identity=cdnprofile.identity.as_dict() if cdnprofile.identity else None
    )


class AzureRMCdnprofile(AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            sku=dict(
                type='str',
                choices=[
                    'standard_verizon', 'premium_verizon', 'custom_verizon', 'standard_akamai', 'standard_chinacdn',
                    'standard_microsoft', 'standard_azurefrontdoor', 'premium_azurefrontdoor',
                    'standard_955bandwidth_chinacdn', 'standard_avgbandwidth_chinacdn', 'standardplus_chinacdn',
                    'standardplus_955bandwidth_chinacdn', 'standardplus_avgbandwidth_chinacdn'
                ]
            ),
            identity=dict(
                type="dict",
                options=self.managed_identity_multiple_spec
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.tags = None
        self.sku = None
        self.identity = None
        self._managed_identity = None

        required_if = [
            ('state', 'present', ['sku'])
        ]

        self.results = dict(changed=False)

        super(AzureRMCdnprofile, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True,
                                                required_if=required_if)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {
                "identity": ManagedServiceIdentity,
                "user_assigned": UserAssignedIdentity,
            }
        return self._managed_identity

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        to_be_updated = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        response = self.get_cdnprofile()

        if self.state == 'present':

            curr_identity = response["identity"] if response else None
            update_identity = False
            if self.identity:
                update_identity, self.identity = self.update_managed_identity(curr_identity=curr_identity, new_identity=self.identity, patch_support=True)

            if not response:
                self.log("Need to create the CDN profile")

                if not self.check_mode:
                    new_response = self.create_cdnprofile()
                    self.results['id'] = new_response['id']

                self.results['changed'] = True

            else:
                self.log('Results : {0}'.format(response))
                update_tags, response['tags'] = self.update_tags(response['tags'])

                if response['provisioning_state'] == "Succeeded":
                    if update_tags or update_identity:
                        to_be_updated = True

                if to_be_updated:
                    self.log("Need to update the CDN profile")

                    if not self.check_mode:
                        new_response = self.update_cdnprofile()
                        self.results['id'] = new_response['id']

                    self.results['changed'] = True

        elif self.state == 'absent':
            if not response:
                self.fail("CDN profile {0} not exists.".format(self.name))
            else:
                self.log("Need to delete the CDN profile")
                self.results['changed'] = True

                if not self.check_mode:
                    self.delete_cdnprofile()
                    self.results['id'] = response['id']

        return self.results

    def create_cdnprofile(self):
        '''
        Creates a Azure CDN profile.

        :return: deserialized Azure CDN profile instance state dictionary
        '''
        self.log("Creating the Azure CDN profile instance {0}".format(self.name))

        parameters = Profile(
            location=self.location,
            sku=Sku(name=self.sku),
            tags=self.tags,
            identity=self.identity
        )

        xid = str(uuid.uuid1())

        try:
            poller = self.cdn_client.profiles.begin_create(self.resource_group,
                                                           self.name,
                                                           parameters)
            response = self.get_poller_result(poller)
            return cdnprofile_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create Azure CDN profile instance.')
            self.fail("Error Creating Azure CDN profile instance: {0}".format(exc.message))

    def update_cdnprofile(self):
        '''
        Updates a Azure CDN profile.

        :return: deserialized Azure CDN profile instance state dictionary
        '''
        self.log("Updating the Azure CDN profile instance {0}".format(self.name))

        try:
            parameters = ProfileUpdateParameters(
                tags=self.tags,
                identity=self.identity
            )
            poller = self.cdn_client.profiles.begin_update(
                self.resource_group,
                self.name,
                parameters
            )
            response = self.get_poller_result(poller)
            return cdnprofile_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to update Azure CDN profile instance.')
            self.fail("Error updating Azure CDN profile instance: {0}".format(exc.message))

    def delete_cdnprofile(self):
        '''
        Deletes the specified Azure CDN profile in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the CDN profile {0}".format(self.name))
        try:
            poller = self.cdn_client.profiles.begin_delete(
                self.resource_group, self.name)
            self.get_poller_result(poller)
            return True
        except Exception as e:
            self.log('Error attempting to delete the CDN profile.')
            self.fail("Error deleting the CDN profile: {0}".format(e.message))
            return False

    def get_cdnprofile(self):
        '''
        Gets the properties of the specified CDN profile.

        :return: deserialized CDN profile state dictionary
        '''
        self.log(
            "Checking if the CDN profile {0} is present".format(self.name))
        try:
            response = self.cdn_client.profiles.get(self.resource_group, self.name)
            self.log("Response : {0}".format(response))
            self.log("CDN profile : {0} found".format(response.name))
            return cdnprofile_to_dict(response)
        except Exception:
            self.log('Did not find the CDN profile.')
            return False


def main():
    """Main execution"""
    AzureRMCdnprofile()


if __name__ == '__main__':
    main()

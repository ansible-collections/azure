#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.rulesetsoperations?view=azure-python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_afdruleset
version_added: "3.4.0"
short_description: Manage an Azure Front Door Rule Set
description:
    - Create, update and delete an Azure Front Door Rule Set to be used by a Front Door Service Profile created using azure_rm_cdnprofile.

options:
    name:
        description:
            - Name of the Front Door Rule Set.
        required: true
        type: str
    profile_name:
        description:
            - Name of the Front Door Profile.
        required: true
        type: str
    resource_group:
        description:
            - Name of a resource group where the CDN front door ruleset exists or will be created.
        required: true
        type: str
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

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Create a Ruleset
  azure_rm_afdruleset:
    name: myRuleset
    profile_name: myProfile
    resource_group: myResourceGroup
    state: present

- name: Delete a Ruleset
  azure_rm_afdruleset:
    name: myRuleset
    profile_name: myProfile
    resource_group: myResourceGroup
    state: absent
'''
RETURN = '''
id:
    description: Resource ID
    returned: always
    type: str
    example: "/subscriptions/xxxxxx-xxxx-xxxx-xxxx-xxxxxxx/resourcegroups/myRG/providers/Microsoft.Cdn/profiles/myProf/rulesets/myRS"
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMRuleSet(AzureRMModuleBase):
    """Class representing a Ruleset for Azure Frontdoor Standard or Premium"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent'],
                required=False
            )
        )

        self.name = None
        self.profile_name = None
        self.resource_group = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMRuleSet, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        response = self.get_ruleset()

        self.results['changed'] = False
        self.results['id'] = None

        if self.state == 'present':

            if not response:
                self.log("Need to create the Rule Set")
                if not self.check_mode:
                    new_response = self.create_ruleset()
                    self.results['id'] = new_response['id']

                self.results['changed'] = True

            else:
                self.results['id'] = response['id']
                self.log('Results : {0}'.format(response))

        elif self.state == 'absent':
            if not response:
                self.log("Rule Set {0} does not exist.".format(self.name))
            else:
                self.log("Need to delete the Rule Set")
                self.results['changed'] = True

                self.results['id'] = response['id']
                if not self.check_mode:
                    self.delete_ruleset()

        return self.results

    def create_ruleset(self):
        '''
        Creates an Azure Rule Set.

        :return: deserialized Azure Rule Set instance state dictionary
        '''
        self.log("Creating the Azure Rule Set instance {0}".format(self.name))

        try:
            response = self.cdn_client.rule_sets.create(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.name
            )
            return ruleset_to_dict(response)
        except AttributeError as exc:
            self.fail("Please ensure azure-mgmt-cdn is upgraded to version 13.1.0 or greater: {0}".format(str(exc)))
        except Exception as exc:
            self.log('Error attempting to create Azure Rule Set instance.')
            self.fail("Error Creating Azure Rule Set instance: {0}".format(str(exc)))

    def delete_ruleset(self):
        '''
        Deletes the specified Azure Rule Set in the specified subscription and resource group.

        :return: bool
        '''
        self.log("Deleting the Rule Set {0}".format(self.name))
        try:
            poller = self.cdn_client.rule_sets.begin_delete(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.name)
            self.get_poller_result(poller)
            return True
        except Exception as exc:
            self.log('Error attempting to delete the Rule Set.')
            self.fail("Error deleting the Rule Set: {0}".format(str(exc)))
            return False

    def get_ruleset(self):
        '''
        Gets the properties of the specified Rule Set.

        :return: deserialized Rule Set state dictionary
        '''
        self.log(
            "Checking if the Rule Set {0} is present".format(self.name))
        try:
            response = self.cdn_client.rule_sets.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.name,
            )
            self.log("Response : {0}".format(response))
            self.log("Rule Set : {0} found".format(response.name))
            return ruleset_to_dict(response)
        except Exception as err:
            self.log('Did not find the Rule Set.' + err.args[0])
            return False


def ruleset_to_dict(ruleset):
    '''
    Sets the properties of the specified Rule Set.

    :return: deserialized Rule Set state dictionary
    '''
    return dict(
        deployment_status=ruleset.deployment_status,
        id=ruleset.id,
        name=ruleset.name,
        provisioning_state=ruleset.provisioning_state,
        type=ruleset.type
    )


def main():
    """Main execution"""
    AzureRMRuleSet()


if __name__ == '__main__':
    main()

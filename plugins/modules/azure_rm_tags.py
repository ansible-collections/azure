#!/usr/bin/python
#
# Copyright (c) 2025 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_tags
version_added: "4.0.0"
short_description: Manage tags.
description:
    - Create, update or delete the vm public key.
options:
    state:
        description:
            - State of the SSH Public Key. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create a new tags with scope
  azure_rm_tags:
    scope: "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/v-xisuRG02"
    properties:
      tags:
        key4: value4

- name: Update the tags with scope
  azure_rm_tags:
    scope: "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/v-xisuRG02"
    tags_patch:
       operation: Delete
         properties:
           tags:
             key5: value7

'''
RETURN = '''
tag_info:
    description:
        - The tag info.
    returned: when I(scope=None)
    type: complex
    contains:
        id:
            description:
                - The ID of the tags wrapper resource.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Resources/tags/default"
        name:
            description:
                - The name of the tags wrapper resource.
            returned: always
            type: str
            sample: default
        type:
            description:
                - The type of the tags wrapper resource.
            returned: always
            type: str
            sample: Microsoft.Resources/tags
        properties:
            description:
                - The set of tags.
            returned: always
            type: dict
            sample: { 'tags': {'key1': 'value1', 'key2': 'value2'}}
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from azure.core.polling import LROPoller
import copy
import logging
logging.basicConfig(filename='log.log', level=logging.INFO)

class AzureRMTags(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            tag_name=dict(type='str'),
            tag_value=dict(type='str'),
            scope=dict(type='str'),
            properties=dict(
                type='dict',
                options=dict(
                    tags=dict(type='dict')
                )
            ),
            tags_patch=dict(
                type='dict',
                options=dict(
                    operation=dict(type='str', required=True, choices=['Replace', 'Merge', 'Delete']),
                    properties=dict(
                        type='dict',
                        required=True,
                        options=dict(
                            tags=dict(type='dict')
                        )
                    )
                )
            ),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.tag_name = None
        self.tag_value = None
        self.scope = None
        self.properties = None
        self.tags_patch = None
        self.state = None

        self.results = dict(
            changed=False,
            tag_info=dict()
        )

        super(AzureRMTags, self).__init__(self.module_arg_spec,
                                          supports_tags=True,
                                          supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        changed = False
        if self.state == 'present':
            if self.scope is not None:
                response = self.get_at_scope()
                if response['properties']['tags']:
                    if self.tags_patch is not None:
                        update_tags = self.tags_update(response['properties']['tags'], self.tags_patch['properties'].get('tags'))
                        if update_tags:
                            changed = True
                            response = self.begin_update_at_scope(self.tags_patch)
                        elif self.tags_patch['operation'] == 'Delete':
                            changed = True
                            response = self.begin_update_at_scope(self.tags_patch)
                else:
                    if self.properties is not None:
                        changed = True
                        response = self.begin_create_or_update_at_scope(self.properties)
            else:
                if self.tag_name is not None and self.tag_value is not None:
                    response = self.create_or_update_value()
                elif self.tag_name is not None:
                    response = self.create_or_update()
                else:
                    self.fail("If I(scope!=None), The tag_name, or tag_name and tag_value must be configured")
        else:
            changed = True
            if self.scope is not None:
                response = self.delete_at_scope()
            elif self.tag_name is not None and self.tag_value is not None:
                response = self.delete_value()
            elif self.tag_name is not None:
                response = self.delete_tags()
            else:
                self.fail("When I(state=absent), scope, tag_name, or tag_name and tag_value must be configured")

        self.results['changed'] = changed
        self.results['tag_info'] = response

        return self.results

    def begin_create_or_update_at_scope(self, properties):
        self.log('Creates or updates the entire set of tags on a resource or subscription.')
        try:
            response = self.rm_client.tags.begin_create_or_update_at_scope(self.scope, dict(properties=properties))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Creates or updates the entire set of tags on a resource or subscription got Exception as as {0}'.format(exc.message or str(exc)))
        return self.format_tags(response)

    def begin_update_at_scope(self, tags_patch):
        self.log('Selectively updates the set of tags on a resource or subscription.')
        try:
            response = self.rm_client.tags.begin_update_at_scope(self.scope, tags_patch)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Selectively updates the set of tags on a resource or subscription got Excption as {0}'.format(exc.message or str(exc)))

        return self.format_tags(response)

    def create_or_update_value(self):
        self.log('Creates a predefined value for a predefined tag name.')
        try:
            results = self.rm_client.tags.create_or_update_value(self.tag_name, self.tag_value)
        except Exception as exc:
            self.fail('Creates a predefined value for a predefined tag name got Excetion as {0}'.format(exc.message or str(exc)))

        return results

    def create_or_update(self):
        self.log('Creates a predefined tag name.')
        try:
            results = self.rm_client.tags.create_or_update(self.tag_name)
        except Exception as exc:
            self.fail('Creates a predefined tag name got Excetion as {0}'.format(exc.message or str(exc)))

        return results.as_dict()

    def delete_at_scope(self):
        self.log('Deletes the entire set of tags on a resource or subscription.')
        try:
            self.rm_client.tags.begin_delete_at_scope(self.scope)
        except Exception as exc:
            self.fail('Delete the entire set of tag got Excetion as {0}'.format(exc.message or str(exc)))

    def delete_value(self):
        self.log('Deletes a predefined tag value for a predefined tag name {0} and value {1}'.format(self.tag_name, self.tag_value))
        try:
            self.rm_client.tags.delete_value(self.tag_name, self.tag_value)
        except Exception as exc:
            self.fail('Delete the predefined tag value got Excetion as {0}'.format(exc.message or str(exc)))

    def delete_tags(self):
        self.log('Delete a predefined tag name {0}'.format(self.tag_name))
        try:
            self.rm_client.tags.delete(self.tag_name)
        except Exception as exc:
            self.fail('Delete the predefined tag name got Excetion as {0}'.format(exc.message or str(exc)))

    def get_at_scope(self):
        self.log('Get properties for {0}'.format(self.scope))
        try:
            response = self.rm_client.tags.get_at_scope(self.scope)
            if response is not None:
                return self.format_tags(response)
        except Exception as exc:
            self.fail('Error when get the tags info under specified scope got Excetion as {0}'.format(exc.message or str(exc)))

    def list_all(self):
        self.log('List resources under resource group')
        results = []
        try:
            response = self.rm_client.tags.list()
            while True:
                results.append(response.next().as_dict())
        except StopIteration:
            pass
        except Exception as exc:
            self.fail('Error when listing all tags under subscription got Excetion as {0}'.format(exc.message or str(exc)))
        return results

    def format_tags(self, tags):
        results = dict(
            id=tags.id,
            name=tags.name,
            type=tags.type,
            properties=dict()
        )
        if tags.properties is not None:
            results['properties'] = tags.properties.as_dict()

        return results

    def tags_update(self, old, new):
        tags = old or dict()
        new_tags = copy.copy(tags) if isinstance(tags, dict) else dict()
        param_tags = new if isinstance(new, dict) else dict()
        changed = False
        # check add or update
        for key, value in param_tags.items():
            if not new_tags.get(key) or new_tags[key] != value:
                changed = True
                new_tags[key] = value
        return changed

def main():
    AzureRMTags()


if __name__ == '__main__':
    main()

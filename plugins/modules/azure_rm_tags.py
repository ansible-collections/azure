#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_tags
version_added: "3.5.0"
short_description: Manage tags
description:
    - Create, update ,delete and replace the tags.
options:
    scope:
        description:
            - The resource scope.
        type: str
        required: True
    operation:
        description:
            - The operation type for the patch API.
            - The default value is I(operation=Merge) and use to add tags.
        type: str
        default: Merge
        choices:
            - Delete
            - Replace
            - Merge
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
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create a new tags with scope
  azure_rm_tags:
    scope: "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/v-xisuRG02"
    tags:
      key1: value1

- name: Update the tags with scope
  azure_rm_tags:
    scope: "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/v-xisuRG02"
    operation: Merge
    tags:
      key2: value2

- name: Delete the tags by scope
  azure_rm_tags:
    scope: "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/v-xisuRG02"
    state: absent
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


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTags(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            scope=dict(type='str', required=True),
            operation=dict(type='str', choices=['Replace', 'Merge', 'Delete'], default='Merge'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.scope = None
        self.operation = None
        self.tags = None
        self.state = None

        self.results = dict(
            changed=False,
            tag_info=dict()
        )

        super(AzureRMTags, self).__init__(self.module_arg_spec,
                                          supports_tags=True,
                                          supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        if self.state == 'present':
            response = self.get_at_scope()
            if response and response['properties'].get('tags'):
                merge_tag, delete_tag, replace_tag = self.tags_update(response['properties']['tags'], self.tags)

                if (self.operation == 'Merge' and merge_tag) or (self.operation == 'Replace' and replace_tag) or (delete_tag and self.operation == 'Delete'):
                    changed = True
                    response = self.begin_update_at_scope(self.tags, self.operation)
            else:
                if self.tags:
                    changed = True
                    response = self.begin_create_or_update_at_scope(self.tags)
        else:
            response = self.get_at_scope()
            if response['properties']['tags']:
                changed = True
                response = self.delete_at_scope()

        self.results['changed'] = changed
        self.results['tag_info'] = response

        return self.results

    def begin_create_or_update_at_scope(self, tags):
        self.log('Creates or updates the entire set of tags on a resource or subscription.')
        try:
            response = self.rm_client.tags.begin_create_or_update_at_scope(self.scope,
                                                                           dict(properties=dict(tags=tags)))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Creates or updates the entire set of tags on a resource or subscription got Exception as as {0}'.format(exc.message or str(exc)))
        return self.format_tags(response)

    def begin_update_at_scope(self, tags, operation):
        self.log('Selectively updates the set of tags on a resource or subscription.')
        try:
            response = self.rm_client.tags.begin_update_at_scope(self.scope,
                                                                 dict(operation=operation, properties=dict(tags=tags)))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Selectively updates the set of tags on a resource or subscription got Excption as {0}'.format(exc.message or str(exc)))

        return self.format_tags(response)

    def delete_at_scope(self):
        self.log('Deletes the entire set of tags on a resource or subscription.')
        try:
            self.rm_client.tags.begin_delete_at_scope(self.scope)
        except Exception as exc:
            self.fail('Delete the entire set of tag got Excetion as {0}'.format(exc.message or str(exc)))

    def get_at_scope(self):
        self.log('Get properties for {0}'.format(self.scope))
        try:
            response = self.rm_client.tags.get_at_scope(self.scope)
            if response is not None:
                return self.format_tags(response)
        except Exception as exc:
            self.fail('Error when get the tags info under specified scope got Excetion as {0}'.format(exc.message or str(exc)))

    def format_tags(self, tags):
        results = dict(
            id=tags.id,
            name=tags.name,
            type=tags.type,
            properties=dict()
        )
        if tags.properties:
            results['properties'] = tags.properties.as_dict()

        return results

    def tags_update(self, old, new):
        old = old or dict()
        new = new or dict()
        merge_tag = not set(new.items()).issubset(set(old.items()))
        replace_tag = True
        if not merge_tag and len(old) == len(new):
            replace_tag = False
        delete_tag = False
        for key, value in new.items():
            if old.get(key) and old.get(key) == value:
                delete_tag = True
                break
        return merge_tag, delete_tag, replace_tag


def main():
    AzureRMTags()


if __name__ == '__main__':
    main()

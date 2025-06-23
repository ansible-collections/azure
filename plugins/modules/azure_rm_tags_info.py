#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_tags_info

version_added: "3.5.0"

short_description: List tags facts

description:
    - List all tag details under subscription_id.
    - Get the tag info at the specified scope.

options:
    scope:
        description:
            - The resource scope.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get the tag info at thespecified resource
  azure_rm_tags_info:
    scope: scope_str

- name: List all tag details under subscription
  azure_rm_tags_info:
'''
RETURN = '''
tag_details:
    description:
        - List tag details.
    returned: when I(scope!=None)
    type: complex
    contains:
        id:
            description:
                - The tag name ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/tagNames/k1"
        tag_name:
            description:
                - The tag name.
            returned: always
            type: str
            sample: K1
        count:
            description:
                - The total number of resources that use the resource tag.
                -  When a tag is initially created and has no associated resources, the value is 0.
            returned: always
            type: dict
            sample: { 'type': 'Total', 'value': 1}
        values:
            description:
                - The list of tag values.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - The tag value ID.
                    returned: always
                    type: str
                    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/tagNames/key2/tagValues/v1"
                tag_value:
                    description:
                        - The tag value.
                    returned: always
                    type: str
                    sample: V1
                count:
                    description:
                        - The tag value count
                    returned: always
                    type: dict
                    sample: {'type': 'totoal', 'value': 1}
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


AZURE_OBJECT_CLASS = 'Tags'


class AzureRMTagsInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            scope=dict(type='str'),
        )

        self.results = dict(
            changed=False,
            tags_detail=[],
            tag_info=None
        )

        self.scope = None

        super(AzureRMTagsInfo, self).__init__(self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False,
                                              facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.scope:
            self.results['tag_info'] = self.get_at_scope(self.scope)
        else:
            self.results['tag_details'] = self.list_all()

        return self.results

    def get_at_scope(self, scope):
        self.log('Get properties for {0}'.format(self.scope))
        results = []
        try:
            response = self.rm_client.tags.get_at_scope(scope)
            if response:
                results.append(self.format_tags(response))
        except StopIteration:
            pass
        except Exception as exc:
            self.fail('Error when get the tags info under specified scope got Excetion as {0}'.format(exc.message or str(exc)))
        return results

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
        if tags.properties:
            results['properties'] = tags.properties.as_dict()

        return results


def main():
    AzureRMTagsInfo()


if __name__ == '__main__':
    main()

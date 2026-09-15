#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_servicebusrule_info

version_added: "4.1.0"

short_description: Get Azure Service Bus subscription rule facts

description:
    - Get facts of a specific Azure Service Bus topic subscription rule or all rules of a subscription.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    namespace:
        description:
            - Servicebus namespace name.
        required: true
        type: str
    topic:
        description:
            - Topic name which the subscription belongs to.
        required: true
        type: str
    subscription:
        description:
            - Subscription name which the rule belongs to.
        required: true
        type: str
    name:
        description:
            - Limit results to a specific rule.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get facts of a specific rule
  azure_rm_servicebusrule_info:
    resource_group: myResourceGroup
    namespace: bar
    topic: subtopic
    subscription: sbsub
    name: sqlrule

- name: Get facts of all rules in a subscription
  azure_rm_servicebusrule_info:
    resource_group: myResourceGroup
    namespace: bar
    topic: subtopic
    subscription: sbsub
'''

RETURN = '''
rules:
    description:
        - A list of Service Bus subscription rules.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Current state of the rule.
            returned: always
            type: str
            sample: "/subscriptions/xxx...xxx/resourceGroups/myResourceGroup/providers/Microsoft.ServiceBus/
                    namespaces/nsb57dc95979/topics/topicb57dc95979/subscriptions/subsb57dc95979/rules/rule57dc95979"
        name:
            description:
                - Name of the rule.
            returned: always
            type: str
            sample: sqlrule
        filter_type:
            description:
                - The type of filter expression evaluated against a message.
            returned: always
            type: str
            sample: SqlFilter
        sql_filter:
            description:
                - The SQL expression, when I(filter_type=SqlFilter).
            returned: always
            type: str
            sample: "myproperty='ABC'"
        correlation_filter:
            description:
                - Properties of the correlation filter, when I(filter_type=CorrelationFilter).
            returned: always
            type: dict
            sample: {'label': 'red'}
            contains:
                correlation_id:
                    description:
                        - Identifier of the correlation.
                    returned: always
                    type: str
                    sample: null
                message_id:
                    description:
                        - Identifier of the message.
                    returned: always
                    type: str
                    sample: null
                to:
                    description:
                        - Address to send to.
                    returned: always
                    type: str
                    sample: null
                reply_to:
                    description:
                        - Address of the queue to reply to.
                    returned: always
                    type: str
                    sample: null
                label:
                    description:
                        - Application specific label.
                    returned: always
                    type: str
                    sample: red
                session_id:
                    description:
                        - Session identifier.
                    returned: always
                    type: str
                    sample: null
                reply_to_session_id:
                    description:
                        - Session identifier to reply to.
                    returned: always
                    type: str
                    sample: null
                content_type:
                    description:
                        - Content type of the message.
                    returned: always
                    type: str
                    sample: null
                properties:
                    description:
                        - Dictionary object for custom filters.
                    returned: always
                    type: dict
                    sample: null
        action:
            description:
                - SQL expression run against a message that has been matched by the filter.
            returned: always
            type: str
            sample: "SET sys.label = 'X'"
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


correlation_filter_keys = (
    'correlation_id', 'message_id', 'to', 'reply_to', 'label',
    'session_id', 'reply_to_session_id', 'content_type', 'properties',
)


class AzureRMServiceBusRuleInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            namespace=dict(type='str', required=True),
            topic=dict(type='str', required=True),
            subscription=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.resource_group = None
        self.namespace = None
        self.topic = None
        self.subscription = None
        self.name = None

        self.results = dict(changed=False)

        super(AzureRMServiceBusRuleInfo, self).__init__(self.module_arg_spec,
                                                        supports_tags=False,
                                                        supports_check_mode=True,
                                                        facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['rules'] = self.get_item()
        else:
            self.results['rules'] = self.list_items()

        return self.results

    def get_item(self):
        try:
            item = self.servicebus_client.rules.get(self.resource_group, self.namespace, self.topic, self.subscription, self.name)
            return [self.to_dict(item)]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error getting servicebus rule {0} - {1}".format(self.name, str(exc)))

    def list_items(self):
        try:
            items = self.servicebus_client.rules.list_by_subscriptions(self.resource_group, self.namespace, self.topic, self.subscription)
            return [self.to_dict(item) for item in items]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error listing servicebus rules - {0}".format(str(exc)))

    def to_dict(self, item):
        result = dict(
            id=item.id,
            name=item.name,
            filter_type=item.filter_type,
            sql_filter=item.sql_filter.sql_expression if item.sql_filter else None,
            correlation_filter=None,
            action=item.action.sql_expression if item.action else None,
        )
        if item.correlation_filter:
            result['correlation_filter'] = {key: getattr(item.correlation_filter, key, None) for key in correlation_filter_keys}
        return result


def main():
    AzureRMServiceBusRuleInfo()


if __name__ == '__main__':
    main()

#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_servicebusrule

version_added: "4.1.0"

short_description: Manage Azure Service Bus subscription rule

description:
    - Create, update or delete an Azure Service Bus topic subscription rule.

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
            - Name of the rule.
        required: true
        type: str
    state:
        description:
            - Assert the state of the rule. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    filter_type:
        description:
            - The type of filter expression evaluated against a message.
            - Required when I(state=present).
        type: str
        choices:
            - sql_filter
            - correlation_filter
    sql_filter:
        description:
            - The SQL expression, for example I(sql_filter="myproperty='ABC'").
            - Required when I(filter_type=sql_filter).
        type: str
    correlation_filter:
        description:
            - Properties of the correlation filter.
            - Required when I(filter_type=correlation_filter).
            - At least one suboption must be set.
        type: dict
        suboptions:
            correlation_id:
                description:
                    - Identifier of the correlation.
                type: str
            message_id:
                description:
                    - Identifier of the message.
                type: str
            to:
                description:
                    - Address to send to.
                type: str
            reply_to:
                description:
                    - Address of the queue to reply to.
                type: str
            label:
                description:
                    - Application specific label.
                type: str
            session_id:
                description:
                    - Session identifier.
                type: str
            reply_to_session_id:
                description:
                    - Session identifier to reply to.
                type: str
            content_type:
                description:
                    - Content type of the message.
                type: str
            properties:
                description:
                    - Dictionary object for custom filters.
                type: dict
    action:
        description:
            - SQL expression run against a message that has been matched by the filter, for example I(action="SET sys.label = 'X'").
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a rule with a SQL filter
  azure_rm_servicebusrule:
    resource_group: myResourceGroup
    namespace: bar
    topic: subtopic
    subscription: sbsub
    name: sqlrule
    filter_type: sql_filter
    sql_filter: "myproperty='ABC'"

- name: Create a rule with a correlation filter
  azure_rm_servicebusrule:
    resource_group: myResourceGroup
    namespace: bar
    topic: subtopic
    subscription: sbsub
    name: correlationrule
    filter_type: correlation_filter
    correlation_filter:
      label: red
      content_type: application/text

- name: Delete a rule
  azure_rm_servicebusrule:
    resource_group: myResourceGroup
    namespace: bar
    topic: subtopic
    subscription: sbsub
    name: sqlrule
    state: absent
'''

RETURN = '''
id:
    description:
        - Current state of the rule.
    returned: success
    type: str
    sample: "/subscriptions/xxx...xxx/resourceGroups/myResourceGroup/providers/Microsoft.ServiceBus/
            namespaces/nsb57dc95979/topics/topicb57dc95979/subscriptions/subsb57dc95979/rules/rule57dc95979"
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


filter_type_map = dict(
    sql_filter='SqlFilter',
    correlation_filter='CorrelationFilter',
)


correlation_filter_keys = (
    'correlation_id', 'message_id', 'to', 'reply_to', 'label',
    'session_id', 'reply_to_session_id', 'content_type', 'properties',
)


class AzureRMServiceBusRule(AzureRMModuleBase):

    def __init__(self):

        correlation_filter_spec = dict(
            correlation_id=dict(type='str'),
            message_id=dict(type='str'),
            to=dict(type='str'),
            reply_to=dict(type='str'),
            label=dict(type='str'),
            session_id=dict(type='str'),
            reply_to_session_id=dict(type='str'),
            content_type=dict(type='str'),
            properties=dict(type='dict'),
        )

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            namespace=dict(type='str', required=True),
            topic=dict(type='str', required=True),
            subscription=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            filter_type=dict(type='str', choices=['sql_filter', 'correlation_filter']),
            sql_filter=dict(type='str'),
            correlation_filter=dict(type='dict', options=correlation_filter_spec),
            action=dict(type='str'),
        )

        self.resource_group = None
        self.namespace = None
        self.topic = None
        self.subscription = None
        self.name = None
        self.state = None
        self.filter_type = None
        self.sql_filter = None
        self.correlation_filter = None
        self.action = None

        self.results = dict(
            changed=False,
            id=None
        )

        required_if = [
            ('state', 'present', ['filter_type']),
            ('filter_type', 'sql_filter', ['sql_filter']),
            ('filter_type', 'correlation_filter', ['correlation_filter']),
        ]

        super(AzureRMServiceBusRule, self).__init__(self.module_arg_spec,
                                                    supports_tags=False,
                                                    supports_check_mode=True,
                                                    mutually_exclusive=[('sql_filter', 'correlation_filter')],
                                                    required_if=required_if)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        changed = False
        original = self.get()

        if self.state == 'present':
            params = dict(filter_type=filter_type_map[self.filter_type])
            if self.filter_type == 'sql_filter':
                params['sql_filter'] = self.servicebus_models.SqlFilter(sql_expression=self.sql_filter)
            else:
                params['correlation_filter'] = self.servicebus_models.CorrelationFilter(**self.correlation_filter)
            if self.action:
                params['action'] = self.servicebus_models.Action(sql_expression=self.action)

            instance = self.servicebus_models.Rule(**params)

            if not original:
                changed = True
            elif self.has_changed(original, instance):
                changed = True

            if changed and not self.check_mode:
                original = self.create_or_update(instance)
        elif original:
            changed = True
            if not self.check_mode:
                self.delete()
                original = None

        self.results['changed'] = changed
        if original:
            self.results['id'] = original.id
        return self.results

    def has_changed(self, original, instance):
        if original.filter_type != instance.filter_type:
            return True

        if instance.filter_type == filter_type_map['sql_filter']:
            existing_expression = original.sql_filter.sql_expression if original.sql_filter else None
            if existing_expression != self.sql_filter:
                return True
        else:
            for key in correlation_filter_keys:
                desired_value = self.correlation_filter.get(key)
                if getattr(original.correlation_filter, key, None) != desired_value:
                    return True

        existing_action = original.action.sql_expression if original.action else None
        if existing_action != self.action:
            return True

        return False

    def get(self):
        try:
            return self.servicebus_client.rules.get(self.resource_group, self.namespace, self.topic, self.subscription, self.name)
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error getting servicebus rule {0} - {1}".format(self.name, str(exc)))

    def create_or_update(self, param):
        try:
            return self.servicebus_client.rules.create_or_update(self.resource_group, self.namespace, self.topic,
                                                                 self.subscription, self.name, param)
        except Exception as exc:
            self.fail("Error creating or updating servicebus rule {0} - {1}".format(self.name, str(exc)))

    def delete(self):
        try:
            self.servicebus_client.rules.delete(self.resource_group, self.namespace, self.topic, self.subscription, self.name)
        except Exception as exc:
            self.fail("Error deleting servicebus rule {0} - {1}".format(self.name, str(exc)))


def main():
    AzureRMServiceBusRule()


if __name__ == '__main__':
    main()

#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_eventgrid_topic
version_added: "3.13.0"
short_description: Manage Eventgrid Topics
description:
    - Create, update ,delete and replace Eventgrid Topics.
options:
    name:
        description:
            - Name of the topic.
        required: true
        type: str
    resource_group:
        description:
            - Name of a resource group where the topic exists or will be created.
        required: true
        type: str
    location:
        description:
            - Valid azure location. Defaults to location of the resource group.
        type: str
    input_schema:
        description:
            - Schema in which incoming events will be published to this topic/domain.
              If you specify CustomEventSchema as the value for this parameter, you must
              also provide values for at least one of input_mapping_default_values /
              input_mapping_fields.
        type: str
        choices:
            - CloudEventSchemaV1_0
            - CustomEventSchema
            - EventGridSchema
        default: EventGridSchema
    input_mapping_default_values:
        description:
            - When input_schema is specified as CustomEventSchema, this parameter can be
              used to specify input mappings based on default values. You can use this
              parameter when your custom schema does not include a field that corresponds
              to one of the three fields supported by this parameter.
        type: list
        elements: dict
        suboptions:
            mapping_key:
                description:
                    - Parameter name
                type: str
                choices:
                    - subject
                    - eventtype
                    - dataversion
            mapping_value:
                description:
                    - Default value to use for Parameter when not in publish event.
                type: str
    input_mapping_fields:
        description:
            - When input_schema is specified as CustomEventSchema, this parameter is used
              to specify input mappings based on field names.
        type: list
        elements: dict
        suboptions:
            mapping_key:
                description:
                    - Parameter name
                type: str
                choices:
                    - id
                    - topic
                    - eventtime
                    - subject
                    - eventtype
                    - dataversion
            mapping_value:
                description:
                    - Corresponding value should specify the name of the field in the custom
                      input schema.  If a mapping for either 'id' or 'eventtime' is not
                      provided, Event Grid will auto-generate a default value for these two
                      fields.
                type: str
    inbound_ip_rules:
        description:
            - List of inbound IP rules
        required: false
        type: list
        default: []
        elements: dict
        suboptions:
            ipmask:
                description:
                    - IP Address in CIDR notation e.g., 10.0.0.0/8
                type: str
            action:
                description:
                    - Action to perform based ont the match or no match of the IpMask.
                type: str
                choices:
                    - Allow
                    - Deny
    public_network_access:
        description:
            - This determines if traffic is allowed over public network.
        choices:
            - enabled
            - disabled
        type: str
        default: enabled
    identity:
        description:
            - Identity for the Server.
        type: dict
        suboptions:
            type:
                description:
                    - Type of the managed identity
                choices:
                    - UserAssigned
                    - SystemAssigned
                    - SystemAssigned UserAssigned
                    - None
                default: SystemAssigned
                type: str
            user_assigned_identities:
                description:
                    - User Assigned Managed Identity
                type: list
                elements: str
    kind:
        description:
            - The kind of topic resource.
        default: Azure
        type: str
        choices:
            - Azure
            - AzureArc
    extended_location_name:
        description:
            - The extended location name.
            - Required if I(kind=AzureArc).
        type: str
    extended_location_type:
        description:
            - The extended location type.
            - Required if I(kind=AzureArc).
        type: str
        choices:
            - customlocation
    state:
        description:
            - State of the Eventgrid Topic. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    regenerate_keys:
        description:
            - if C(present) and topic exsists (ie update action) this will force
              the listed key to be regeneratd. This cannot be idempotent. Everytime
              this is called it will regenerate the key(s).
        type: list
        elements: str
        choices:
            - key1
            - key2

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a new Topic
  azure.azcollection.azure_rm_eventgrid_topic:
    resource_group: rg1
    name: topic1
    location: westus2

- name: Create a new Topic with custom input mappings
  azure.azcollection.azure_rm_eventgrid_topic:
    resource_group: rg1
    name: topic1
    location: westus2
    input_schema: CustomEventSchema
    input_mapping_fields:
      - mapping_key: topic
        mapping_value: myTopicField
      - mapping_key: eventtype
        mapping_value: myEventTypeField
    input_mapping_default_values:
      - mapping_key: subject
        mapping_value: DefaultSubject
      - mapping_key: dataversion
        mapping_value: 1.0

- name: Create a new Topic that accepts events published in CloudEvents V1.0 schema
  azure.azcollection.azure_rm_eventgrid_topic:
    resource_group: rg1
    name: topic1
    location: westus2
    input_schema: CloudEventSchemaV1_0

- name: Create a new Topic which allows specific inbound ip rules with Basic Sku and system assigned
  azure.azcollection.azure_rm_eventgrid_topic:
    resource_group: rg1
    name: topic1
    location: westus2
    public_network_access: enabled
    inbound_ip_rules:
      - ipmask: 10.0.0.0/8
        action: Allow
      - ipmask: 10.2.0.0/8
        action: Allow
    identity:
      type: SystemAssigned

- name: Create a new topic in AzureArc targeting a custom location
  azure.azcollection.azure_rm_eventgrid_topic:
    resource_group: rg1
    name: topic1
    location: eastus2euap
    kind: azurearc
    extended_location_name: /subscriptions/<subid>/resourcegroups/<rgname>/providers/microsoft.extendedlocation/customlocations/<cust-loc-name>
    extended_location_type: customlocation
    input_schema: CloudEventSchemaV1_0

- name: Delete the topic
  azure.azcollection.azure_rm_eventgrid_topic:
    resource_group: rg1
    name: topic1
    state: absent
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: true
eventgrid_topic:
    description:
        - Eventgrid Topic.
    returned: always
    type: complex
    contains:
        data_residency_boundary:
            description:
                - Residncy boundary
            returned: always
            type: str
            sample: WithinGeopair
        disable_local_auth:
            description:
                - Whether local auth is disabled
            returned: always
            type: bool
            sample: false
        endpoint:
            description:
                - Rest API endpoint to use to post events
            returned: always
            type: str
            sample: https://myTopic-20070.westus3-1.eventgrid.azure.net/api/events
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.EventGrid/topics/myTopic
        inbound_ip_rules:
            description:
                - Rules for network access
            type: complex
            returned: when-enabled
            contains:
                action:
                    description:
                        - What action will be taken, Allow or Disallow
                    returned: always
                    type: str
                    sample: Allow
                ip_mask:
                    description:
                        - CIDR notation of the network to act on.
                    returned: always
                    type: str
                    sample: 10.0.0.0/8
        input_schema:
            description:
                - The input schema assigned to this Topic
            returned: always
            type: str
            sample: EventGridSchema
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: westus3
        metric_resource_id:
            description:
                - Metric Resource ID.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        minimum_tls_version_allowed:
            description:
                - The minimum TLS version allowed
            returned: always
            type: str
            sample: 1.0
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myTopic
        provisioning_state:
            description:
                - The provisioning state.
            returned: always
            type: str
            sample: Succeeded
        public_network_access:
            description:
                - Indicates if boot diagnostics are enabled.
            returned: always
            type: str
            sample: Enabled
        type:
            description:
                - Type of Eventgrid
            type: str
            returned: always
            sample: Microsoft.EventGrid/topics
        input_schema_mapping:
            description:
                - Custom input schema mapping
            type: str
            returned: when-enabled
            sample: |
                "data_version": {
                  "default_value": "1.0"
                },
                "event_time": {},
                "event_type": {
                  "source_field": "myEventTypeField"
                },
                "id": {},
                "input_schema_mapping_type": "Json",
                "subject": {
                  "default_value": "DefaultSubject"
                },
                "topic": {
                  "source_field": "myTopicField"
                }
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.mgmt.eventgrid import EventGridManagementClient
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

managed_identity_spec = dict(
    type=dict(
        type='str',
        default='SystemAssigned',
        choices=['SystemAssigned',
                 'UserAssigned',
                 'SystemAssigned UserAssigned',
                 'None'],
    ),
    user_assigned_identities=dict(
        type='list',
        elements='str'
    ),
)

input_mapping_default_values_spec = dict(
    mapping_key=dict(
        type='str',
        choices=['subject',
                 'eventtype',
                 'dataversion'],
    ),
    mapping_value=dict(
        type='str'
    ),
)

input_mapping_fields_spec = dict(
    mapping_key=dict(
        type='str',
        choices=['id',
                 'topic',
                 'eventtime',
                 'subject',
                 'eventtype',
                 'dataversion'],
    ),
    mapping_value=dict(
        type='str'
    ),
)

inbound_ip_rules_spec = dict(
    ipmask=dict(
        type='str'
    ),
    action=dict(
        type='str',
        choices=['Allow',
                 'Deny']
    )
)


class AzureRMEventgridTopic(AzureRMModuleBaseExt):

    @property
    def client(self):
        self.log('Getting client')
        if not self._client:
            self._client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        return self._client

    @property
    def models(self):
        self.log('Getting models')
        return self.client.topics.models

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            input_schema=dict(
                type='str',
                default='EventGridSchema',
                choices=['CloudEventSchemaV1_0', 'CustomEventSchema', 'EventGridSchema']
            ),
            input_mapping_default_values=dict(
                type='list',
                elements='dict',
                options=input_mapping_default_values_spec,
                required_together=[('mapping_key', 'mapping_value')],
            ),
            input_mapping_fields=dict(
                type='list',
                elements='dict',
                options=input_mapping_fields_spec,
                required_together=[('mapping_key', 'mapping_value')],
            ),
            inbound_ip_rules=dict(
                type='list',
                default=[],
                elements='dict',
                options=inbound_ip_rules_spec,
                required_together=[('ipmask', 'action')],
            ),
            public_network_access=dict(
                type='str',
                default='enabled',
                choices=['enabled', 'disabled']
            ),
            identity=dict(
                type='dict',
                options=managed_identity_spec
            ),
            kind=dict(
                type='str',
                default='Azure',
                choices=['Azure', 'AzureArc']
            ),
            extended_location_name=dict(
                type='str'
            ),
            extended_location_type=dict(
                type='str',
                choices=['customlocation']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            regenerate_keys=dict(
                type='list',
                elements='str',
                choices=['key1', 'key2']
            ),
        )

        self._client = None

        self.name = None
        self.location = None
        self.input_schema = None
        self.input_mapping_default_values = None
        self.input_mapping_fields = None
        self.inbound_ip_rules = None
        self.public_network_access = None
        self.identity = None
        self.kind = None
        self.extended_location_name = None
        self.extended_location_type = None
        self.state = None
        self.regenerate_keys = None

        self.results = dict(
            changed=False,
            eventgrid_topic=dict()
        )

        required_together = [['extended_location_name', 'extended_location_type']]
        required_if = [
            ("kind", "AzureArc", ["extended_location_name"]),
        ]

        super(AzureRMEventgridTopic, self).__init__(self.module_arg_spec,
                                                    supports_tags=True,
                                                    supports_check_mode=True,
                                                    required_together=required_together,
                                                    required_if=required_if,
                                                    )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        identity_info = self._get_identity_info_only_if_not_none(self.identity, self.kind)
        input_schema_mapping = self._get_input_schema_and_mapping(self.input_mapping_fields,
                                                                  self.input_mapping_default_values)
        inbound_ip_rules = self._get_inbound_ip_rules(self.inbound_ip_rules)
        extended_location = self._get_extended_location(self.kind,
                                                        self.extended_location_name,
                                                        self.extended_location_type)

        if self.state == 'present':
            response = self.get_eventgrid_topic(self.resource_group,
                                                self.name)
            if response:
                topic_update_parameters = self.models.TopicUpdateParameters(tags=self.tags,
                                                                            public_network_access=self.public_network_access,
                                                                            inbound_ip_rules=inbound_ip_rules,
                                                                            identity=identity_info)

                self.results['compare'] = []
                changed = not self.default_compare({},
                                                   self.format_eventgrid_topic(topic_update_parameters),
                                                   response,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.begin_update_eventgrid_topic(self.resource_group,
                                                                 self.name,
                                                                 topic_update_parameters)
                if self.regenerate_keys and not self.check_mode:
                    changed = True
                    for key_name in self.regenerate_keys:
                        key_response = self.topic_regenerate_key(self.resource_group,
                                                                 self.name,
                                                                 key_name)

            else:
                changed = True
                topic_info = self.models.Topic(
                    location=self.location,
                    tags=self.tags,
                    input_schema=self.input_schema,
                    input_schema_mapping=input_schema_mapping,
                    public_network_access=self.public_network_access,
                    inbound_ip_rules=inbound_ip_rules,
                    identity=identity_info,
                    kind=self.kind,
                    extended_location=extended_location)

                if not self.check_mode:
                    response = self.begin_create_or_update_eventgrid_topic(self.resource_group,
                                                                           self.name,
                                                                           topic_info)
        else:
            response = self.get_eventgrid_topic(self.resource_group,
                                                self.name)
            if response:
                changed = True
                if not self.check_mode:
                    response = self.delete_eventgrid_topic(self.resource_group,
                                                           self.name)

        self.results['changed'] = changed
        self.results['eventgrid_topic'] = response

        return self.results

    def begin_create_or_update_eventgrid_topic(self, resource_group, topic_name, topic_info):
        self.log('Creates or updates the Eventgrid Topic.')

        try:
            response = self.client.topics.begin_create_or_update(resource_group, topic_name, topic_info)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Creates or updates the Eventgrid Topic got Exception as as {0}'.format(exc.message or str(exc)))
        return self.format_eventgrid_topic(response)

    def begin_update_eventgrid_topic(self, resource_group, topic_name, topic_update_parameters):
        self.log('Selectively updates the Eventgrid Topic.')

        try:
            response = self.client.topics.begin_update(resource_group_name=resource_group,
                                                       topic_name=topic_name,
                                                       topic_update_parameters=topic_update_parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Selectively updates the Eventgrid Topic got Excption as {0}'.format(exc.message or str(exc)))

        return self.format_eventgrid_topic(response)

    def delete_eventgrid_topic(self, resource_group, topic_name):
        self.log('Deletes the entire Eventgrid Topic.')
        try:
            self.client.topics.begin_delete(resource_group, topic_name)
        except Exception as exc:
            self.fail('Delete the entire set of tag got Excetion as {0}'.format(exc.message or str(exc)))

    def get_eventgrid_topic(self, resource_group, topic_name):
        self.log('Get properties for {0}'.format(topic_name))
        try:
            response = self.client.topics.get(resource_group, topic_name)
            if response is not None:
                return self.format_eventgrid_topic(response)
        except ResourceNotFoundError:
            self.log('Did not find the eventgrid_topic.')
            return False
        except Exception as exc:
            self.fail('Error when get eventgrid_topic got Excetion as {0}'.format(exc.message or str(exc)))

    def format_eventgrid_topic(self, topic_data):
        results = topic_data and topic_data.as_dict() or {}
        return results

    def _get_identity_info_only_if_not_none(self, identity=None, kind=None):
        identity_info = None
        if identity:
            # If UserAssigned in module args and ids specified
            if 'UserAssigned' in identity.get('type') and len(identity.get('user_assigned_identities', [])) != 0:
                user_assigned_identities_dict = {uami: self.models.UserIdentityProperties() for uami in identity.get('user_assigned_identities')}
                # Append identities to the model
                identity_info = self.models.IdentityInfo(
                    type=identity.get('type'),
                    user_assigned_identities=user_assigned_identities_dict
                )
            # If UserAssigned in module args, but ids are not specified
            elif 'UserAssigned' in identity.get('type') and len(identity.get('user_assigned_identities', [])) == 0:
                self.fail("UserAssigned specified but no User Identity IDs provided")
            # In any other case ('SystemAssigned' or 'None') apply the configuration to the model
            else:
                identity_info = self.models.IdentityInfo(
                    type=identity.get('type')
                )
        else:
            if kind is None or kind == 'Azure':
                indentity_info = self.models.IdentityInfo(type="None")

        return identity_info

    def _get_input_schema_and_mapping(self,
                                      input_mapping_fields=None,
                                      input_mapping_default_values=None):

        input_schema_mapping = None

        if input_mapping_fields is not None or input_mapping_default_values is not None:
            input_schema_mapping = self.models.JsonInputSchemaMapping()

            input_schema_mapping.id = self.models.JsonField()
            input_schema_mapping.topic = self.models.JsonField()
            input_schema_mapping.event_time = self.models.JsonField()
            input_schema_mapping.subject = self.models.JsonFieldWithDefault()
            input_schema_mapping.event_type = self.models.JsonFieldWithDefault()
            input_schema_mapping.data_version = self.models.JsonFieldWithDefault()

            if input_mapping_fields is not None:
                for input_mapping_field in input_mapping_fields:
                    target = input_mapping_field.get('mapping_key')
                    source = input_mapping_field.get('mapping_value')
                    if target == 'id':
                        input_schema_mapping.id.source_field = source
                    elif target == 'eventtime':
                        input_schema_mapping.event_time.source_field = source
                    elif target == 'topic':
                        input_schema_mapping.topic.source_field = source
                    elif target == 'subject':
                        input_schema_mapping.subject.source_field = source
                    elif target == 'dataversion':
                        input_schema_mapping.data_version.source_field = source
                    elif target == 'eventtype':
                        input_schema_mapping.event_type.source_field = source

            if input_mapping_default_values is not None:
                for input_mapping_default_value in input_mapping_default_values:
                    target = input_mapping_default_value.get('mapping_key')
                    source = input_mapping_default_value.get('mapping_value')
                    if target == 'subject':
                        input_schema_mapping.subject.default_value = source
                    elif target == 'dataversion':
                        input_schema_mapping.data_version.default_value = source
                    elif target == 'eventtype':
                        input_schema_mapping.event_type.default_value = source

        return input_schema_mapping

    def _get_inbound_ip_rules(self, inbound_ip_rules):
        inbound_ip_rules_mapping = []

        for inbound_ip_rule in inbound_ip_rules:
            ipmask = inbound_ip_rule.get('ipmask')
            action = inbound_ip_rule.get('action')
            inbound_ip_rules_mapping.append(self.models.InboundIpRule(ip_mask=ipmask, action=action))

        return inbound_ip_rules_mapping

    def _get_extended_location(self, kind_name=None, extended_location_name=None,
                               extended_location_type=None):
        result = None

        if kind_name == 'AzureArc':
            result = self.models.ExtendedLocation(name=extended_location_name,
                                                  type=extended_location_type)

        return result

    def topic_regenerate_key(self,
                             resource_group,
                             topic_name,
                             key_name):
        regenerate_key_request = self.models.TopicRegenerateKeyRequest(key_name=key_name)

        return self.client.topics.begin_regenerate_key(
            resource_group_name=resource_group,
            topic_name=topic_name,
            regenerate_key_request=regenerate_key_request
        )


def main():
    AzureRMEventgridTopic()


if __name__ == '__main__':
    main()

#!/usr/bin/python
#
# Copyright (c) 2020 Aparna Patil(@aparna-patil)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_privatednsrecordset

version_added: "1.1.0"

short_description: Create, delete and update Private DNS record sets and records

description:
    - Creates, deletes, and updates Private DNS records sets and records within an existing Azure Private DNS Zone.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    zone_name:
        description:
            - Name of the existing Private DNS zone in which to manage the record set.
        required: true
        type: str
    relative_name:
        description:
            - Relative name of the record set.
        required: true
        type: str
    record_type:
        description:
            - The type of record set to create or delete.
        choices:
            - A
            - AAAA
            - CNAME
            - MX
            - PTR
            - SOA
            - SRV
            - TXT
        required: true
        type: str
    record_mode:
        description:
            - Whether existing record values not sent to the module should be purged.
        default: purge
        type: str
        choices:
            - append
            - purge
    state:
        description:
            - Assert the state of the record set. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    time_to_live:
        description:
            - Time to live of the record set in seconds.
        default: 3600
        type: int
    records:
        description:
            - List of records to be created depending on the type of record (set).
        type: list
        elements: dict
        suboptions:
            preference:
                description:
                    - Used for creating an C(MX) record set/records.
                type: int
            priority:
                description:
                   - Used for creating an C(SRV) record set/records.
                type: int
            weight:
                description:
                    - Used for creating an C(SRV) record set/records.
                type: int
            port:
                description:
                    - Used for creating an C(SRV) record set/records.
                type: int
            entry:
                description:
                    - Primary data value for all record types.
                type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@aparna-patil)
'''

EXAMPLES = '''

- name: ensure an "A" record set with multiple records
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    relative_name: www
    zone_name: testing.com
    record_type: A
    records:
      - entry: 192.168.100.101
      - entry: 192.168.100.102
      - entry: 192.168.100.103

- name: delete a record set
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    record_type: A
    relative_name: www
    zone_name: testing.com
    state: absent

- name: create multiple "A" record sets with multiple records
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    zone_name: testing.com
    relative_name: "{{ item.name }}"
    record_type: "{{ item.type }}"
    records: "{{ item.records }}"
  with_items:
    - { name: 'servera', type: 'A', records: [ { entry: '10.10.10.20' }, { entry: '10.10.10.21' }] }
    - { name: 'serverb', type: 'A', records: [ { entry: '10.10.10.30' }, { entry: '10.10.10.41' }] }
    - { name: 'serverc', type: 'A', records: [ { entry: '10.10.10.40' }, { entry: '10.10.10.41' }] }

- name: create SRV records in a new record set
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    relative_name: _sip._tcp.testing.com
    zone_name: testing.com
    time_to_live: 7200
    record_type: SRV
    records:
    - entry: sip.testing.com
      priority: 20
      weight: 10
      port: 5060

- name: create PTR record in a new record set
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    relative_name: 192.168.100.101.in-addr.arpa
    zone_name: testing.com
    record_type: PTR
    records:
    - entry: servera.testing.com

- name: create TXT record in a new record set
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    relative_name: mail.testing.com
    zone_name: testing.com
    record_type: TXT
    records:
    - entry: 'v=spf1 a -all'

- name: Update SOA record
  azure_rm_privatednsrecordset:
    resource_group: myResourceGroup
    relative_name: "@"
    zone_name: testing.com
    record_type: SOA
    records:
      - host: azureprivatedns.net
        email: azureprivatedns-host99.example.com
        serial_number: 1
        refresh_time: 3699
        retry_time: 399
        expire_time: 2419299
        minimum_ttl: 399
'''

RETURN = '''
state:
    description:
        - Current state of the DNS record set.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The DNS record set ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxx......xxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/privateDnsZones/
                     b57dc95985712e4523282.com/A/www"
        name:
            description:
                - Relate name of the record set.
            returned: always
            type: str
            sample: 'www'
        fqdn:
            description:
                - Fully qualified domain name of the record set.
            returned: always
            type: str
            sample: www.b57dc95985712e4523282.com
        etag:
            description:
                - The etag of the record set.
            returned: always
            type: str
            sample: 692c3e92-a618-46fc-aecd-8f888807cd6c
        is_auto_registered:
            description:
                - Is the record set auto-registered in the Private DNS zone through a virtual network link.
            returned: always
            type: bool
            sample: false
        ttl:
            description:
                - The TTL(time-to-live) of the records in the records set.
            returned: always
            type: int
            sample: 3600
        type:
            description:
                - The type of DNS record in this record set.
            returned: always
            type: str
            sample: A
        a_records:
            description:
                - A list of records in the record set.
            returned: always
            type: list
            elements: dict
            sample: [
            {
                "ipv4_address": "192.0.2.2"
            },
            {
                "ipv4_address": "192.0.2.4"
            },
            {
                "ipv4_address": "192.0.2.8"
            }
        ]
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, HAS_AZURE

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


RECORD_ARGSPECS = dict(
    A=dict(
        ipv4_address=dict(type='str', required=True, aliases=['entry'])
    ),
    AAAA=dict(
        ipv6_address=dict(type='str', required=True, aliases=['entry'])
    ),
    CNAME=dict(
        cname=dict(type='str', required=True, aliases=['entry'])
    ),
    MX=dict(
        preference=dict(type='int', required=True),
        exchange=dict(type='str', required=True, aliases=['entry'])
    ),
    PTR=dict(
        ptrdname=dict(type='str', required=True, aliases=['entry'])
    ),
    SRV=dict(
        priority=dict(type='int', required=True),
        port=dict(type='int', required=True),
        weight=dict(type='int', required=True),
        target=dict(type='str', required=True, aliases=['entry'])
    ),
    TXT=dict(
        value=dict(type='list', required=True, aliases=['entry'])
    ),
    SOA=dict(
        host=dict(type='str', aliases=['entry']),
        email=dict(type='str'),
        serial_number=dict(type='int'),
        refresh_time=dict(type='int'),
        retry_time=dict(type='int'),
        expire_time=dict(type='int'),
        minimum_ttl=dict(type='int')
    )
)

RECORDSET_VALUE_MAP = dict(
    A=dict(attrname='a_records', classobj='ARecord', is_list=True),
    AAAA=dict(attrname='aaaa_records', classobj='AaaaRecord', is_list=True),
    CNAME=dict(attrname='cname_record', classobj='CnameRecord', is_list=False),
    MX=dict(attrname='mx_records', classobj='MxRecord', is_list=True),
    NS=dict(attrname='ns_records', classobj='NsRecord', is_list=True),
    PTR=dict(attrname='ptr_records', classobj='PtrRecord', is_list=True),
    SRV=dict(attrname='srv_records', classobj='SrvRecord', is_list=True),
    TXT=dict(attrname='txt_records', classobj='TxtRecord', is_list=True),
    SOA=dict(attrname='soa_record', classobj='SoaRecord', is_list=False),
    CAA=dict(attrname='caa_records', classobj='CaaRecord', is_list=True)
) if HAS_AZURE else {}


class AzureRMPrivateDNSRecordSet(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            relative_name=dict(type='str', required=True),
            zone_name=dict(type='str', required=True),
            record_type=dict(choices=RECORD_ARGSPECS.keys(), required=True, type='str'),
            record_mode=dict(choices=['append', 'purge'], default='purge'),
            state=dict(choices=['present', 'absent'], default='present', type='str'),
            time_to_live=dict(type='int', default=3600),
            records=dict(type='list', elements='dict')
        )

        required_if = [
            ('state', 'present', ['records'])
        ]

        self.results = dict(
            changed=False
        )

        # Argument validation
        super(AzureRMPrivateDNSRecordSet, self).__init__(self.module_arg_spec,
                                                         required_if=required_if,
                                                         supports_check_mode=True,
                                                         skip_exec=True)

        # check the subspec and metadata
        record_subspec = RECORD_ARGSPECS.get(self.module.params['record_type'])

        # patch the right record shape onto the argspec
        self.module_arg_spec['records']['options'] = record_subspec

        self.resource_group = None
        self.relative_name = None
        self.zone_name = None
        self.record_type = None
        self.record_mode = None
        self.state = None
        self.time_to_live = None
        self.records = None

        # rerun validation and module
        super(AzureRMPrivateDNSRecordSet, self).__init__(self.module_arg_spec,
                                                         required_if=required_if,
                                                         supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec.keys():
            setattr(self, key, kwargs[key])

        self.log('Fetching private DNS zone {0}'.format(self.zone_name))
        zone = self.private_dns_client.private_zones.get(self.resource_group, self.zone_name)
        if not zone:
            self.fail('The zone {0} does not exist in the resource group {1}'.format(self.zone_name,
                                                                                     self.resource_group))

        try:
            self.log('Fetching Private DNS Record Set {0}'.format(self.relative_name))
            record_set = self.private_dns_client.record_sets.get(self.resource_group,
                                                                 self.zone_name,
                                                                 self.record_type,
                                                                 self.relative_name)
            self.results['state'] = self.recordset_to_dict(record_set)
        except ResourceNotFoundError:
            record_set = None

        record_type_metadata = RECORDSET_VALUE_MAP.get(self.record_type)

        if self.state == 'present':
            # convert the input records to SDK objects
            self.input_sdk_records = self.create_sdk_records(self.records, self.record_type)

            if not record_set:
                changed = True
            else:
                # use recordset to get the type-specific records
                server_records = getattr(record_set, record_type_metadata.get('attrname'))

                # Compare the input records to the server records
                self.input_sdk_records, changed = self.records_changed(self.input_sdk_records, server_records)

                # check the top-level recordset properties
                changed |= record_set.ttl != self.time_to_live

            self.results['changed'] |= changed

        elif self.state == 'absent':
            if record_set:
                self.results['changed'] = True

        if self.check_mode:
            return self.results

        if self.results['changed']:
            if self.state == 'present':
                record_set_args = dict(
                    ttl=self.time_to_live
                )

                record_set_args[record_type_metadata['attrname']] = \
                    self.input_sdk_records if record_type_metadata['is_list'] else self.input_sdk_records[0]

                record_set = self.private_dns_models.RecordSet(**record_set_args)
                # create record set
                self.results['state'] = self.create_or_update(record_set)

            elif self.state == 'absent':
                # delete record set
                self.delete_record_set()

        return self.results

    def create_or_update(self, record_set):
        try:
            # create the record set
            record_set = \
                self.private_dns_client.record_sets.create_or_update(resource_group_name=self.resource_group,
                                                                     private_zone_name=self.zone_name,
                                                                     record_type=self.record_type,
                                                                     relative_record_set_name=self.relative_name,
                                                                     parameters=record_set)
            return self.recordset_to_dict(record_set)
        except Exception as exc:
            self.fail("Error creating or updating dns record {0} - {1}".format(self.relative_name,
                                                                               exc.message or str(exc)))

    def delete_record_set(self):
        try:
            # delete the record set
            self.private_dns_client.record_sets.delete(resource_group_name=self.resource_group,
                                                       private_zone_name=self.zone_name,
                                                       relative_record_set_name=self.relative_name,
                                                       record_type=self.record_type)
        except Exception as exc:
            self.fail("Error deleting record set {0} - {1}".format(self.relative_name, exc.message or str(exc)))
        return None

    def create_sdk_records(self, input_records, record_type):
        record = RECORDSET_VALUE_MAP.get(record_type)
        if not record:
            self.fail('record type {0} is not supported now'.format(record_type))
        record_sdk_class = getattr(self.private_dns_models, record.get('classobj'))
        return [record_sdk_class(**x) for x in input_records]

    def records_changed(self, input_records, server_records):
        # ensure we're always comparing a list, even for the single-valued types
        if not isinstance(server_records, list):
            server_records = [server_records]

        input_set = set([self.module.jsonify(x.as_dict()) for x in input_records])
        server_set = set([self.module.jsonify(x.as_dict()) for x in server_records])

        if self.record_mode == 'append':  # only a difference if the server set is missing something from the input set
            input_set = server_set.union(input_set)

        # non-append mode; any difference in the sets is a change
        changed = input_set != server_set

        records = [self.module.from_json(x) for x in input_set]
        return self.create_sdk_records(records, self.record_type), changed

    def recordset_to_dict(self, recordset):
        result = recordset.as_dict()
        result['type'] = result['type'].strip('Microsoft.Network/privateDnsZones/')
        return result


def main():
    AzureRMPrivateDNSRecordSet()


if __name__ == '__main__':
    main()

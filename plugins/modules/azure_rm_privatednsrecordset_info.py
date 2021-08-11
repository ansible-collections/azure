#!/usr/bin/python
#
# Copyright (c) 2020 Aparna Patil(@aparna-patil)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_privatednsrecordset_info

version_added: "1.1.0"

short_description: Get Private DNS Record Set facts

description:
    - Get facts for a specific DNS Record Set in a Private DNS Zone, or a specific type of DNS record in all zones or
      one zone etc.

options:
    relative_name:
        description:
            - Only show results for a Record Set.
        type: str
    resource_group:
        description:
            - Limit results by resource group. Required when filtering by name or type.
        type: str
    zone_name:
        description:
            - Limit results by zones. Required when filtering by name or type.
        type: str
    record_type:
        description:
            - Limit record sets by record type.
        type: str
    top:
        description:
            - Limit the maximum number of record sets to return.
        type: int

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@aparna-patil)

'''

EXAMPLES = '''
- name: Get facts for one record set in one Private DNS Zone
  azure_rm_privatednsrecordset_info:
    resource_group: myResourceGroup
    zone_name: newzone.com
    relative_name: servera
    record_type: A
- name: Get facts for all Type A record sets in a Private DNS Zone
  azure_rm_privatednsrecordset_info:
    resource_group: myResourceGroup
    zone_name: newzone.com
    record_type: A
- name: Get all record sets in a Private DNS Zone
  azure_rm_privatednsrecordset_info:
    resource_group: myResourceGroup
    zone_name: newzone.com
'''

RETURN = '''
dnsrecordsets:
    description:
        - Gets a list of recordsets dict in a Private DNS zone.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "fqdn": "servera.newzone.com.",
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                   Microsoft.Network/privateDnsZones/newzone.com/A/servera",
            "record_type": "A",
            "records": [
                {
                    "ipv4_address": "10.10.10.10"
                }
            ],
            "relative_name": "servera",
            "time_to_live": 3600
        },
        {
            "fqdn": "serverb.newzone.com.",
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                   Microsoft.Network/privateDnsZones/newzone.com/A/serverb",
            "record_type": "A",
            "records": [
                {
                    "ipv4_address": "10.10.10.11"
                }
            ],
            "relative_name": "serverb",
            "time_to_live": 3600
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'RecordSet'


RECORDSET_VALUE_MAP = dict(
    A='a_records',
    AAAA='aaaa_records',
    CNAME='cname_record',
    MX='mx_records',
    PTR='ptr_records',
    SRV='srv_records',
    TXT='txt_records',
    SOA='soa_record'
)


class AzureRMPrivateDNSRecordSetInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(
            relative_name=dict(type='str'),
            resource_group=dict(type='str'),
            zone_name=dict(type='str'),
            record_type=dict(type='str'),
            top=dict(type='int')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False,
        )

        self.relative_name = None
        self.resource_group = None
        self.zone_name = None
        self.record_type = None
        self.top = None

        super(AzureRMPrivateDNSRecordSetInfo, self).__init__(self.module_arg_spec, supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if not self.top or self.top <= 0:
            self.top = None

        # create conditionals to catch errors when calling record facts
        if self.relative_name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name or record type.")
        if self.relative_name and not self.zone_name:
            self.fail("Parameter error: DNS Zone required when filtering by name or record type.")

        results = []
        # list the conditions for what to return based on input
        if self.relative_name is not None:
            # if there is a name listed, they want only facts about that specific Record Set itself
            results = self.get_item()
        elif self.record_type:
            # else, they just want all the record sets of a specific type
            results = self.list_type()
        elif self.zone_name:
            # if there is a zone name listed, then they want all the record sets in a zone
            results = self.list_zone()

        self.results['dnsrecordsets'] = self.curated_list(results)
        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.relative_name))
        item = None
        results = []

        # try to get information for specific Record Set
        try:
            item = self.private_dns_client.record_sets.get(self.resource_group,
                                                           self.zone_name,
                                                           self.record_type,
                                                           self.relative_name)
        except CloudError:
            pass

        results = [item]
        return results

    def list_type(self):
        self.log('Lists the record sets of a specified type in a Private DNS zone')
        try:
            response = self.private_dns_client.record_sets.list_by_type(self.resource_group,
                                                                        self.zone_name,
                                                                        self.record_type,
                                                                        top=self.top)
        except AzureHttpError as exc:
            self.fail("Failed to list for record type {0} - {1}".format(self.record_type, str(exc)))

        results = []
        for item in response:
            results.append(item)
        return results

    def list_zone(self):
        self.log('Lists all record sets in a Private DNS zone')
        try:
            response = self.private_dns_client.record_sets.list(self.resource_group, self.zone_name, top=self.top)
        except AzureHttpError as exc:
            self.fail("Failed to list for zone {0} - {1}".format(self.zone_name, str(exc)))

        results = []
        for item in response:
            results.append(item)
        return results

    def curated_list(self, raws):
        return [self.record_to_dict(item) for item in raws] if raws else []

    def record_to_dict(self, record):
        record_type = record.type[len('Microsoft.Network/privateDnsZones/'):]
        records = getattr(record, RECORDSET_VALUE_MAP.get(record_type))
        if records:
            if not isinstance(records, list):
                records = [records]
        else:
            records = []
        return dict(
            id=record.id,
            relative_name=record.name,
            record_type=record_type,
            records=[x.as_dict() for x in records],
            time_to_live=record.ttl,
            fqdn=record.fqdn
        )


def main():
    AzureRMPrivateDNSRecordSetInfo()


if __name__ == '__main__':
    main()

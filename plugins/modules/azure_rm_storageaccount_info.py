#!/usr/bin/python
#
# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storageaccount_info

version_added: "0.1.2"

short_description: Get storage account facts

description:
    - Get facts for one storage account or all storage accounts within a resource group.

options:
    name:
        description:
            - Only show results for a specific account.
        type: str
    resource_group:
        description:
            - Limit results to a resource group. Required when filtering by name.
        type: str
        aliases:
            - resource_group_name
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str
    show_connection_string:
        description:
            - Show the connection string for each of the storageaccount's endpoints.
            - For convenient usage, I(show_connection_string) will also show the access keys for each of the storageaccount's endpoints.
            - Note that it will cost a lot of time when list all storageaccount rather than query a single one.
        type: bool
    show_blob_cors:
        description:
            - Show the blob CORS settings for each blob related to the storage account.
            - Querying all storage accounts will take a long time.
        type: bool
    show_georeplication_stats:
        description:
            - Show the Geo Replication Stats for each storage account.
            - Using this option on an account that does not support georeplication will cause a delay in getting results.
        type: bool

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Chris Houseknecht (@chouseknecht)
    - Matt Davis (@nitzmahone)

'''

EXAMPLES = '''
- name: Get facts for one account
  azure_rm_storageaccount_info:
    resource_group: myResourceGroup
    name: clh0002

- name: Get facts for all accounts in a resource group
  azure_rm_storageaccount_info:
    resource_group: myResourceGroup

- name: Get facts for all accounts by tags
  azure_rm_storageaccount_info:
    tags:
      - testing
      - foo:bar
'''

RETURN = '''
azure_storageaccounts:
    description:
        - List of storage account dicts.
    returned: always
    type: list
    example: [{
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/myResourceGroups/testing/providers/Microsoft.Storage/storageAccounts/testaccount001",
        "location": "eastus2",
        "name": "testaccount001",
        "properties": {
            "accountType": "Standard_LRS",
            "creationTime": "2016-03-28T02:46:58.290113Z",
            "primaryEndpoints": {
                "blob": "https://testaccount001.blob.core.windows.net/",
                "file": "https://testaccount001.file.core.windows.net/",
                "queue": "https://testaccount001.queue.core.windows.net/",
                "table": "https://testaccount001.table.core.windows.net/"
            },
            "primaryLocation": "eastus2",
            "provisioningState": "Succeeded",
            "statusOfPrimary": "Available"
        },
        "tags": {},
        "type": "Microsoft.Storage/storageAccounts"
    }]
storageaccounts:
    description:
        - List of storage account dicts in resource module's parameter format.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/t
                     estaccount001"
        name:
            description:
                - Name of the storage account to update or create.
            returned: always
            type: str
            sample: testaccount001
        location:
            description:
                - Valid Azure location. Defaults to location of the resource group.
            returned: always
            type: str
            sample: eastus
        account_type:
            description:
                - Type of storage account.
                - C(Standard_ZRS) and C(Premium_LRS) accounts cannot be changed to other account types.
                - Other account types cannot be changed to C(Standard_ZRS) or C(Premium_LRS).
            returned: always
            type: str
            sample: Standard_ZRS
        allow_cross_tenant_replication:
            description:
                - Allow or disallow cross AAD tenant object replication.
            type: bool
            returned: always
            sample: true
        allow_shared_key_access:
            description:
                - Indicates whether the storage account permits requests to be authorized with the account access key via Shared Key.
            type: bool
            returned: always
            sample: true
        default_to_o_auth_authentication:
            description:
                - A boolean flag which indicates whether the default authentication is OAuth or not.
                - The default interpretation is false for this property.
            type: bool
            returned: always
            sample: true
        custom_domain:
            description:
                - User domain assigned to the storage account.
                - Must be a dictionary with I(name) and I(use_sub_domain) keys where I(name) is the CNAME source.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - CNAME source.
                    returned: always
                    type: str
                    sample: testaccount
                use_sub_domain:
                    description:
                        - Whether to use sub domain.
                    returned: always
                    type: bool
                    sample: true
        encryption:
            description:
                - The encryption settings on the storage account.
            type: complex
            returned: always
            contains:
                key_source:
                    description:
                        - The encryption keySource (provider).
                    type: str
                    returned: always
                    sample: Microsoft.Storage
                require_infrastructure_encryption:
                    description:
                        - A boolean indicating whether or not the service applies a secondary layer of encryption with platform managed keys for data at rest.
                    type: bool
                    returned: always
                    sample: false
                services:
                    description:
                        - List of services which support encryption.
                    type: dict
                    returned: always
                    contains:
                        file:
                            description:
                                - The encryption function of the file storage service.
                            type: dict
                            returned: always
                            sample: {'enabled': true}
                        table:
                            description:
                                - The encryption function of the table storage service.
                            type: dict
                            returned: always
                            sample: {'enabled': true}
                        queue:
                            description:
                                - The encryption function of the queue storage service.
                            type: dict
                            returned: always
                            sample: {'enabled': true}
                        blob:
                            description:
                                - The encryption function of the blob storage service.
                            type: dict
                            returned: always
                            sample: {'enabled': true}
        is_hns_enabled:
            description:
                - Account HierarchicalNamespace enabled if sets to true.
            type: bool
            returned: always
            sample: true
        immutable_storage_with_versioning:
            description:
                - The property is immutable and can only be set to true at the account creation time.
                - When set to true, it enables object level immutability for all the containers in the account by default.
            type: complex
            returned: when-used
            contains:
                enabled:
                    description:
                        - A boolean flag which enables account-level immutability.
                        - All the containers under such an account have object-level immutability enabled by default.
                    type: bool
                    returned: when-used
                    sample: true
                immutability_policy:
                    description:
                        - Specifies the default account-level immutability policy which is inherited and
                          applied to objects that do not possess an explicit immutability policy at the object level.
                        - The object-level immutability policy has higher precedence than the container-level immutability policy,
                          which has a higher precedence than the account-level immutability policy.
                    type: dict
                    returned: when-used
                    contains:
                        allow_protected_append_writes:
                            description:
                                - This property can only be changed for disabled and unlocked time-based retention policies.
                                - When enabled, new blocks can be written to an append blob while maintaining immutability protection and compliance.
                                - Only new blocks can be added and any existing blocks cannot be modified or deleted.
                            type: bool
                            returned: when-used
                            sample: true
                        state:
                            description:
                                - The ImmutabilityPolicy state defines the mode of the policy.
                            type: str
                            returned: when-used
                            sample: Unlocked
                        immutability_period_since_creation_in_days:
                            description:
                                - The immutability period for the blobs in the container since the policy creation, in days.
                            type: int
                            returned: when-used
                            sample: true
        enable_nfs_v3:
            description:
                - NFS 3.0 protocol.
            type: bool
            returned: always
            sample: false
        kind:
            description:
                - The kind of storage.
            returned: always
            type: str
            sample: Storage
        access_tier:
            description:
                - The access tier for this storage account.
            returned: always
            type: str
            sample: Hot
        https_only:
            description:
                -  Allows https traffic only to storage service when set to C(true).
            returned: always
            type: bool
            sample: false
        minimum_tls_version:
            description:
                -  The minimum TLS version permitted on requests to storage.
            returned: always
            type: str
            sample: TLS1_2
        public_network_access:
            description:
                -  Public network access to Storage Account allowed or disallowed.
            returned: always
            type: str
            sample: Enabled
        allow_blob_public_access:
            description:
                -  Public access to all blobs or containers in the storage account allowed or disallowed.
            returned: always
            type: bool
            sample: true
        network_acls:
            description:
                - A set of firewall and virtual network rules
            returned: always
            type: dict
            sample: {
                    "bypass": "AzureServices",
                    "default_action": "Deny",
                    "virtual_network_rules": [
                        {
                            "action": "Allow",
                            "id": "/subscriptions/mySubscriptionId/resourceGroups/myResourceGroup/ \
                                    providers/Microsoft.Network/virtualNetworks/myVnet/subnets/mySubnet"
                            }
                        ],
                    "ip_rules": [
                        {
                            "action": "Allow",
                            "value": "1.2.3.4"
                        },
                        {
                            "action": "Allow",
                            "value": "123.234.123.0/24"
                        }
                    ]
                    }
        provisioning_state:
            description:
                - The status of the storage account at the time the operation was called.
                - Possible values include C(Creating), C(ResolvingDNS), C(Succeeded).
            returned: always
            type: str
            sample: Succeeded
        failover_in_progress:
            description:
                - Status indicating the storage account is currently failing over to its secondary location.
            returned: always
            type: bool
            sample: False
        secondary_location:
            description:
                - The location of the geo-replicated secondary for the storage account.
                - Only available if the I(account_type=Standard_GRS) or I(account_type=Standard_RAGRS).
            returned: always
            type: str
            sample: westus
        status_of_primary:
            description:
                - Status of the primary location of the storage account; either C(available) or C(unavailable).
            returned: always
            type: str
            sample: available
        status_of_secondary:
            description:
                - Status of the secondary location of the storage account; either C(available) or C(unavailable).
            returned: always
            type: str
            sample: available
        primary_location:
            description:
                - The location of the primary data center for the storage account.
            returned: always
            type: str
            sample: eastus
        primary_endpoints:
            description:
                - URLs to retrieve a public I(blob), I(file), I(queue), or I(table) object.
                - Note that C(Standard_ZRS) and C(Premium_LRS) accounts only return the blob endpoint.
            returned: always
            type: complex
            contains:
                blob:
                    description:
                        - The primary blob endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The primary blob endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.blob.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the blob endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;BlobEndpoint=X"
                file:
                    description:
                        - The primary file endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The primary file endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.file.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the file endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;FileEndpoint=X"
                queue:
                    description:
                        - The primary queue endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The primary queue endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.queue.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the queue endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;QueueEndpoint=X"
                table:
                    description:
                        - The primary table endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The primary table endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.table.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the table endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;TableEndpoint=X"
                key:
                    description:
                        - The account key for the primary_endpoints
                    returned: always
                    type: str
                    sample: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        secondary_endpoints:
            description:
                - The URLs to retrieve a public I(blob), I(file), I(queue), or I(table) object from the secondary location.
                - Only available if the SKU I(name=Standard_RAGRS).
            returned: always
            type: complex
            contains:
                blob:
                    description:
                        - The secondary blob endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The secondary blob endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.blob.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the blob endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;BlobEndpoint=X"
                file:
                    description:
                        - The secondary file endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The secondary file endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.file.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the file endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;FileEndpoint=X"
                queue:
                    description:
                        - The secondary queue endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The secondary queue endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.queue.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the queue endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;QueueEndpoint=X"
                table:
                    description:
                        - The secondary table endpoint and connection string.
                    returned: always
                    type: complex
                    contains:
                        endpoint:
                            description:
                                - The secondary table endpoint.
                            returned: always
                            type: str
                            sample: "https://testaccount001.table.core.windows.net/"
                        connectionstring:
                            description:
                                - Connectionstring of the table endpoint.
                            returned: always
                            type: str
                            sample: "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=X;AccountKey=X;TableEndpoint=X"
                key:
                    description:
                        - The account key for the secondary_endpoints
                    sample: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    type: str
        georeplication_stats:
            description:
                - Parameters related to the status of geo-replication.
                - This will be null on accounts that don't support geo-replication.
            returned: always
            type: complex
            contains:
                can_failover:
                    description:
                        - Property indicating if fail over is supported by the account.
                    type: bool
                    sample: true
                last_sync_time:
                    description:
                        - Writes to the primary before this time are guaranteed to be replicated to the secondary.
                    type: str
                    sample: "2023-04-10T21:22:15+00:00"
                sync_status:
                    description:
                        - Property showing status of the secondary region.
                        - Known values are "Live", "Bootstrap", and "Unavailable".
                    type: str
                    sample: Live
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { "tag1": "abc" }
        large_file_shares_state:
            description:
                - Allow large file shares if sets to Enabled.
            type: str
            returned: always
            sample: Enabled
        static_website:
            description:
                - Static website configuration for the storage account.
            returned: always
            version_added: "1.13.0"
            type: complex
            contains:
                enabled:
                    description:
                        - Whether this account is hosting a static website.
                    returned: always
                    type: bool
                    sample: true
                index_document:
                    description:
                        - The default name of the index page under each directory.
                    returned: always
                    type: str
                    sample: index.html
                error_document404_path:
                    description:
                        - The absolute path of the custom 404 page.
                    returned: always
                    type: str
                    sample: error.html
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils._text import to_native


AZURE_OBJECT_CLASS = 'StorageAccount'


class AzureRMStorageAccountInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str', aliases=['resource_group_name']),
            tags=dict(type='list', elements='str'),
            show_connection_string=dict(type='bool'),
            show_blob_cors=dict(type='bool'),
            show_georeplication_stats=dict(type='bool')
        )

        self.results = dict(
            changed=False,
            storageaccounts=[]
        )

        self.name = None
        self.resource_group = None
        self.tags = None
        self.show_connection_string = None
        self.show_blob_cors = None
        self.show_georeplication_stats = None

        super(AzureRMStorageAccountInfo, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False,
                                                        facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        results = []
        if self.name:
            results = self.get_account()
        elif self.resource_group:
            results = self.list_resource_group()
        else:
            results = self.list_all()

        filtered = self.filter_tag(results)

        self.results['storageaccounts'] = self.format_to_dict(filtered)
        return self.results

    def get_account(self):
        self.log('Get properties for account {0}'.format(self.name))
        account = None
        try:
            expand = None
            if (self.show_georeplication_stats):
                expand = 'georeplicationstats'
            account = self.storage_client.storage_accounts.get_properties(self.resource_group, self.name, expand=expand)
            return [account]
        except Exception as exc:

            # Several errors are passed as generic HTTP errors. Catch the error and pass back the basic account information
            # if the account doesn't support replication or replication stats are not available.
            if "InvalidAccountType" in str(exc) or "LastSyncTimeUnavailable" in str(exc):
                account = self.storage_client.storage_accounts.get_properties(self.resource_group, self.name)
                return [account]

            if "AuthorizationFailed" in str(exc):
                self.fail("Error authenticating with the Azure storage API. {0}".format(str(exc)))

        return []

    def list_resource_group(self):
        self.log('List items')
        try:
            response = self.storage_client.storage_accounts.list_by_resource_group(self.resource_group)
        except Exception as exc:
            self.fail("Error listing for resource group {0} - {1}".format(self.resource_group, str(exc)))

        return response

    def list_all(self):
        self.log('List all items')
        try:
            response = self.storage_client.storage_accounts.list()
        except Exception as exc:
            self.fail("Error listing all items - {0}".format(str(exc)))

        return response

    def filter_tag(self, raw):
        return [item for item in raw if self.has_tags(item.tags, self.tags)]

    def serialize(self, raw):
        return [self.serialize_obj(item, AZURE_OBJECT_CLASS) for item in raw]

    def format_to_dict(self, raw):
        return [self.account_obj_to_dict(item) for item in raw]

    def account_obj_to_dict(self, account_obj):
        account_dict = dict(
            id=account_obj.id,
            name=account_obj.name,
            location=account_obj.location,
            failover_in_progress=(account_obj.failover_in_progress
                                  if account_obj.failover_in_progress is not None else False),
            access_tier=(account_obj.access_tier
                         if account_obj.access_tier is not None else None),
            account_type=account_obj.sku.name,
            kind=account_obj.kind if account_obj.kind else None,
            provisioning_state=account_obj.provisioning_state,
            secondary_location=account_obj.secondary_location,
            status_of_primary=(account_obj.status_of_primary
                               if account_obj.status_of_primary is not None else None),
            status_of_secondary=(account_obj.status_of_secondary
                                 if account_obj.status_of_secondary is not None else None),
            primary_location=account_obj.primary_location,
            https_only=account_obj.enable_https_traffic_only,
            minimum_tls_version=account_obj.minimum_tls_version,
            public_network_access=account_obj.public_network_access,
            allow_blob_public_access=account_obj.allow_blob_public_access,
            is_hns_enabled=account_obj.is_hns_enabled if account_obj.is_hns_enabled else False,
            large_file_shares_state=account_obj.large_file_shares_state,
            enable_nfs_v3=account_obj.enable_nfs_v3 if hasattr(account_obj, 'enable_nfs_v3') else None,
            allow_cross_tenant_replication=account_obj.allow_cross_tenant_replication,
            allow_shared_key_access=account_obj.allow_shared_key_access,
            default_to_o_auth_authentication=account_obj.default_to_o_auth_authentication,
            static_website=dict(
                enabled=False,
                index_document=None,
                error_document404_path=None,
            ),
            immutable_storage_with_versioning=account_obj.immutable_storage_with_versioning.as_dict() if account_obj.immutable_storage_with_versioning else None
        )

        account_dict['geo_replication_stats'] = None
        if account_obj.geo_replication_stats is not None:
            account_dict['geo_replication_stats'] = dict(
                status=account_obj.geo_replication_stats.status,
                can_failover=account_obj.geo_replication_stats.can_failover,
                last_sync_time=account_obj.geo_replication_stats.last_sync_time
            )

        id_dict = self.parse_resource_to_dict(account_obj.id)
        account_dict['resource_group'] = id_dict.get('resource_group')
        account_key = self.get_connectionstring(account_dict['resource_group'], account_dict['name'])
        account_dict['custom_domain'] = None
        if account_obj.custom_domain:
            account_dict['custom_domain'] = dict(
                name=account_obj.custom_domain.name,
                use_sub_domain=account_obj.custom_domain.use_sub_domain
            )

        account_dict['network_acls'] = None
        if account_obj.network_rule_set:
            account_dict['network_acls'] = dict(
                bypass=account_obj.network_rule_set.bypass,
                default_action=account_obj.network_rule_set.default_action,
                ip_rules=account_obj.network_rule_set.ip_rules
            )
            if account_obj.network_rule_set.virtual_network_rules:
                account_dict['network_acls']['virtual_network_rules'] = []
                for rule in account_obj.network_rule_set.virtual_network_rules:
                    account_dict['network_acls']['virtual_network_rules'].append(dict(id=rule.virtual_network_resource_id, action=rule.action))

            if account_obj.network_rule_set.ip_rules:
                account_dict['network_acls']['ip_rules'] = []
                for rule in account_obj.network_rule_set.ip_rules:
                    account_dict['network_acls']['ip_rules'].append(dict(value=rule.ip_address_or_range, action=rule.action))

        account_dict['primary_endpoints'] = None
        if account_obj.primary_endpoints:
            account_dict['primary_endpoints'] = dict(
                blob=self.format_endpoint_dict(account_dict['name'], account_key[0], account_obj.primary_endpoints.blob, 'blob'),
                file=self.format_endpoint_dict(account_dict['name'], account_key[0], account_obj.primary_endpoints.file, 'file'),
                queue=self.format_endpoint_dict(account_dict['name'], account_key[0], account_obj.primary_endpoints.queue, 'queue'),
                table=self.format_endpoint_dict(account_dict['name'], account_key[0], account_obj.primary_endpoints.table, 'table')
            )
            if account_key[0]:
                account_dict['primary_endpoints']['key'] = '{0}'.format(account_key[0])
        account_dict['secondary_endpoints'] = None
        if account_obj.secondary_endpoints:
            account_dict['secondary_endpoints'] = dict(
                blob=self.format_endpoint_dict(account_dict['name'], account_key[1], account_obj.primary_endpoints.blob, 'blob'),
                file=self.format_endpoint_dict(account_dict['name'], account_key[1], account_obj.primary_endpoints.file, 'file'),
                queue=self.format_endpoint_dict(account_dict['name'], account_key[1], account_obj.primary_endpoints.queue, 'queue'),
                table=self.format_endpoint_dict(account_dict['name'], account_key[1], account_obj.primary_endpoints.table, 'table'),
            )
            if account_key[1]:
                account_dict['secondary_endpoints']['key'] = '{0}'.format(account_key[1])
        account_dict['tags'] = None
        if account_obj.tags:
            account_dict['tags'] = account_obj.tags
        blob_mgmt_props = self.get_blob_mgmt_props(account_dict['resource_group'], account_dict['name'])
        if blob_mgmt_props and blob_mgmt_props.cors and blob_mgmt_props.cors.cors_rules:
            account_dict['blob_cors'] = [dict(
                allowed_origins=to_native(x.allowed_origins),
                allowed_methods=to_native(x.allowed_methods),
                max_age_in_seconds=x.max_age_in_seconds,
                exposed_headers=to_native(x.exposed_headers),
                allowed_headers=to_native(x.allowed_headers)
            ) for x in blob_mgmt_props.cors.cors_rules]
        blob_client_props = self.get_blob_client_props(account_dict['resource_group'], account_dict['name'], account_dict['kind'])
        if blob_client_props and blob_client_props['static_website']:
            static_website = blob_client_props['static_website']
            account_dict['static_website'] = dict(
                enabled=static_website.enabled,
                index_document=static_website.index_document,
                error_document404_path=static_website.error_document404_path,
            )

        account_dict['encryption'] = dict()
        if account_obj.encryption:
            account_dict['encryption']['require_infrastructure_encryption'] = account_obj.encryption.require_infrastructure_encryption
            account_dict['encryption']['key_source'] = account_obj.encryption.key_source

            if account_obj.encryption.services:
                account_dict['encryption']['services'] = dict()

                if account_obj.encryption.services.file:
                    account_dict['encryption']['services']['file'] = dict(enabled=True)
                if account_obj.encryption.services.table:
                    account_dict['encryption']['services']['table'] = dict(enabled=True)
                if account_obj.encryption.services.queue:
                    account_dict['encryption']['services']['queue'] = dict(enabled=True)
                if account_obj.encryption.services.blob:
                    account_dict['encryption']['services']['blob'] = dict(enabled=True)

        account_dict['identity'] = dict()
        if account_obj.identity:
            account_dict['identity'] = account_obj.identity.as_dict()

        return account_dict

    def format_endpoint_dict(self, name, key, endpoint, storagetype, protocol='https'):
        result = dict(endpoint=endpoint)
        if key:
            result['connectionstring'] = 'DefaultEndpointsProtocol={0};EndpointSuffix={1};AccountName={2};AccountKey={3};{4}Endpoint={5}'.format(
                                         protocol,
                                         self._cloud_environment.suffixes.storage_endpoint,
                                         name,
                                         key,
                                         str.title(storagetype),
                                         endpoint)
        return result

    def get_blob_mgmt_props(self, resource_group, name):
        if not self.show_blob_cors:
            return None
        try:
            return self.storage_client.blob_services.get_service_properties(resource_group, name)
        except Exception:
            pass
        return None

    def get_blob_client_props(self, resource_group, name, kind):
        if kind == "FileStorage":
            return None
        try:
            return self.get_blob_service_client(resource_group, name).get_service_properties()
        except Exception:
            pass
        return None

    def get_connectionstring(self, resource_group, name):
        keys = ['', '']
        if not self.show_connection_string:
            return keys
        try:
            cred = self.storage_client.storage_accounts.list_keys(resource_group, name)
            # get the following try catch from CLI
            try:
                keys = [cred.keys[0].value, cred.keys[1].value]
            except AttributeError:
                keys = [cred.key1, cred.key2]
        except Exception:
            pass
        return keys


def main():
    AzureRMStorageAccountInfo()


if __name__ == '__main__':
    main()

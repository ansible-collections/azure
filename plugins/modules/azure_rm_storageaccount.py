#!/usr/bin/python
#
# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storageaccount
version_added: "0.1.0"
short_description: Manage Azure storage accounts
description:
    - Create, update or delete a storage account.
options:
    auth_mode:
        description:
            - The mode in which to run the command. C(login) mode will directly use your login credentials for the authentication.
            - The legacy C(key) mode will attempt to query for an account key if no authentication parameters for the account are provided.
            - Can also be set via the environment variable C(AZURE_STORAGE_AUTH_MODE).
        default: key
        type: str
        choices:
            - key
            - login
        version_added: "3.10.0"
    resource_group:
        description:
            - Name of the resource group to use.
        required: true
        type: str
        aliases:
            - resource_group_name
    name:
        description:
            - Name of the storage account to update or create.
        type: str
        required: true
    state:
        description:
            - State of the storage account. Use C(present) to create or update a storage account and use C(absent) to delete an account.
            - C(failover) is used to failover the storage account to its secondary. This process can take up to a hour.
        default: present
        type: str
        choices:
            - absent
            - present
            - failover
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    account_type:
        description:
            - Type of storage account. Required when creating a storage account.
            - C(Standard_ZRS) and C(Premium_LRS) accounts cannot be changed to other account types.
            - Other account types cannot be changed to C(Standard_ZRS) or C(Premium_LRS).
        type: str
        choices:
            - Premium_LRS
            - Standard_GRS
            - Standard_LRS
            - Standard_RAGRS
            - Standard_ZRS
            - Premium_ZRS
            - Standard_RAGZRS
            - Standard_GZRS
        aliases:
            - type
    custom_domain:
        description:
            - User domain assigned to the storage account.
            - Must be a dictionary with I(name) and I(use_sub_domain) keys where I(name) is the CNAME source.
            - Only one custom domain is supported per storage account at this time.
            - To clear the existing custom domain, use an empty string for the custom domain name property.
            - Can be added to an existing storage account. Will be ignored during storage account creation.
        type: dict
        aliases:
            - custom_dns_domain_suffix
    kind:
        description:
            - The kind of storage.
            - The C(FileStorage) and (BlockBlobStorage) only used when I(account_type=Premium_LRS) or I(account_type=Premium_ZRS).
        default: 'Storage'
        type: str
        choices:
            - Storage
            - StorageV2
            - BlobStorage
            - BlockBlobStorage
            - FileStorage
    is_hns_enabled:
        description:
            - Account HierarchicalNamespace enabled if sets to true.
            - When I(is_hns_enabled=True), I(kind) cannot be C(Storage).
        type: bool
    enable_nfs_v3:
        description:
            - NFS 3.0 protocol.
        type: bool
    access_tier:
        description:
            - The access tier for this storage account. Required when I(kind=BlobStorage).
        type: str
        choices:
            - Hot
            - Cool
    force_delete_nonempty:
        description:
            - Attempt deletion if resource already exists and cannot be updated.
        type: bool
        default: False
        aliases:
            - force
    https_only:
        description:
            - Allows https traffic only to storage service when set to C(True).
            - If omitted, new account creation will default to True, while existing accounts will not be change.
        type: bool
    minimum_tls_version:
        description:
            - The minimum required version of Transport Layer Security (TLS) for requests to a storage account.
            - If omitted, new account creation will default to null which is currently interpreted to TLS1_0. Existing accounts will not be modified.
        type: str
        choices:
            - TLS1_0
            - TLS1_1
            - TLS1_2
        version_added: "1.0.0"
    public_network_access:
        description:
            - Allow or disallow public network access to Storage Account.
        type: str
        choices:
            - Enabled
            - Disabled
        version_added: "1.12.0"
    allow_blob_public_access:
        description:
            - Allows blob containers in account to be set for anonymous public access.
            - If set to false, no containers in this account will be able to allow anonymous public access.
            - If omitted, new account creation will default to null which is currently interpreted to True. Existing accounts will not be modified.
        type: bool
        version_added: "1.1.0"
    network_acls:
        description:
            - Manages the Firewall and virtual networks settings of the storage account.
        type: dict
        suboptions:
            default_action:
                description:
                    - Default firewall traffic rule.
                    - If I(default_action=Allow) no other settings have effect.
                type: str
                choices:
                    - Allow
                    - Deny
                default: Allow
            bypass:
                description:
                    - When I(default_action=Deny) this controls which Azure components can still reach the Storage Account.
                    - The list is comma separated.
                    - It can be any combination of the example C(AzureServices), C(Logging), C(Metrics).
                    - If no Azure components are allowed, explicitly set I(bypass="").
                default: AzureServices
                type: str
            virtual_network_rules:
                description:
                    - A list of subnets and their actions.
                type: list
                elements: dict
                suboptions:
                    id:
                        description:
                            - The complete path to the subnet.
                        type: str
                    action:
                        description:
                            - The only logical I(action=Allow) because this setting is only accessible when I(default_action=Deny).
                        default: 'Allow'
                        type: str
            ip_rules:
                description:
                    - A list of IP addresses or ranges in CIDR format.
                type: list
                elements: dict
                suboptions:
                    value:
                        description:
                            - The IP address or range.
                        type: str
                    action:
                        description:
                            - The only logical I(action=Allow) because this setting is only accessible when I(default_action=Deny).
                        default: 'Allow'
                        type: str
    blob_cors:
        description:
            - Specifies CORS rules for the Blob service.
            - You can include up to five CorsRule elements in the request.
            - If no blob_cors elements are included in the argument list, nothing about CORS will be changed.
            - If you want to delete all CORS rules and disable CORS for the Blob service, explicitly set I(blob_cors=[]).
        type: list
        elements: dict
        suboptions:
            allowed_origins:
                description:
                    - A list of origin domains that will be allowed via CORS, or "*" to allow all domains.
                type: list
                elements: str
                required: true
            allowed_methods:
                description:
                    - A list of HTTP methods that are allowed to be executed by the origin.
                type: list
                elements: str
                required: true
            max_age_in_seconds:
                description:
                    - The number of seconds that the client/browser should cache a preflight response.
                type: int
                required: true
            exposed_headers:
                description:
                    - A list of response headers to expose to CORS clients.
                type: list
                elements: str
                required: true
            allowed_headers:
                description:
                    - A list of headers allowed to be part of the cross-origin request.
                type: list
                elements: str
                required: true
    static_website:
        description:
            - Manage static website configuration for the storage account.
        type: dict
        version_added: "1.13.0"
        suboptions:
            enabled:
                description:
                    - Indicates whether this account is hosting a static website.
                type: bool
                default: false
            index_document:
                description:
                    - The default name of the index page under each directory.
                type: str
            error_document404_path:
                description:
                    - The absolute path of the custom 404 page.
                type: str
    large_file_shares_state:
        description:
            - Allow large file shares if sets to Enabled.
        type: str
        choices:
            - Enabled
            - Disabled
    allow_cross_tenant_replication:
        description:
            - Allow or disallow cross AAD tenant object replication.
        type: bool
    allow_shared_key_access:
        description:
            - Indicates whether the storage account permits requests to be authorized with the account access key via Shared Key.
            - If false, then all requests, including shared access signatures, must be authorized with Azure Active Directory (Azure AD).
            - The default value is null, which is equivalent to true.
        type: bool
    default_to_o_auth_authentication:
        description:
            - A boolean flag which indicates whether the default authentication is OAuth or not.
            - The default interpretation is false for this property.
        type: bool
    encryption:
        description:
            - The encryption settings on the storage account.
        type: dict
        suboptions:
            services:
                description:
                    -  List of services which support encryption.
                type: dict
                suboptions:
                    table:
                        description:
                            - The encryption function of the table storage service.
                        type: dict
                        suboptions:
                            enabled:
                                description:
                                    - Whether to encrypt the table type.
                                type: bool
                    queue:
                        description:
                            - The encryption function of the queue storage service.
                        type: dict
                        suboptions:
                            enabled:
                                description:
                                    - Whether to encrypt the queue type.
                                type: bool
                    file:
                        description:
                            - The encryption function of the file storage service.
                        type: dict
                        suboptions:
                            enabled:
                                description:
                                    - Whether to encrypt the file type.
                                type: bool
                    blob:
                        description:
                            - The encryption function of the blob storage service.
                        type: dict
                        suboptions:
                            enabled:
                                description:
                                    - Whether to encrypt the blob type.
                                type: bool
            key_source:
                description:
                    - The encryption keySource (provider).
                type: str
                default: Microsoft.Storage
                choices:
                    - Microsoft.Storage
                    - Microsoft.Keyvault
            key_vault_properties:
                description:
                  - list of Microsoft Keyvault properties needed in order to create Storage account with encryption enabled with Microsoft KeyVault for CMK.
                type: dict
                suboptions:
                  key_vault_uri:
                    description:
                        - The Uri of KeyVault.
                    type: str
                    required: true
                  key_name:
                    description:
                      - The name of KeyVault key.
                    type: str
                    required: true
                  key_version:
                    description:
                      - The version of KeyVault key.
                    type: str
            encryption_identity:
                description:
                    - The identity to be used with service-side encryption at rest.
                type: dict
                suboptions:
                  encryption_user_assigned_identity:
                    description:
                      - Resource identifier of the UserAssigned identity to be associated with server-side encryption on the storage account.
                    type: str
            require_infrastructure_encryption:
                description:
                    - A boolean indicating whether or not the service applies a secondary layer of encryption with platform managed keys for data at rest.
                type: bool
    immutable_storage_with_versioning:
        description:
            - The property is immutable and can only be set to true at the account creation time.
            - When set to true, it enables object level immutability for all the containers in the account by default.
        type: dict
        suboptions:
            enabled:
                description:
                    - A boolean flag which enables account-level immutability.
                    - All the containers under such an account have object-level immutability enabled by default.
                type: bool
            immutability_policy:
                description:
                    - Specifies the default account-level immutability policy which is inherited and
                      applied to objects that do not possess an explicit immutability policy at the object level.
                    - The object-level immutability policy has higher precedence than the container-level immutability policy,
                      which has a higher precedence than the account-level immutability policy.
                type: dict
                suboptions:
                    allow_protected_append_writes:
                        description:
                            - This property can only be changed for C(disabled) and C(unlocked) time-based retention policies.
                            - When C(enabled), new blocks can be written to an append blob while maintaining immutability protection and compliance.
                            - Only new blocks can be added and any existing blocks cannot be modified or deleted.
                        type: bool
                    state:
                        description:
                            - The ImmutabilityPolicy state defines the mode of the policy.
                        type: str
                        choices:
                            - Unlocked
                            - Locked
                            - Disabled
                    immutability_period_since_creation_in_days:
                        description:
                            - The immutability period for the blobs in the container since the policy creation, in days.
                        type: int

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_single

author:
    - Chris Houseknecht (@chouseknecht)
    - Matt Davis (@nitzmahone)
'''

EXAMPLES = '''
- name: remove account, if it exists
  azure_rm_storageaccount:
    resource_group: myResourceGroup
    name: clh0002
    state: absent

- name: create an account
  azure_rm_storageaccount:
    resource_group: myResourceGroup
    name: clh0002
    type: Standard_RAGRS
    tags:
      testing: testing
      delete: on-exit

- name: Create an account with kind of FileStorage
  azure_rm_storageaccount:
    resource_group: myResourceGroup
    name: c1h0002
    type: Premium_LRS
    kind: FileStorage
    tags:
      testing: testing

- name: Create storage account with I(enable_nfs_v3=false)
  azure_rm_storageaccount:
    resource_group: myResourceGroup
    name: c1h0002
    account_type: Premium_LRS
    kind: FileStorage
    enable_nfs_v3: false
    static_website:
      enabled: true

- name: configure firewall and virtual networks
  azure_rm_storageaccount:
    resource_group: myResourceGroup
    name: clh0002
    type: Standard_RAGRS
    network_acls:
      bypass: AzureServices,Metrics
      default_action: Deny
      virtual_network_rules:
        - id: /subscriptions/mySubscriptionId/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/mySubnet
          action: Allow
      ip_rules:
        - value: 1.2.3.4
          action: Allow
        - value: 123.234.123.0/24
          action: Allow

- name: create an account with blob CORS
  azure_rm_storageaccount:
    resource_group: myResourceGroup
    name: clh002
    type: Standard_RAGRS
    blob_cors:
      - allowed_origins:
          - http://www.example.com/
        allowed_methods:
          - GET
          - POST
        allowed_headers:
          - x-ms-meta-data*
          - x-ms-meta-target*
          - x-ms-meta-abc
        exposed_headers:
          - x-ms-meta-*
        max_age_in_seconds: 200

- name: Create new storage account with (key_source=Microsoft.Keyvault)
  azure.azcollection.azure_rm_storageaccount:
    resource_group: "{{ resource_group }}"
    name: "{{ storage_account_name }}"
    account_type: Standard_RAGRS
    kind: StorageV2
    identity:
      type: UserAssigned
      user_assigned_identity: "{{ managed_identity_ids[0] }}"
    encryption:
      services:
        blob:
          enabled: true
        file:
          enabled: true
      require_infrastructure_encryption: false
      key_source: Microsoft.Keyvault
      key_vault_properties:
        key_vault_uri: "https://vaultestfred001.vault.azure.net/"
        key_name: testkey
        key_version: 0bd2556671c64fc998095603878beb12
      encryption_identity:
        encryption_user_assigned_identity: "{{ managed_identity_ids[0] }}"
'''


RETURN = '''
state:
    description:
        - Current state of the storage account.
    returned: always
    type: complex
    contains:
        account_type:
            description:
                - Type of storage account.
            returned: always
            type: str
            sample: Standard_RAGRS
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
                encryption_identity:
                    description:
                        - The identity to be used with service-side encryption at rest.
                    type: dict
                    returned: always
                    sample: {"encryption_user_assigned_identity": \
                             "/subscriptions/xxxx/resourcegroups/testRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/identity-11"}
                key_vault_properties:
                    description:
                        - Dict of Microsoft Keyvault properties.
                        - Create the Storage account with encryption enabled with Microsoft KeyVault for CMK.
                    type: dict
                    returned: always
                    sample: {"key_name": "testkey",
                             "key_vault_uri": "https://vxxxxxxx01.vault.azure.net/",
                             "key_version": "0bd2556671c64fc998xxxxeb12"}
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/clh0003"
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
        location:
            description:
                - Valid Azure location. Defaults to location of the resource group.
            returned: always
            type: str
            sample: eastus2
        name:
            description:
                - Name of the storage account to update or create.
            returned: always
            type: str
            sample: clh0003
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
        primary_endpoints:
            description:
                - The URLs to retrieve the public I(blob), I(queue), or I(table) object from the primary location.
            returned: always
            type: dict
            sample: {
                    "blob": "https://clh0003.blob.core.windows.net/",
                    "queue": "https://clh0003.queue.core.windows.net/",
                    "table": "https://clh0003.table.core.windows.net/"
                    }
        primary_location:
            description:
                - The location of the primary data center for the storage account.
            returned: always
            type: str
            sample: eastus2
        provisioning_state:
            description:
                - The status of the storage account.
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
        resource_group:
            description:
                - The resource group's name.
            returned: always
            type: str
            sample: Testing
        secondary_endpoints:
            description:
                - The URLs to retrieve the public I(blob), I(queue), or I(table) object from the secondary location.
            returned: always
            type: dict
            sample: {
                    "blob": "https://clh0003-secondary.blob.core.windows.net/",
                    "queue": "https://clh0003-secondary.queue.core.windows.net/",
                    "table": "https://clh0003-secondary.table.core.windows.net/"
                    }
        secondary_location:
            description:
                - The location of the geo-replicated secondary for the storage account.
            returned: always
            type: str
            sample: centralus
        status_of_primary:
            description:
                - The status of the primary location of the storage account; either C(available) or C(unavailable).
            returned: always
            type: str
            sample: available
        status_of_secondary:
            description:
                - The status of the secondary location of the storage account; either C(available) or C(unavailable).
            returned: always
            type: str
            sample: available
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
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { 'tags1': 'value1' }
        type:
            description:
                - The storage account type.
            returned: always
            type: str
            sample: "Microsoft.Storage/storageAccounts"
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


import copy
import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AZURE_SUCCESS_STATE
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import env_fallback

try:
    from azure.mgmt.storage.models import (Identity, UserAssignedIdentity)
except ImportError:
    # This is handled in azure_rm_common
    pass

cors_rule_spec = dict(
    allowed_origins=dict(type='list', elements='str', required=True),
    allowed_methods=dict(type='list', elements='str', required=True),
    max_age_in_seconds=dict(type='int', required=True),
    exposed_headers=dict(type='list', elements='str', required=True),
    allowed_headers=dict(type='list', elements='str', required=True),
)

static_website_spec = dict(
    enabled=dict(type='bool', default=False),
    index_document=dict(type='str'),
    error_document404_path=dict(type='str'),
)


file_spec = dict(
    enabled=dict(type='bool')
)


queue_spec = dict(
    enabled=dict(type='bool')
)


table_spec = dict(
    enabled=dict(type='bool')
)


blob_spec = dict(
    enabled=dict(type='bool')
)


def compare_cors(cors1, cors2):
    if len(cors1) != len(cors2):
        return False
    copy2 = copy.copy(cors2)
    for rule1 in cors1:
        matched = False
        for rule2 in copy2:
            if (rule1['max_age_in_seconds'] == rule2['max_age_in_seconds']
                    and set(rule1['allowed_methods']) == set(rule2['allowed_methods'])
                    and set(rule1['allowed_origins']) == set(rule2['allowed_origins'])
                    and set(rule1['allowed_headers']) == set(rule2['allowed_headers'])
                    and set(rule1['exposed_headers']) == set(rule2['exposed_headers'])):
                matched = True
                copy2.remove(rule2)
        if not matched:
            return False
    return True


class AzureRMStorageAccount(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            auth_mode=dict(
                type='str',
                choices=['key', 'login'],
                fallback=(env_fallback, ['AZURE_STORAGE_AUTH_MODE']),
                default="key"
            ),
            account_type=dict(type='str',
                              choices=['Premium_LRS', 'Standard_GRS', 'Standard_LRS', 'Standard_RAGRS', 'Standard_ZRS', 'Premium_ZRS',
                                       'Standard_RAGZRS', 'Standard_GZRS'],
                              aliases=['type']),
            custom_domain=dict(type='dict', aliases=['custom_dns_domain_suffix']),
            location=dict(type='str'),
            name=dict(type='str', required=True),
            resource_group=dict(required=True, type='str', aliases=['resource_group_name']),
            state=dict(default='present', choices=['present', 'absent', 'failover']),
            force_delete_nonempty=dict(type='bool', default=False, aliases=['force']),
            tags=dict(type='dict'),
            kind=dict(type='str', default='Storage', choices=['Storage', 'StorageV2', 'BlobStorage', 'FileStorage', 'BlockBlobStorage']),
            access_tier=dict(type='str', choices=['Hot', 'Cool']),
            https_only=dict(type='bool'),
            minimum_tls_version=dict(type='str', choices=['TLS1_0', 'TLS1_1', 'TLS1_2']),
            public_network_access=dict(type='str', choices=['Enabled', 'Disabled']),
            allow_blob_public_access=dict(type='bool'),
            allow_shared_key_access=dict(type='bool'),
            allow_cross_tenant_replication=dict(type='bool'),
            default_to_o_auth_authentication=dict(type='bool'),
            network_acls=dict(type='dict'),
            blob_cors=dict(type='list', options=cors_rule_spec, elements='dict'),
            static_website=dict(type='dict', options=static_website_spec),
            is_hns_enabled=dict(type='bool'),
            large_file_shares_state=dict(type='str', choices=['Enabled', 'Disabled']),
            enable_nfs_v3=dict(type='bool'),
            encryption=dict(
                type='dict',
                options=dict(
                    services=dict(
                        type='dict',
                        options=dict(
                            blob=dict(
                                type='dict',
                                options=blob_spec
                            ),
                            table=dict(
                                type='dict',
                                options=table_spec
                            ),
                            queue=dict(
                                type='dict',
                                options=queue_spec
                            ),
                            file=dict(
                                type='dict',
                                options=file_spec
                            )
                        )
                    ),
                    require_infrastructure_encryption=dict(type='bool'),
                    key_source=dict(type='str', choices=["Microsoft.Storage", "Microsoft.Keyvault"], default='Microsoft.Storage'),
                    key_vault_properties=dict(
                        type='dict',
                        options=dict(
                            key_vault_uri=dict(type='str', required=True, no_log=True),
                            key_name=dict(type='str', required=True),
                            key_version=dict(type='str', no_log=True)
                        ), no_log=True
                    ),
                    encryption_identity=dict(
                        type='dict',
                        options=dict(
                            encryption_user_assigned_identity=dict(type='str', required=False)  # This will hold the resource ID of the user-assigned identity
                        )
                    )
                )
            ),
            identity=dict(
                type="dict",
                options=self.managed_identity_single_spec
            ),
            immutable_storage_with_versioning=dict(
                type='dict',
                options=dict(
                    enabled=dict(type='bool'),
                    immutability_policy=dict(
                        type='dict',
                        options=dict(
                            immutability_period_since_creation_in_days=dict(type='int'),
                            state=dict(type='str', choices=['Unlocked', 'Locked', 'Disabled']),
                            allow_protected_append_writes=dict(type='bool')
                        )
                    )
                )
            )
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.account_dict = None
        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.account_type = None
        self.custom_domain = None
        self.tags = None
        self.force_delete_nonempty = None
        self.kind = None
        self.access_tier = None
        self.https_only = None
        self.minimum_tls_version = None
        self.public_network_access = None
        self.allow_blob_public_access = None
        self.network_acls = None
        self.blob_cors = None
        self.static_website = None
        self.encryption = None
        self.is_hns_enabled = None
        self.large_file_shares_state = None
        self.enable_nfs_v3 = None
        self.allow_shared_key_access = None
        self.allow_cross_tenant_replication = None
        self.default_to_o_auth_authentication = None
        self._managed_identity = None
        self.identity = None
        self.update_identity = False
        self.immutable_storage_with_versioning = None

        super(AzureRMStorageAccount, self).__init__(self.module_arg_spec,
                                                    supports_check_mode=True)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {
                "identity": Identity,
                "user_assigned": UserAssignedIdentity,
            }
        return self._managed_identity

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        if len(self.name) < 3 or len(self.name) > 24:
            self.fail("Parameter error: name length must be between 3 and 24 characters.")

        if self.custom_domain:
            if self.custom_domain.get('name', None) is None:
                self.fail("Parameter error: expecting custom_domain to have a name attribute of type string.")
            if self.custom_domain.get('use_sub_domain', None) is None:
                self.fail("Parameter error: expecting custom_domain to have a use_sub_domain "
                          "attribute of type boolean.")

        if self.kind in ['FileStorage', 'BlockBlobStorage', ] and self.account_type not in ['Premium_LRS', 'Premium_ZRS']:
            self.fail("Parameter error: Storage account with {0} kind require account type is Premium_LRS or Premium_ZRS".format(self.kind))
        self.account_dict = self.get_account()

        curr_identity = self.account_dict["identity"] if self.account_dict else None

        if self.identity:
            self.update_identity, identity_result = self.update_single_managed_identity(curr_identity=curr_identity,
                                                                                        new_identity=self.identity,
                                                                                        patch_support=True)
            self.identity = identity_result.as_dict()

        if self.state == 'present' and self.account_dict and \
           self.account_dict['provisioning_state'] != AZURE_SUCCESS_STATE:
            self.fail("Error: storage account {0} has not completed provisioning. State is {1}. Expecting state "
                      "to be {2}.".format(self.name, self.account_dict['provisioning_state'], AZURE_SUCCESS_STATE))

        if self.account_dict is not None:
            self.results['state'] = self.account_dict
        else:
            self.results['state'] = dict()

        if self.state == 'present':
            if not self.account_dict:
                self.results['state'] = self.create_account()
            else:
                self.results['state'] = self.update_account()
        elif self.state == 'absent' and self.account_dict:
            self.delete_account()
            self.results['state'] = dict(Status='Deleted')
        elif self.state == 'failover' and self.account_dict:
            self.failover_account()
            self.results['state'] = self.get_account()

        return self.results

    def check_name_availability(self):
        self.log('Checking name availability for {0}'.format(self.name))
        try:
            account_name = self.storage_models.StorageAccountCheckNameAvailabilityParameters(name=self.name)
            self.storage_client.storage_accounts.check_name_availability(account_name)
        except Exception as e:
            self.log('Error attempting to validate name.')
            self.fail("Error checking name availability: {0}".format(str(e)))

    def get_account(self):
        self.log('Get properties for account {0}'.format(self.name))
        account_obj = None
        blob_mgmt_props = None
        blob_client_props = None
        account_dict = None

        try:
            account_obj = self.storage_client.storage_accounts.get_properties(self.resource_group, self.name)
            blob_mgmt_props = self.storage_client.blob_services.get_service_properties(self.resource_group, self.name)
            if self.kind != "FileStorage":
                blob_client_props = self.get_blob_service_client(self.resource_group, self.name, self.auth_mode).get_service_properties()
        except Exception:
            pass

        if account_obj:
            account_dict = self.account_obj_to_dict(account_obj, blob_mgmt_props, blob_client_props)

        return account_dict

    def account_obj_to_dict(self, account_obj, blob_mgmt_props=None, blob_client_props=None):
        account_dict = dict(
            id=account_obj.id,
            name=account_obj.name,
            location=account_obj.location,
            failover_in_progress=(account_obj.failover_in_progress
                                  if account_obj.failover_in_progress is not None else False),
            resource_group=self.resource_group,
            type=account_obj.type,
            access_tier=account_obj.access_tier,
            sku_tier=account_obj.sku.tier,
            sku_name=account_obj.sku.name,
            provisioning_state=account_obj.provisioning_state,
            secondary_location=account_obj.secondary_location,
            status_of_primary=account_obj.status_of_primary,
            status_of_secondary=account_obj.status_of_secondary,
            primary_location=account_obj.primary_location,
            https_only=account_obj.enable_https_traffic_only,
            minimum_tls_version=account_obj.minimum_tls_version,
            public_network_access=account_obj.public_network_access,
            allow_blob_public_access=account_obj.allow_blob_public_access,
            default_to_o_auth_authentication=account_obj.default_to_o_auth_authentication,
            allow_cross_tenant_replication=account_obj.allow_cross_tenant_replication,
            allow_shared_key_access=account_obj.allow_shared_key_access,
            network_acls=account_obj.network_rule_set,
            is_hns_enabled=account_obj.is_hns_enabled if account_obj.is_hns_enabled else False,
            enable_nfs_v3=account_obj.enable_nfs_v3 if hasattr(account_obj, 'enable_nfs_v3') else None,
            large_file_shares_state=account_obj.large_file_shares_state,
            static_website=dict(
                enabled=False,
                index_document=None,
                error_document404_path=None,
            ),
            immutable_storage_with_versioning=account_obj.immutable_storage_with_versioning.as_dict() if account_obj.immutable_storage_with_versioning else None
        )
        account_dict['custom_domain'] = None
        if account_obj.custom_domain:
            account_dict['custom_domain'] = dict(
                name=account_obj.custom_domain.name,
                use_sub_domain=account_obj.custom_domain.use_sub_domain
            )

        account_dict['primary_endpoints'] = None
        if account_obj.primary_endpoints:
            account_dict['primary_endpoints'] = dict(
                blob=account_obj.primary_endpoints.blob,
                queue=account_obj.primary_endpoints.queue,
                table=account_obj.primary_endpoints.table
            )
        account_dict['secondary_endpoints'] = None
        if account_obj.secondary_endpoints:
            account_dict['secondary_endpoints'] = dict(
                blob=account_obj.secondary_endpoints.blob,
                queue=account_obj.secondary_endpoints.queue,
                table=account_obj.secondary_endpoints.table
            )
        account_dict['tags'] = None
        if account_obj.tags:
            account_dict['tags'] = account_obj.tags
        if blob_mgmt_props and blob_mgmt_props.cors and blob_mgmt_props.cors.cors_rules:
            account_dict['blob_cors'] = [dict(
                allowed_origins=[to_native(y) for y in x.allowed_origins],
                allowed_methods=[to_native(y) for y in x.allowed_methods],
                max_age_in_seconds=x.max_age_in_seconds,
                exposed_headers=[to_native(y) for y in x.exposed_headers],
                allowed_headers=[to_native(y) for y in x.allowed_headers]
            ) for x in blob_mgmt_props.cors.cors_rules]

        if blob_client_props and blob_client_props['static_website']:
            static_website = blob_client_props['static_website']
            account_dict['static_website'] = dict(
                enabled=static_website.enabled,
                index_document=static_website.index_document,
                error_document404_path=static_website.error_document404_path,
            )

        account_dict['network_acls'] = None
        if account_obj.network_rule_set:
            account_dict['network_acls'] = dict(
                bypass=account_obj.network_rule_set.bypass,
                default_action=account_obj.network_rule_set.default_action
            )
            account_dict['network_acls']['virtual_network_rules'] = []
            if account_obj.network_rule_set.virtual_network_rules:
                for rule in account_obj.network_rule_set.virtual_network_rules:
                    account_dict['network_acls']['virtual_network_rules'].append(dict(id=rule.virtual_network_resource_id, action=rule.action))

            account_dict['network_acls']['ip_rules'] = []
            if account_obj.network_rule_set.ip_rules:
                for rule in account_obj.network_rule_set.ip_rules:
                    account_dict['network_acls']['ip_rules'].append(dict(value=rule.ip_address_or_range, action=rule.action))
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

                if account_obj.encryption.encryption_identity:
                    account_dict['encryption']['encryption_identity'] = dict(
                        encryption_user_assigned_identity=account_obj.encryption.encryption_identity.encryption_user_assigned_identity)
                else:
                    account_dict['encryption']['encryption_identity'] = None
                if account_obj.encryption.key_vault_properties:
                    account_dict['encryption']['key_vault_properties'] = dict(key_vault_uri=account_obj.encryption.key_vault_properties.key_vault_uri,
                                                                              key_name=account_obj.encryption.key_vault_properties.key_name,
                                                                              key_version=account_obj.encryption.key_vault_properties.key_version)
                else:
                    account_dict['encryption']['key_vault_properties'] = None

            account_dict['identity'] = dict()
            if account_obj.identity:
                account_dict['identity'] = account_obj.identity.as_dict()

        return account_dict

    def failover_account(self):

        if str(self.account_dict['sku_name']) not in ["Standard_GZRS", "Standard_GRS", "Standard_RAGZRS", "Standard_RAGRS"]:
            self.fail("Storage account SKU ({0}) does not support failover to a secondary region.".format(self.account_dict['sku_name']))
        try:
            account_obj = self.storage_client.storage_accounts.get_properties(self.resource_group, self.name, expand='georeplicationstats')
        except Exception as exc:
            self.fail("Error occured while acquiring geo-replication status. {0}".format(str(exc)))

        if account_obj.failover_in_progress:
            self.fail("Storage account is already in process of failing over to secondary region.")

        if not account_obj.geo_replication_stats.can_failover:
            self.fail("Storage account is unable to failover.  Secondary region has status of {0}".format(account_obj.geo_replication_stats.status))

        try:
            poller = self.storage_client.storage_accounts.begin_failover(self.resource_group, self.name)
            result = self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error occured while attempting a failover operation. {0}".format(str(exc)))

        self.results['changed'] = True
        return result

    def update_network_rule_set(self):
        if not self.check_mode:
            try:
                parameters = self.storage_models.StorageAccountUpdateParameters(network_rule_set=self.network_acls)
                self.storage_client.storage_accounts.update(self.resource_group,
                                                            self.name,
                                                            parameters)
            except Exception as exc:
                self.fail("Failed to update account type: {0}".format(str(exc)))

    def sort_list_of_dicts(self, rule_set, dict_key):
        return sorted(rule_set, key=lambda i: i[dict_key])

    def update_account(self):
        self.log('Update storage account {0}'.format(self.name))
        if self.network_acls:
            if self.network_acls.get('default_action', 'Allow') != self.account_dict['network_acls']['default_action']:
                self.results['changed'] = True
                self.account_dict['network_acls']['default_action'] = self.network_acls['default_action']
                self.update_network_rule_set()

            if self.network_acls.get('default_action', 'Allow') == 'Deny':
                if self.network_acls['bypass'] != self.account_dict['network_acls']['bypass']:
                    self.results['changed'] = True
                    self.account_dict['network_acls']['bypass'] = self.network_acls['bypass']
                    self.update_network_rule_set()

                if self.network_acls.get('virtual_network_rules', None) is not None and self.account_dict['network_acls']['virtual_network_rules'] != []:
                    if self.sort_list_of_dicts(self.network_acls['virtual_network_rules'], 'id') != \
                            self.sort_list_of_dicts(self.account_dict['network_acls']['virtual_network_rules'], 'id'):
                        self.results['changed'] = True
                        self.account_dict['network_acls']['virtual_network_rules'] = self.network_acls['virtual_network_rules']
                        self.update_network_rule_set()
                if self.network_acls.get('virtual_network_rules', None) is not None and self.account_dict['network_acls']['virtual_network_rules'] == []:
                    self.results['changed'] = True
                    self.update_network_rule_set()

                if self.network_acls.get('ip_rules', None) is not None and self.account_dict['network_acls']['ip_rules'] != []:
                    if self.sort_list_of_dicts(self.network_acls['ip_rules'], 'value') != \
                            self.sort_list_of_dicts(self.account_dict['network_acls']['ip_rules'], 'value'):
                        self.results['changed'] = True
                        self.account_dict['network_acls']['ip_rules'] = self.network_acls['ip_rules']
                        self.update_network_rule_set()
                if self.network_acls.get('ip_rules', None) is not None and self.account_dict['network_acls']['ip_rules'] == []:
                    self.results['changed'] = True
                    self.update_network_rule_set()

        if self.enable_nfs_v3 is not None and bool(self.enable_nfs_v3) != bool(self.account_dict.get('enable_nfs_v3')):
            self.results['changed'] = True
            self.account_dict['enable_nfs_v3'] = self.enable_nfs_v3

        if self.is_hns_enabled is not None and bool(self.is_hns_enabled) != bool(self.account_dict.get('is_hns_enabled')):
            self.results['changed'] = True
            self.account_dict['is_hns_enabled'] = self.is_hns_enabled
            if not self.check_mode:
                self.fail("The is_hns_enabled parameter not support to update, from {0} to {1}".
                          format(bool(self.account_dict.get('is_hns_enabled')), self.is_hns_enabled))

        if self.https_only is not None and bool(self.https_only) != bool(self.account_dict.get('https_only')):
            self.results['changed'] = True
            self.account_dict['https_only'] = self.https_only
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(enable_https_traffic_only=self.https_only)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update https only: {0}".format(str(exc)))

        if self.minimum_tls_version is not None and self.minimum_tls_version != self.account_dict.get('minimum_tls_version'):
            self.results['changed'] = True
            self.account_dict['minimum_tls_version'] = self.minimum_tls_version
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(minimum_tls_version=self.minimum_tls_version)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update minimum tls: {0}".format(str(exc)))

        if self.public_network_access is not None and self.public_network_access != self.account_dict.get('public_network_access'):
            self.results['changed'] = True
            self.account_dict['public_network_access'] = self.public_network_access
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(public_network_access=self.public_network_access)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update public network access: {0}".format(str(exc)))

        if self.allow_blob_public_access is not None and self.allow_blob_public_access != self.account_dict.get('allow_blob_public_access'):
            self.results['changed'] = True
            self.account_dict['allow_blob_public_access'] = self.allow_blob_public_access
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(allow_blob_public_access=self.allow_blob_public_access)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update allow public blob access: {0}".format(str(exc)))

        if self.allow_shared_key_access is not None and self.allow_shared_key_access != self.account_dict.get('allow_shared_key_access'):
            self.results['changed'] = True
            self.account_dict['allow_shared_key_access'] = self.allow_shared_key_access
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(allow_shared_key_access=self.allow_shared_key_access)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update allow shared key access: {0}".format(str(exc)))

        if self.allow_cross_tenant_replication is not None and self.allow_cross_tenant_replication != self.account_dict.get('allow_cross_tenant_replication'):
            self.results['changed'] = True
            self.account_dict['allow_cross_tenant_replication'] = self.allow_cross_tenant_replication
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(allow_cross_tenant_replication=self.allow_cross_tenant_replication)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update allow cross tenant replication: {0}".format(str(exc)))

        if self.default_to_o_auth_authentication is not None and \
           self.default_to_o_auth_authentication != self.account_dict.get('default_to_o_auth_authentication'):
            self.results['changed'] = True
            self.account_dict['default_to_o_auth_authentication'] = self.default_to_o_auth_authentication
            if not self.check_mode:
                try:
                    parameters = self.storage_models.StorageAccountUpdateParameters(default_to_o_auth_authentication=self.default_to_o_auth_authentication)
                    self.storage_client.storage_accounts.update(self.resource_group,
                                                                self.name,
                                                                parameters)
                except Exception as exc:
                    self.fail("Failed to update default_to_o_auth_authentication: {0}".format(str(exc)))

        if self.account_type:
            if self.account_type != self.account_dict['sku_name']:
                # change the account type
                SkuName = self.storage_models.SkuName
                if self.account_dict['sku_name'] in [SkuName.premium_lrs, SkuName.standard_zrs]:
                    self.fail("Storage accounts of type {0} and {1} cannot be changed.".format(
                        SkuName.premium_lrs, SkuName.standard_zrs))
                if self.account_type in [SkuName.premium_lrs, SkuName.standard_zrs]:
                    self.fail("Storage account of type {0} cannot be changed to a type of {1} or {2}.".format(
                        self.account_dict['sku_name'], SkuName.premium_lrs, SkuName.standard_zrs))

                self.results['changed'] = True
                self.account_dict['sku_name'] = self.account_type

                if self.results['changed'] and not self.check_mode:
                    # Perform the update. The API only allows changing one attribute per call.
                    try:
                        self.log("sku_name: %s" % self.account_dict['sku_name'])
                        self.log("sku_tier: %s" % self.account_dict['sku_tier'])
                        sku = self.storage_models.Sku(name=SkuName(self.account_dict['sku_name']))
                        sku.tier = self.storage_models.SkuTier(self.account_dict['sku_tier'])
                        parameters = self.storage_models.StorageAccountUpdateParameters(sku=sku)
                        self.storage_client.storage_accounts.update(self.resource_group,
                                                                    self.name,
                                                                    parameters)
                    except Exception as exc:
                        self.fail("Failed to update account type: {0}".format(str(exc)))

        if self.custom_domain:
            if not self.account_dict['custom_domain'] or self.account_dict['custom_domain'] != self.custom_domain:
                self.results['changed'] = True
                self.account_dict['custom_domain'] = self.custom_domain

            if self.results['changed'] and not self.check_mode:
                new_domain = self.storage_models.CustomDomain(name=self.custom_domain['name'],
                                                              use_sub_domain=self.custom_domain['use_sub_domain'])
                parameters = self.storage_models.StorageAccountUpdateParameters(custom_domain=new_domain)
                try:
                    self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
                except Exception as exc:
                    self.fail("Failed to update custom domain: {0}".format(str(exc)))

        if self.update_identity:
            self.results['changed'] = True
            parameters = self.storage_models.StorageAccountUpdateParameters(identity=self.identity)
            try:
                self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
            except Exception as exc:
                self.fail("Failed to update access tier: {0}".format(str(exc)))

        if self.access_tier:
            if not self.account_dict['access_tier'] or self.account_dict['access_tier'] != self.access_tier:
                self.results['changed'] = True
                self.account_dict['access_tier'] = self.access_tier

            if self.results['changed'] and not self.check_mode:
                parameters = self.storage_models.StorageAccountUpdateParameters(access_tier=self.access_tier)
                try:
                    self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
                except Exception as exc:
                    self.fail("Failed to update access tier: {0}".format(str(exc)))

        if self.large_file_shares_state is not None:
            if self.large_file_shares_state != self.account_dict['large_file_shares_state']:
                self.results['changed'] = True
                self.account_dict['large_file_shares_state'] = self.large_file_shares_state

            if self.results['changed'] and not self.check_mode:
                if self.large_file_shares_state == 'Disabled':
                    parameters = self.storage_models.StorageAccountUpdateParameters(large_file_shares_state=None)
                else:
                    parameters = self.storage_models.StorageAccountUpdateParameters(large_file_shares_state=self.large_file_shares_state)
                try:
                    self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
                except Exception as exc:
                    self.fail("Failed to update large_file_shares_state: {0}".format(str(exc)))

        update_tags, self.account_dict['tags'] = self.update_tags(self.account_dict['tags'])
        if update_tags:
            self.results['changed'] = True
            if not self.check_mode:
                parameters = self.storage_models.StorageAccountUpdateParameters(tags=self.account_dict['tags'])
                try:
                    self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
                except Exception as exc:
                    self.fail("Failed to update tags: {0}".format(str(exc)))

        if not self.default_compare({}, self.immutable_storage_with_versioning, self.account_dict['immutable_storage_with_versioning'], '', dict(compare=[])):
            self.results['changed'] = True
            if not self.check_mode:
                parameters = self.storage_models.StorageAccountUpdateParameters(immutable_storage_with_versioning=self.immutable_storage_with_versioning)
                try:
                    self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
                except Exception as exc:
                    self.fail("Failed to update immutable_storage_with_versioning: {0}".format(str(exc)))

        if self.blob_cors and not compare_cors(self.account_dict.get('blob_cors', []), self.blob_cors):
            self.results['changed'] = True
            if not self.check_mode:
                self.set_blob_cors()

        if self.static_website and self.static_website != self.account_dict.get("static_website", dict()):
            self.results['changed'] = True
            self.account_dict['static_website'] = self.static_website
            self.update_static_website()

        if self.encryption is not None:
            encryption_changed = False
            if self.encryption.get('require_infrastructure_encryption') and bool(self.encryption.get('require_infrastructure_encryption')) \
                    != bool(self.account_dict['encryption']['require_infrastructure_encryption']):
                encryption_changed = True

            if self.encryption.get('key_source') != self.account_dict['encryption']['key_source']:
                encryption_changed = True

            if self.encryption.get('services') is not None:
                if self.encryption.get('queue') is not None and self.account_dict['encryption']['services'].get('queue') is not None:
                    encryption_changed = True
                if self.encryption.get('file') is not None and self.account_dict['encryption']['services'].get('file') is not None:
                    encryption_changed = True
                if self.encryption.get('table') is not None and self.account_dict['encryption']['services'].get('table') is not None:
                    encryption_changed = True
                if self.encryption.get('blob') is not None and self.account_dict['encryption']['services'].get('blob') is not None:
                    encryption_changed = True
            if not self.default_compare({}, self.encryption.get('key_vault_properties'),
                                        self.account_dict['encryption'].get('key_vault_properties'), '', dict(compare=[])):
                encryption_changed = True
            if not self.default_compare({}, self.encryption.get('encryption_identity'),
                                        self.account_dict['encryption'].get('encryption_identity'), '', dict(compare=[])):
                encryption_changed = True

            if encryption_changed and not self.check_mode:
                self.fail("The encryption can't update encryption, encryption info as {0}".format(self.account_dict['encryption']))
        time.sleep(1)
        return self.get_account()

    def create_account(self):
        self.log("Creating account {0}".format(self.name))

        if not self.location:
            self.fail('Parameter error: location required when creating a storage account.')

        if not self.account_type:
            self.fail('Parameter error: account_type required when creating a storage account.')

        if not self.access_tier and self.kind == 'BlobStorage':
            self.fail('Parameter error: access_tier required when creating a storage account of type BlobStorage.')

        self.check_name_availability()
        self.results['changed'] = True

        if self.check_mode:
            account_dict = dict(
                location=self.location,
                account_type=self.account_type,
                name=self.name,
                resource_group=self.resource_group,
                enable_https_traffic_only=self.https_only,
                minimum_tls_version=self.minimum_tls_version,
                public_network_access=self.public_network_access,
                allow_blob_public_access=self.allow_blob_public_access,
                encryption=self.encryption,
                is_hns_enabled=self.is_hns_enabled,
                enable_nfs_v3=self.enable_nfs_v3,
                large_file_shares_state=self.large_file_shares_state,
                default_to_o_auth_authentication=self.default_to_o_auth_authentication,
                allow_cross_tenant_replication=self.allow_cross_tenant_replication,
                allow_shared_key_access=self.allow_shared_key_access,
                identity=self.identity,
                immutable_storage_with_versioning=self.immutable_storage_with_versioning,
                tags=dict()
            )
            if self.tags:
                account_dict['tags'] = self.tags
            if self.network_acls:
                account_dict['network_acls'] = self.network_acls
            if self.blob_cors:
                account_dict['blob_cors'] = self.blob_cors
            if self.static_website:
                account_dict['static_website'] = self.static_website
            return account_dict
        sku = self.storage_models.Sku(name=self.storage_models.SkuName(self.account_type))
        sku.tier = self.storage_models.SkuTier.standard if 'Standard' in self.account_type else \
            self.storage_models.SkuTier.premium
        # pylint: disable=missing-kwoa
        parameters = self.storage_models.StorageAccountCreateParameters(sku=sku,
                                                                        kind=self.kind,
                                                                        location=self.location,
                                                                        tags=self.tags,
                                                                        identity=self.identity,
                                                                        enable_https_traffic_only=self.https_only,
                                                                        minimum_tls_version=self.minimum_tls_version,
                                                                        public_network_access=self.public_network_access,
                                                                        allow_blob_public_access=self.allow_blob_public_access,
                                                                        encryption=self.encryption,
                                                                        is_hns_enabled=self.is_hns_enabled,
                                                                        enable_nfs_v3=self.enable_nfs_v3,
                                                                        access_tier=self.access_tier,
                                                                        allow_shared_key_access=self.allow_shared_key_access,
                                                                        default_to_o_auth_authentication=self.default_to_o_auth_authentication,
                                                                        allow_cross_tenant_replication=self.allow_cross_tenant_replication,
                                                                        immutable_storage_with_versioning=self.immutable_storage_with_versioning,
                                                                        large_file_shares_state=self.large_file_shares_state)
        self.log(str(parameters))
        try:
            poller = self.storage_client.storage_accounts.begin_create(self.resource_group, self.name, parameters)
            self.get_poller_result(poller)
        except Exception as e:
            self.log('Error creating storage account.')
            self.fail("Failed to create account: {0}".format(str(e)))
        if self.network_acls:
            self.set_network_acls()
        if self.blob_cors:
            self.set_blob_cors()
        if self.static_website:
            self.update_static_website()
        return self.get_account()

    def delete_account(self):
        if self.account_dict['provisioning_state'] == self.storage_models.ProvisioningState.succeeded.value and \
           not self.force_delete_nonempty and self.account_has_blob_containers():
            self.fail("Account contains blob containers. Is it in use? Use the force_delete_nonempty option to attempt deletion.")

        self.log('Delete storage account {0}'.format(self.name))
        self.results['changed'] = True
        if not self.check_mode:
            try:
                status = self.storage_client.storage_accounts.delete(self.resource_group, self.name)
                self.log("delete status: ")
                self.log(str(status))
            except Exception as e:
                self.fail("Failed to delete the account: {0}".format(str(e)))
        return True

    def account_has_blob_containers(self):
        '''
        If there are blob containers, then there are likely VMs depending on this account and it should
        not be deleted.
        '''
        if self.kind == "FileStorage":
            return False
        self.log('Checking for existing blob containers')
        blob_service = self.get_blob_service_client(self.resource_group, self.name, self.auth_mode)
        try:
            response = blob_service.list_containers()
        except Exception:
            # No blob storage available?
            return False

        if len(list(response)) > 0:
            return True
        return False

    def set_blob_cors(self):
        try:
            cors_rules = self.storage_models.CorsRules(cors_rules=[self.storage_models.CorsRule(**x) for x in self.blob_cors])
            self.storage_client.blob_services.set_service_properties(self.resource_group,
                                                                     self.name,
                                                                     self.storage_models.BlobServiceProperties(cors=cors_rules))
        except Exception as exc:
            self.fail("Failed to set CORS rules: {0}".format(str(exc)))

    def update_static_website(self):
        if self.kind == "FileStorage":
            return
        try:
            self.get_blob_service_client(self.resource_group, self.name, self.auth_mode).set_service_properties(static_website=self.static_website)
        except Exception as exc:
            self.fail("Failed to set static website config: {0}".format(str(exc)))

    def set_network_acls(self):
        try:
            parameters = self.storage_models.StorageAccountUpdateParameters(network_rule_set=self.network_acls)
            self.storage_client.storage_accounts.update(self.resource_group,
                                                        self.name,
                                                        parameters)
        except Exception as exc:
            self.fail("Failed to update account type: {0}".format(str(exc)))


def main():
    AzureRMStorageAccount()


if __name__ == '__main__':
    main()

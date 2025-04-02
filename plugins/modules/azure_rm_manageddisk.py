#!/usr/bin/python
#
# Copyright (c) 2017 Bruno Medina Bolanos Cacho <bruno.medina@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_manageddisk

version_added: "0.1.2"

short_description: Manage Azure Manage Disks

description:
    - Create, update and delete an Azure Managed Disk.

notes:
    - This module was called M(azure.azcollection.azure_rm_managed_disk) before Ansible 2.8. The usage did not change.

options:
    resource_group:
        description:
            - Name of a resource group where the managed disk exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of the managed disk.
        required: true
        type: str
    state:
        description:
            - Assert the state of the managed disk. Use C(present) to create or update a managed disk and C(absent) to delete a managed disk.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    storage_account_type:
        description:
            - Type of storage for the managed disk.
            - If not specified, the disk is created as C(Standard_LRS).
            - C(Standard_LRS) is for Standard HDD.
            - C(StandardSSD_LRS) (added in 2.8) is for Standard SSD.
            - C(StandardSSD_ZRS) is for Standard SSD Zone-redundant.
            - C(Premium_LRS) is for Premium SSD.
            - C(Premium_ZRS) is for Premium SSD Zone-redundant.
            - C(UltraSSD_LRS) (added in 2.8) is for Ultra SSD, which is only available on select instance types.
            - See U(https://docs.microsoft.com/en-us/azure/virtual-machines/windows/disks-types) for more information about disk types.
        type: str
        choices:
            - Standard_LRS
            - StandardSSD_LRS
            - StandardSSD_ZRS
            - Premium_LRS
            - PremiumV2_LRS
            - Premium_ZRS
            - UltraSSD_LRS
    create_option:
        description:
            - C(import) from a VHD file in I(source_uri) and C(copy) from previous managed disk I(source_uri).
        type: str
        choices:
            - empty
            - import
            - copy
            - upload
            - fromimage
            - restore
            - uploadpreparedsecure
    storage_account_id:
        description:
            - The full path to the storage account the image is to be imported from.
            - Required when I(create_option=import).
        type: str
    source_uri:
        description:
            - URI to a valid VHD file to be used or the resource ID of the managed disk to copy.
        type: str
        aliases:
            - source_resource_uri
    os_type:
        description:
            - Type of Operating System.
            - Used when I(create_option=copy) or I(create_option=import) and the source is an OS disk.
            - If omitted during creation, no value is set.
            - If omitted during an update, no change is made.
            - Once set, this value cannot be cleared.
        type: str
        choices:
            - linux
            - windows
            - Linux
            - Windows
    disk_size_gb:
        description:
            - Size in GB of the managed disk to be created.
            - If I(create_option=copy) then the value must be greater than or equal to the source's size.
        type: int
    managed_by:
        description:
            - Name of an existing virtual machine with which the disk is or will be associated, this VM should be in the same resource group.
            - To detach a disk from a vm, explicitly set to ''.
            - If this option is unset, the value will not be changed.
        type: str
    managed_by_extended:
        description:
            - List of name and resource group of the VMs that have the disk attached.
            - I(max_shares) should be set to a value greater than one for disks to allow attaching them to multiple VMs.
        type: list
        elements: dict
        suboptions:
            resource_group:
                description:
                    - The resource group of the attache VM.
                type: str
            name:
                description:
                    - The name of the attache VM.
                type: str
    max_shares:
        description:
            - The maximum number of VMs that can attach to the disk at the same time.
            - Value greater than one indicates a disk that can be mounted on multiple VMs at the same time.
        type: int
    attach_caching:
        description:
            - Disk caching policy controlled by VM. Will be used when attached to the VM defined by C(managed_by).
            - If this option is different from the current caching policy, the managed disk will be deattached and attached with current caching option again.
        type: str
        choices:
            - ''
            - read_only
            - read_write
    zone:
        description:
            - The Azure managed disk's zone.
            - Allowed values are C(1), C(2), C(3) and C('').
        type: str
        choices:
            - '1'
            - '2'
            - '3'
            - ''
    lun:
        description:
            - The logical unit number for data disk.
            - This value is used to identify data disks within the VM and therefore must be unique for each data disk attached to a VM.
        type: int
    disk_iops_read_write:
        description:
            - The number of IOPS allowed for this disk.
            - Only settable for I(storage_account_type=UltraSSD_LRS) disks.
            - One operation can transfer between 4k and 256k bytes.
        type: int
    disk_m_bps_read_write:
        description:
            - The bandwidth allowed for this disk.
            - Only settable for I(storage_account_type=UltraSSD_LRS) disks.
            - One operation can transfer between 4k and 256k bytes.
        type: int
    disk_iops_read_only:
        description:
            - The total throughput (MBps) that will be allowed across all VMs mounting the shared disk as ReadOnly.
            - One operation can transfer between 4k and 256k bytes.
        type: int
    disk_m_bps_read_only:
        description:
            - The total throughput (MBps) that will be allowed across all VMs mounting the shared disk as ReadOnly.
            - MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
        type: int
    tier:
        description:
            - Performance tier assigned to this disk.
            - Only settable for I(storage_account_type=Premium_LRS) disks.
            - Allowed values are C(P1), C(P2), C(P3), C(P4), C(P6), C(P10), C(P15), C(P20), C(P30), C(P40), C(P50), C(P60), C(P70), C(P80)
            - See U(https://learn.microsoft.com/en-us/azure/virtual-machines/disks-change-performance) for more information about disk performance tiers.
            - Does not apply to Ultra disks.
        type: str
        choices:
            - P1
            - P2
            - P3
            - P4
            - P6
            - P10
            - P15
            - P20
            - P30
            - P40
            - P50
            - P60
            - P70
            - P80
    network_access_policy:
        description:
            - Policy for accessing the disk via network.
        type: str
        choices:
            - AllowAll
            - AllowPrivate
            - DenyAll
    public_network_access:
        description:
            - Policy for controlling export on the disk.
        type: str
        choices:
            - Enabled
            - Disabled
    write_accelerator_enabled:
        description:
            - Specifies whether writeAccelerator should be enabled or disabled on the disk.
        type: bool
    disk_access_id:
        description:
            - ARM ID of the DiskAccess resource for using private endpoints on disks.
        type: str
    performance_plus:
        description:
            - Set this flag to true to get a boost on the performance target of the disk deployed, see here on the respective performance target.
            - This flag can only be set on disk creation time and cannot be disabled after enabled.
        type: bool
    upload_size_bytes:
        description:
            - If I(create_option=upload), this is the size of the contents of the upload including the VHD footer.
            - This value should be between 20972032 (20 MiB + 512 bytes for the VHD footer) and 35183298347520 bytes (32 TiB + 512 bytes for the VHD footer).
        type: int
    gallery_image_reference:
        description:
            - Required if creating from a Gallery Image.
            - The id/sharedGalleryImageId/communityGalleryImageId of the ImageDiskReference
              will be the ARM id of the shared galley image version from which to create a disk.
        type: dict
        suboptions:
            id:
                description:
                    - A relative uri containing either a Platform Image Repository, user image, or Azure Compute Gallery image reference.
                type: str
            shared_gallery_image_id:
                description:
                    - A relative uri containing a direct shared Azure Compute Gallery image reference.
                type: str
            community_gallery_image_id:
                description:
                    - A relative uri containing a community Azure Compute Gallery image reference.
                type: str
    image_reference:
        description:
            - Disk source information for PIR or user images or Gallery Image.
        type: dict
        suboptions:
            id:
                description:
                    - A relative uri containing either a Platform Image Repository, user image, or Azure Compute Gallery image reference.
                type: str
            shared_gallery_image_id:
                description:
                    - A relative uri containing a direct shared Azure Compute Gallery image reference.
                type: str
            community_gallery_image_id:
                description:
                    - A relative uri containing a community Azure Compute Gallery image reference.
                type: str
    logical_sector_size:
        description:
            - Logical sector size in bytes for Ultra disks.
            - Supported values are 512 ad 4096. 4096 is the default.
        type: int
    source_resource_id:
        description:
            - If I(create_option=copy), this is the ARM id of the source snapshot or disk.
        type: str
    security_profile:
        description:
            - Contains the security related information for the resource.
        type: dict
        suboptions:
            security_type:
                description:
                    - Specifies the SecurityType of the VM. Applicable for OS disks only.
                type: str
                choices:
                    - TrustedLaunch
                    - ConfidentialVM_VMGuestStateOnlyEncryptedWithPlatformKey
                    - ConfidentialVM_DiskEncryptedWithPlatformKey
                    - ConfidentialVM_DiskEncryptedWithCustomerKey
            secure_vm_disk_encryption_set_id:
                description:
                    - ResourceId of the disk encryption set associated to Confidential VM supported disk encrypted with customer managed key.
                type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Bruno Medina (@brusMX)
'''

EXAMPLES = '''
- name: Create managed disk
  azure_rm_manageddisk:
    name: mymanageddisk
    location: eastus
    resource_group: myResourceGroup
    disk_size_gb: 4

- name: Create managed operating system disk from page blob
  azure_rm_manageddisk:
    name: mymanageddisk
    location: eastus2
    resource_group: myResourceGroup
    create_option: import
    source_uri: https://storageaccountname.blob.core.windows.net/containername/blob-name.vhd
    storage_account_id: /subscriptions/<uuid>/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/storageaccountname
    os_type: windows
    storage_account_type: Premium_LRS

- name: Create managed disk with I(create_option=upload)
  azure_rm_manageddisk:
    resource_group: myResourceGroup
    name: mymanageddisk
    storage_account_type: "Standard_LRS"
    upload_size_bytes: 20972032
    network_access_policy: DenyAll
    public_network_access: Disabled
    create_option: upload

- name: Create managed disk with I(create_option=fromimage)
  azure_rm_manageddisk:
    resource_group: "{{ resource_group }}"
    name: "md{{ rpfx }}"
    storage_account_type: "Standard_LRS"
    disk_size_gb: 1024
    network_access_policy: DenyAll
    public_network_access: Disabled
    create_option: fromimage
    os_type: windows
    security_profile:
      security_type: TrustedLaunch
    gallery_image_reference:
      id: "/subscriptions/xxxx/resourceGroups/testRG/providers/Microsoft.Compute/galleries/Gallery01/images/windowsVMimage/versions/0.0.1"

- name: Create managed disk with I(create_option=restore)
  azure_rm_manageddisk:
    resource_group: "{{ resource_group }}"
    name: "md{{ rpfx }}"
    storage_account_type: "Standard_LRS"
    disk_size_gb: 1024
    network_access_policy: DenyAll
    public_network_access: Disabled
    performance_plus: true
    source_resource_id: "/subscriptions/xxxx/resourceGroups/testRG/providers/Microsoft.Compute/
                         restorePointCollections/point01/restorePoints/restorepoint01/diskRestorePoints/testVM_OsDisk_1"
    create_option: restore

- name: Create managed disk with I(create_option=uploadpreparedsecure)
  azure_rm_manageddisk:
    resource_group: "{{ resource_group }}"
    name: "md{{ rpfx }}"
    storage_account_type: "Standard_LRS"
    upload_size_bytes: 20972032
    network_access_policy: DenyAll
    public_network_access: Disabled
    create_option: uploadpreparedsecure
    security_profile:
      security_type: TrustedLaunch

- name: Mount the managed disk to VM
  azure_rm_manageddisk:
    name: mymanageddisk
    location: eastus
    resource_group: myResourceGroup
    disk_size_gb: 4
    managed_by: testvm001
    attach_caching: read_only

- name: Mount the managed disk to multiple VMs
  azure_rm_manageddisk:
    resource_group: myResourceGroup
    name: freddisk04
    max_shares: 4
    disk_size_gb: 1024
    storage_account_type: Premium_LRS
    managed_by_extended:
      - resource_group: myResourceGroup01
        name: testVM01
      - resource_group: myResourceGroup02
        name: testVM02
    zone: 1

- name: Unmount the managed disk to VM
  azure_rm_manageddisk:
    name: mymanageddisk
    location: eastus
    resource_group: myResourceGroup
    managed_by: ''
    disk_size_gb: 4

- name: Delete managed disk
  azure_rm_manageddisk:
    name: mymanageddisk
    location: eastus
    resource_group: myResourceGroup
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the managed disk.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource id.
            type: str
        name:
            description:
                - Name of the managed disk.
            type: str
        location:
            description:
                - Valid Azure location.
            type: str
        storage_account_type:
            description:
                - Type of storage for the managed disk.
                - See U(https://docs.microsoft.com/en-us/azure/virtual-machines/windows/disks-types) for more information about this type.
            type: str
            sample: Standard_LRS
        create_option:
            description:
                - Create option of the disk.
            type: str
            sample: copy
        storage_account_id:
            description:
                - The full path to the storage account the image is to be imported from
            type: str
            sample: /subscriptions/<uuid>/resourceGroups/<resource group name>/providers/Microsoft.Storage/storageAccounts/<storage account name>
        source_uri:
            description:
                - URI to a valid VHD file to be used or the resource ID of the managed disk to copy.
            type: str
        os_type:
            description:
                - Type of Operating System.
            type: str
            sample: linux
        disk_size_gb:
            description:
                - Size in GB of the managed disk to be created.
            type: str
        managed_by:
            description:
                - Name of an existing virtual machine with which the disk is or will be associated, this VM should be in the same resource group.
            type: str
        max_shares:
            description:
                - The maximum number of VMs that can attach to the disk at the same time.
                - Value greater than one indicates a disk that can be mounted on multiple VMs at the same time.
            type: int
            sample: 3
        managed_by_extended:
            description:
                - List ID of an existing virtual machine with which the disk is or will be associated.
            type: list
            sample: ["/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/testVM"]
        tags:
            description:
                - Tags to assign to the managed disk.
            type: dict
            sample: { "tag": "value" }
        disk_iops_read_write:
            description:
                - The number of IOPS allowed for this disk.
                - Only settable for I(storage_account_type=UltraSSD_LRS) disks.
                - One operation can transfer between 4k and 256k bytes.
            type: int
            returned: always
            sample: 200
        disk_m_bps_read_write:
            description:
                - The bandwidth allowed for this disk.
                - Only settable for I(storage_account_type=UltraSSD_LRS) disks.
                - One operation can transfer between 4k and 256k bytes.
            type: int
            returned: always
            sample: 30
        disk_iops_read_only:
            description:
                - The total throughput (MBps) that will be allowed across all VMs mounting the shared disk as ReadOnly.
                - One operation can transfer between 4k and 256k bytes.
            type: int
            returned: always
            sample: 200
        disk_m_bps_read_only:
            description:
                - The total throughput (MBps) that will be allowed across all VMs mounting the shared disk as ReadOnly.
                - MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
            type: int
            returned: always
            sample: 30
        tier:
            description:
                - Performance tier assigned to the managed disk.
            type: str
            sample: "P30"
        network_access_policy:
            description:
                - Policy for accessing the disk via network.
            type: str
            returned: always
            sample: AllowAll
        public_network_access:
            description:
                - Policy for controlling export on the disk.
            type: str
            returned: always
            sample: Enabled
        disk_access_id:
            description:
                - ARM ID of the DiskAccess resource for using private endpoints on disks.
            type: str
            returned: always
            sample: '/subscriptions/*********/resourceGroups/myRG/providers/Microsoft.Compute/diskAccesses/diskacc'
        performance_plus:
            description:
                - The flag of the performance target of the disk deployed.
            type: bool
            returned: always
            sample: False
        upload_size_bytes:
            description:
                - This is the size of the contents of the upload including the VHD footer.
            type: int
            returned: always
            sample: None
        image_reference:
            description:
                - Disk source information for PIR or user images or Gallery Image.
            type: dict
            returned: always
            sample: None
        gallery_image_reference:
            description:
                - The Gallery Image info.
            type: dict
            returned: always
            sample: None
        logical_sector_size:
            description:
                - Logical sector size in bytes for Ultra disks.
            type: int
            returned: always
            sample: None
        source_resource_id:
            description:
                - This is the ARM id of the source snapshot or disk.
            type: str
            returned: always
            sample: None
        security_profile:
            description:
                - The security related information for the resource.
            type: complex
            contains:
                security_type:
                    description:
                        - Specifies the SecurityType of the VM.
                    type: str
                    returned: when-used
                    sample: TrustedLaunch
                secure_vm_disk_encryption_set_id:
                    description:
                        -  ResourceId of the disk encryption set associated to Confidential VM supported disk encrypted with customer managed key.
                    type: str
                    returned: when-used
                    sample: None
changed:
    description:
        - Whether or not the resource has changed.
    returned: always
    type: bool
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from concurrent.futures import ThreadPoolExecutor
    import multiprocessing
    from azure.mgmt.core.tools import parse_resource_id
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


managed_by_extended_spec = dict(
    resource_group=dict(type='str'),
    name=dict(type='str')
)


# duplicated in azure_rm_manageddisk_facts
def managed_disk_to_dict(managed_disk):
    create_data = managed_disk.creation_data
    return dict(
        id=managed_disk.id,
        name=managed_disk.name,
        location=managed_disk.location,
        tags=managed_disk.tags,
        create_option=create_data.create_option.lower(),
        source_uri=create_data.source_uri,
        disk_size_gb=managed_disk.disk_size_gb,
        os_type=managed_disk.os_type.lower() if managed_disk.os_type else None,
        storage_account_type=managed_disk.sku.name if managed_disk.sku else None,
        managed_by=managed_disk.managed_by,
        max_shares=managed_disk.max_shares,
        managed_by_extended=managed_disk.managed_by_extended,
        zone=managed_disk.zones[0] if managed_disk.zones and len(managed_disk.zones) > 0 else '',
        disk_iops_read_write=managed_disk.disk_iops_read_write,
        disk_m_bps_read_write=managed_disk.disk_m_bps_read_write,
        disk_iops_read_only=managed_disk.disk_iops_read_only,
        disk_m_bps_read_only=managed_disk.disk_m_bps_read_only,
        tier=managed_disk.tier,
        public_network_access=managed_disk.public_network_access,
        network_access_policy=managed_disk.network_access_policy,
        disk_access_id=managed_disk.disk_access_id,
        source_resource_id=create_data.source_resource_id,
        storage_account_id=create_data.storage_account_id,
        upload_size_bytes=create_data.upload_size_bytes,
        logical_sector_size=create_data.logical_sector_size,
        performance_plus=create_data.performance_plus,
        gallery_image_reference=dict(
            id=create_data.gallery_image_reference.id,
            shared_gallery_image_id=create_data.gallery_image_reference.shared_gallery_image_id,
            community_gallery_image_id=create_data.gallery_image_reference.community_gallery_image_id
        ) if create_data.gallery_image_reference is not None else None,
        image_reference=dict(
            id=create_data.image_reference.id,
            shared_gallery_image_id=create_data.image_reference.shared_gallery_image_id,
            community_gallery_image_id=create_data.image_reference.community_gallery_image_id
        ) if create_data.image_reference is not None else None,
        security_profile=dict(
            security_type=managed_disk.security_profile.security_type,
            secure_vm_disk_encryption_set_id=managed_disk.security_profile.secure_vm_disk_encryption_set_id
        ) if managed_disk.security_profile is not None else None
    )


class AzureRMManagedDisk(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Disk resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str'
            ),
            storage_account_type=dict(
                type='str',
                choices=['Standard_LRS', 'StandardSSD_LRS', 'StandardSSD_ZRS', 'Premium_LRS', 'Premium_ZRS', 'UltraSSD_LRS', 'PremiumV2_LRS']
            ),
            create_option=dict(
                type='str',
                choices=['empty', 'import', 'copy', 'upload', 'fromimage', 'restore', 'uploadpreparedsecure']
            ),
            storage_account_id=dict(
                type='str'
            ),
            source_uri=dict(
                type='str',
                aliases=['source_resource_uri']
            ),
            os_type=dict(
                type='str',
                choices=['linux', 'windows', 'Linux', 'Windows']
            ),
            disk_size_gb=dict(
                type='int'
            ),
            managed_by=dict(
                type='str'
            ),
            zone=dict(
                type='str',
                choices=['', '1', '2', '3']
            ),
            attach_caching=dict(
                type='str',
                choices=['', 'read_only', 'read_write']
            ),
            lun=dict(
                type='int'
            ),
            max_shares=dict(
                type='int'
            ),
            managed_by_extended=dict(
                type='list',
                elements='dict',
                options=managed_by_extended_spec
            ),
            disk_iops_read_only=dict(
                type='int'
            ),
            disk_iops_read_write=dict(
                type='int'
            ),
            disk_m_bps_read_only=dict(
                type='int'
            ),
            disk_m_bps_read_write=dict(
                type='int'
            ),
            tier=dict(
                type='str',
                choices=['P1', 'P2', 'P3', 'P4', 'P6', 'P10', 'P15', 'P20', 'P30', 'P40', 'P50', 'P60', 'P70', 'P80']
            ),
            public_network_access=dict(
                type='str',
                choices=['Enabled', 'Disabled']
            ),
            write_accelerator_enabled=dict(
                type='bool',
            ),
            network_access_policy=dict(
                type='str',
                choices=['AllowAll', 'AllowPrivate', 'DenyAll']
            ),
            disk_access_id=dict(
                type='str'
            ),
            performance_plus=dict(type='bool'),
            upload_size_bytes=dict(type='int'),
            gallery_image_reference=dict(
                type='dict',
                options=dict(
                    id=dict(type='str'),
                    shared_gallery_image_id=dict(type='str'),
                    community_gallery_image_id=dict(type='str')
                )
            ),
            image_reference=dict(
                type='dict',
                options=dict(
                    id=dict(type='str'),
                    shared_gallery_image_id=dict(type='str'),
                    community_gallery_image_id=dict(type='str')
                )
            ),
            logical_sector_size=dict(
                type='int',
            ),
            source_resource_id=dict(
                type='str'
            ),
            security_profile=dict(
                type='dict',
                options=dict(
                    security_type=dict(
                        type='str',
                        choices=["TrustedLaunch", "ConfidentialVM_VMGuestStateOnlyEncryptedWithPlatformKey",
                                 "ConfidentialVM_DiskEncryptedWithPlatformKey", "ConfidentialVM_DiskEncryptedWithCustomerKey"]
                    ),
                    secure_vm_disk_encryption_set_id=dict(type='str')
                )
            )
        )
        required_if = [
            ('create_option', 'import', ['source_uri', 'storage_account_id']),
            ('create_option', 'copy', ['source_resource_id']),
            ('create_option', 'empty', ['disk_size_gb']),
            ('create_option', 'upload', ['upload_size_bytes']),
            ('create_option', 'restore', ['source_resource_id']),
            ('create_option', 'uploadpreparedsecure', ['upload_size_bytes', 'security_profile']),
            ('network_access_policy', 'AllowPrivate', ['disk_access_id'])
        ]
        self.results = dict(
            changed=False,
            state=dict())

        self.resource_group = None
        self.name = None
        self.location = None
        self.storage_account_type = None
        self.create_option = None
        self.storage_account_id = None
        self.source_uri = None
        self.os_type = None
        self.disk_size_gb = None
        self.tags = None
        self.zone = None
        self.managed_by = None
        self.attach_caching = None
        self.lun = None
        self.max_shares = None
        self.managed_by_extended = None
        self.disk_iops_read_write = None
        self.disk_m_bps_read_write = None
        self.disk_iops_read_only = None
        self.disk_m_bps_read_only = None
        self.tier = None
        self.public_network_access = None
        self.network_access_policy = None
        self.write_accelerator_enabled = None
        self.disk_access_id = None
        self.performance_plus = None
        self.upload_size_bytes = None
        self.source_resource_id = None
        self.image_reference = None
        self.gallery_image_reference = None
        self.logical_sector_size = None
        self.security_profile = None

        mutually_exclusive = [['managed_by_extended', 'managed_by'], ['image_reference', 'gallery_image_reference']]

        super(AzureRMManagedDisk, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            required_if=required_if,
            supports_check_mode=True,
            mutually_exclusive=mutually_exclusive,
            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        result = None
        changed = False
        update_flag = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        disk_instance = self.get_managed_disk()
        if disk_instance is not None:
            update_flag = True
            if self.create_option is None:
                self.create_option = disk_instance.get('create_option')
            if self.source_uri is None:
                self.source_uri = disk_instance.get('source_uri')
            if self.disk_size_gb is None:
                self.disk_size_gb = disk_instance.get('disk_size_gb')
            if self.os_type is None:
                self.os_type = disk_instance.get('os_type')
            if self.zone is None:
                self.zone = disk_instance.get('zone')
            if self.public_network_access is None:
                self.public_network_access = disk_instance.get('public_network_access')
            if self.network_access_policy is None:
                self.network_access_policy = disk_instance.get('network_access_policy')
            if self.disk_access_id is None:
                self.disk_access_id = disk_instance.get('disk_access_id')
            if self.upload_size_bytes is None:
                self.upload_size_bytes = disk_instance.get('upload_size_bytes')
            if self.image_reference is None:
                self.image_reference = disk_instance.get('image_reference')
            if self.gallery_image_reference is None:
                self.gallery_image_reference = disk_instance.get('gallery_image_reference')

        result = disk_instance

        # need create or update
        if self.state == 'present':
            parameter = self.generate_managed_disk_property()
            if not disk_instance or self.is_different(disk_instance, parameter):
                changed = True
                if not self.check_mode:
                    result = self.create_or_update_managed_disk(parameter, update_flag)
                else:
                    result = True

        # Mount the disk to multiple VM
        if self.managed_by_extended:
            if not self.check_mode:
                cpu_count = multiprocessing.cpu_count()
                executor = ThreadPoolExecutor(max_workers=cpu_count)
                task_result = []
                for vm_item in self.managed_by_extended:
                    vm_name_id = self.compute_client.virtual_machines.get(vm_item['resource_group'], vm_item['name'])
                    if result['managed_by_extended'] is None or vm_name_id.id not in result['managed_by_extended']:
                        changed = True
                        feature = executor.submit(self.attach, vm_item['resource_group'], vm_item['name'], result)
                        task_result.append({'task': feature, 'vm_name': vm_item['name'], 'resource_group': vm_item['resource_group']})
                fail_attach_VM = []
                for task_item in task_result:
                    if task_item['task'].result() is not None:
                        task_item['error_msg'] = task_item['task'].result()
                        task_item.pop('task')
                        fail_attach_VM.append(task_item)
                if len(fail_attach_VM) > 0:
                    self.fail("Disk mount failure, VM and Error message information: {0}".format(fail_attach_VM))

                result = self.get_managed_disk()

        # unmount from the old virtual machine and mount to the new virtual machine
        if self.managed_by or self.managed_by == '':
            vm_name = parse_resource_id(disk_instance.get('managed_by', '')).get('name') if disk_instance else None
            resource_group = parse_resource_id(disk_instance.get('managed_by', '')).get('resource_group') if disk_instance else None
            vm_name = vm_name or ''
            if self.managed_by != vm_name or self.is_attach_caching_option_different(vm_name, result):
                changed = True
                if not self.check_mode:
                    if vm_name:
                        self.detach(resource_group, vm_name, result)
                    if self.managed_by:
                        self.attach(self.resource_group, self.managed_by, result)
                    result = self.get_managed_disk()

        if self.state == 'absent' and disk_instance:
            changed = True
            if not self.check_mode:
                self.delete_managed_disk()
            result = True

        self.results['changed'] = changed
        self.results['state'] = result
        return self.results

    def attach(self, resource_group, vm_name, disk):
        vm = self._get_vm(resource_group, vm_name)
        # find the lun
        if self.lun:
            lun = self.lun
        else:
            luns = ([d.lun for d in vm.storage_profile.data_disks]
                    if vm.storage_profile.data_disks else [])
            lun = 0
            while True:
                if lun not in luns:
                    break
                lun = lun + 1
            for item in vm.storage_profile.data_disks:
                if item.name == self.name:
                    lun = item.lun

        # prepare the data disk
        params = self.compute_models.ManagedDiskParameters(id=disk.get('id'), storage_account_type=disk.get('storage_account_type'))
        caching_options = self.compute_models.CachingTypes[self.attach_caching] if self.attach_caching and self.attach_caching != '' else None
        # pylint: disable=missing-kwoa
        data_disk = self.compute_models.DataDisk(lun=lun,
                                                 create_option=self.compute_models.DiskCreateOptionTypes.attach,
                                                 managed_disk=params,
                                                 write_accelerator_enabled=self.write_accelerator_enabled,
                                                 caching=caching_options)
        vm.storage_profile.data_disks.append(data_disk)
        return self._update_vm(resource_group, vm_name, vm)

    def detach(self, resource_group, vm_name, disk):
        vm = self._get_vm(resource_group, vm_name)
        leftovers = [d for d in vm.storage_profile.data_disks if d.name.lower() != disk.get('name').lower()]
        if len(vm.storage_profile.data_disks) == len(leftovers):
            self.fail("No disk with the name '{0}' was found".format(disk.get('name')))
        vm.storage_profile.data_disks = leftovers
        self._update_vm(resource_group, vm_name, vm)

    def _update_vm(self, resource_group, name, params):
        try:
            poller = self.compute_client.virtual_machines.begin_create_or_update(resource_group, name, params)
            self.get_poller_result(poller)
        except Exception as exc:
            if self.managed_by_extended:
                return exc
            else:
                self.fail("Error updating virtual machine {0} - {1}".format(name, str(exc)))

    def _get_vm(self, resource_group, name):
        try:
            return self.compute_client.virtual_machines.get(resource_group, name, expand='instanceview')
        except Exception as exc:
            self.fail("Error getting virtual machine {0} - {1}".format(name, str(exc)))

    def generate_managed_disk_property(self):
        # TODO: Add support for EncryptionSettings, DiskIOPSReadWrite, DiskMBpsReadWrite
        disk_params = {}
        creation_data = {}
        disk_params['location'] = self.location
        disk_params['tags'] = self.tags
        if self.zone:
            disk_params['zones'] = [self.zone]
        if self.storage_account_type:
            storage_account_type = self.disk_models.DiskSku(name=self.storage_account_type)
            disk_params['sku'] = storage_account_type
        disk_params['disk_size_gb'] = self.disk_size_gb

        if self.create_option == 'import':
            creation_data['create_option'] = self.disk_models.DiskCreateOption.import_enum
            creation_data['source_uri'] = self.source_uri
            creation_data['storage_account_id'] = self.storage_account_id
        elif self.create_option == 'copy':
            creation_data['create_option'] = self.disk_models.DiskCreateOption.copy
            creation_data['source_resource_id'] = self.source_resource_id
        elif self.create_option == 'upload':
            creation_data['create_option'] = self.disk_models.DiskCreateOption.upload
            creation_data['upload_size_bytes'] = self.upload_size_bytes
        elif self.create_option == 'fromimage':
            creation_data['create_option'] = self.disk_models.DiskCreateOption.from_image
            if self.image_reference is not None:
                image = self.disk_models.ImageDiskReference(id=self.image_reference.get('id'),
                                                            shared_gallery_image_id=self.image_reference.get('shared_gallery_image_id'),
                                                            community_gallery_image_id=self.image_reference.get('community_gallery_image_id'))
                creation_data['image_reference'] = image
            elif self.gallery_image_reference is not None:
                image = self.disk_models.ImageDiskReference(id=self.gallery_image_reference.get('id'),
                                                            shared_gallery_image_id=self.gallery_image_reference.get('shared_gallery_image_id'),
                                                            community_gallery_image_id=self.gallery_image_reference.get('community_gallery_image_id'))
                creation_data['gallery_image_reference'] = image
            else:
                self.fail("When create_option=fromimage is configured, image_reference or gallery_image_reference must be configured")
        elif self.create_option == 'restore':
            creation_data['create_option'] = self.disk_models.DiskCreateOption.Restore
        elif self.create_option == 'uploadpreparedsecure':
            creation_data['create_option'] = self.disk_models.DiskCreateOption.upload_prepared_secure
            creation_data['upload_size_bytes'] = self.upload_size_bytes
        else:
            creation_data['create_option'] = self.disk_models.DiskCreateOption.empty
        creation_data['logical_sector_size'] = self.logical_sector_size
        creation_data['performance_plus'] = self.performance_plus
        if self.security_profile is not None:
            disk_id = self.security_profile.get('secure_vm_disk_encryption_set_id')
            disk_params['security_profile'] = self.disk_models.DiskSecurityProfile(security_type=self.security_profile.get('security_type'),
                                                                                   secure_vm_disk_encryption_set_id=disk_id)
        if self.os_type:
            disk_params['os_type'] = self.disk_models.OperatingSystemTypes(self.os_type.capitalize())
        else:
            disk_params['os_type'] = None
        if self.max_shares:
            disk_params['max_shares'] = self.max_shares
        if self.disk_m_bps_read_only is not None:
            disk_params['disk_m_bps_read_only'] = self.disk_m_bps_read_only
        if self.disk_m_bps_read_write is not None:
            disk_params['disk_m_bps_read_write'] = self.disk_m_bps_read_write
        if self.disk_iops_read_write is not None:
            disk_params['disk_iops_read_write'] = self.disk_iops_read_write
        if self.disk_iops_read_only is not None:
            disk_params['disk_iops_read_only'] = self.disk_iops_read_only
        if self.tier is not None:
            disk_params['tier'] = self.tier
        if self.network_access_policy is not None:
            disk_params['network_access_policy'] = self.network_access_policy
        if self.public_network_access is not None:
            disk_params['public_network_access'] = self.public_network_access
        if self.disk_access_id is not None:
            disk_params['disk_access_id'] = self.disk_access_id
        disk_params['creation_data'] = creation_data
        return disk_params

    def create_or_update_managed_disk(self, parameter, update_flag):
        try:
            parameter['tags'] = self.tags
            if update_flag:
                poller = self.disk_client.disks.begin_update(self.resource_group,
                                                             self.name,
                                                             parameter)
            else:
                poller = self.disk_client.disks.begin_create_or_update(self.resource_group,
                                                                       self.name,
                                                                       parameter)
            aux = self.get_poller_result(poller)
            return managed_disk_to_dict(aux)
        except Exception as e:
            self.fail("Error creating the managed disk: {0}".format(str(e)))

    # This method accounts for the difference in structure between the
    # Azure retrieved disk and the parameters for the new disk to be created.
    def is_different(self, found_disk, new_disk):
        resp = False
        if new_disk.get('disk_size_gb'):
            if not found_disk['disk_size_gb'] == new_disk['disk_size_gb']:
                resp = True
        if new_disk.get('os_type'):
            if found_disk['os_type'] is None or not self.disk_models.OperatingSystemTypes(found_disk['os_type'].capitalize()) == new_disk['os_type']:
                resp = True
        if new_disk.get('sku'):
            if not found_disk['storage_account_type'] == new_disk['sku'].name:
                resp = True
        # Check how to implement tags
        update_tags, self.tags = self.update_tags(found_disk['tags'])
        if update_tags:
            resp = True
        if self.zone is not None:
            if not found_disk['zone'] == self.zone:
                resp = True
        if self.max_shares is not None:
            if not found_disk['max_shares'] == self.max_shares:
                resp = True
        if self.disk_iops_read_write is not None and found_disk['disk_iops_read_write'] != self.disk_iops_read_write:
            resp = True
        if self.disk_m_bps_read_write is not None and found_disk['disk_m_bps_read_write'] != self.disk_m_bps_read_write:
            resp = True
        if self.disk_iops_read_only is not None and found_disk['disk_iops_read_only'] != self.disk_iops_read_only:
            resp = True
        if self.disk_m_bps_read_only is not None and found_disk['disk_m_bps_read_only'] != self.disk_m_bps_read_only:
            resp = True
        if self.tier is not None:
            if not found_disk['tier'] == self.tier:
                resp = True
        if self.network_access_policy is not None and found_disk['network_access_policy'] != self.network_access_policy:
            resp = True
        if self.public_network_access is not None and found_disk['public_network_access'] != self.public_network_access:
            resp = True
        if self.disk_access_id is not None:
            if found_disk['disk_access_id'] is not None:
                if found_disk['disk_access_id'].lower() != self.disk_access_id.lower():
                    resp = True
            else:
                resp = True
        return resp

    def delete_managed_disk(self):
        try:
            poller = self.disk_client.disks.begin_delete(self.resource_group,
                                                         self.name)
            return self.get_poller_result(poller)
        except Exception as e:
            self.fail("Error deleting the managed disk: {0}".format(str(e)))

    def get_managed_disk(self):
        try:
            resp = self.disk_client.disks.get(
                self.resource_group,
                self.name)
            return managed_disk_to_dict(resp)
        except ResourceNotFoundError:
            self.log('Did not find managed disk')

    def is_attach_caching_option_different(self, vm_name, disk):
        resp = False
        if vm_name:
            vm = self._get_vm(self.resource_group, vm_name)
            correspondence = next((d for d in vm.storage_profile.data_disks if d.name.lower() == disk.get('name').lower()), None)
            caching_options = self.compute_models.CachingTypes[self.attach_caching] if self.attach_caching and self.attach_caching != '' else None
            if correspondence and correspondence.caching != caching_options:
                resp = True
                if correspondence.caching == 'None' and (self.attach_caching == '' or self.attach_caching is None):
                    resp = False
        return resp


def main():
    """Main execution"""
    AzureRMManagedDisk()


if __name__ == '__main__':
    main()

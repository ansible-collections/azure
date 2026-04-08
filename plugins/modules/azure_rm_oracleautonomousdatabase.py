#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_oracle_autonomous_database
version_added: "3.17.0"
short_description: Manage Oracle Autonomous Database instance
description:
    - Create, update and delete instance of Oracle Autonomous Database on Azure.
    - This module uses the Oracle Database@Azure service, which allows running Oracle Autonomous Database natively in Azure data centers.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Oracle Autonomous Database resource.
        required: true
        type: str
    location:
        description:
            - The Azure region where the resource should be created.
            - If not set, location from the resource group will be used as default.
        type: str
    display_name:
        description:
            - The user-friendly name for the Autonomous Database.
        type: str
    admin_password:
        description:
            - Admin password for the Autonomous Database.
            - Required when creating a new Autonomous Database.
        type: str
    db_workload:
        description:
            - The Autonomous Database workload type.
        type: str
        choices:
            - OLTP
            - DW
            - AJD
            - APEX
    compute_model:
        description:
            - The compute model of the Autonomous Database.
        type: str
        choices:
            - ECPU
            - OCPU
    compute_count:
        description:
            - The compute amount (CPUs) available to the database.
        type: float
    cpu_core_count:
        description:
            - The number of CPU cores to be made available to the database.
        type: int
    data_storage_size_in_tbs:
        description:
            - The quantity of data in the database, in terabytes.
        type: int
    data_storage_size_in_gbs:
        description:
            - The size, in gigabytes, of the data volume that will be created and attached to the database.
        type: int
    is_auto_scaling_enabled:
        description:
            - Indicates if auto scaling is enabled for the Autonomous Database CPU core count.
        type: bool
    is_auto_scaling_for_storage_enabled:
        description:
            - Indicates if auto scaling is enabled for the Autonomous Database storage.
        type: bool
    is_mtls_connection_required:
        description:
            - Specifies if the Autonomous Database requires mTLS connections.
        type: bool
    character_set:
        description:
            - The character set for the autonomous database.
            - Only applicable during creation.
        type: str
    ncharacter_set:
        description:
            - The national character set for the Autonomous Database.
            - Only applicable during creation.
        type: str
    db_version:
        description:
            - A valid Oracle Database version for Autonomous Database.
            - Only applicable during creation.
        type: str
    license_model:
        description:
            - The Oracle license model that applies to the Oracle Autonomous Database.
        type: str
        choices:
            - LicenseIncluded
            - BringYourOwnLicense
    database_edition:
        description:
            - The Oracle Database Edition that applies to the Autonomous databases.
        type: str
        choices:
            - StandardEdition
            - EnterpriseEdition
    subnet_id:
        description:
            - Client subnet ID.
            - Only applicable during creation.
        type: str
    vnet_id:
        description:
            - VNET ID for network connectivity.
            - Only applicable during creation.
        type: str
    private_endpoint_ip:
        description:
            - The private endpoint IP address for the resource.
            - Only applicable during creation.
        type: str
    private_endpoint_label:
        description:
            - The resource's private endpoint label.
            - Only applicable during creation.
        type: str
    autonomous_database_id:
        description:
            - Autonomous Database ID (OCI OCID).
            - Only applicable during creation.
        type: str
    is_local_data_guard_enabled:
        description:
            - Indicates whether the Autonomous Database has local (in-region) Data Guard enabled.
        type: bool
    is_preview_version_with_service_terms_accepted:
        description:
            - Specifies if the Autonomous Database preview version is being provisioned.
            - Only applicable during creation.
        type: bool
    backup_retention_period_in_days:
        description:
            - Retention period, in days, for long-term backups.
        type: int
    whitelisted_ips:
        description:
            - The client IP access control list (ACL).
            - An array of CIDR notations and/or IP addresses.
        type: list
        elements: str
    customer_contacts:
        description:
            - Customer contact email addresses for Oracle notifications.
            - Each item should have an C(email) key.
        type: list
        elements: dict
        suboptions:
            email:
                description:
                    - The email address for Oracle notifications.
                required: true
                type: str
    scheduled_operations:
        description:
            - The list of scheduled operations.
        type: list
        elements: dict
        suboptions:
            day_of_week:
                description:
                    - Day of week.
                required: true
                type: str
                choices:
                    - Monday
                    - Tuesday
                    - Wednesday
                    - Thursday
                    - Friday
                    - Saturday
                    - Sunday
            scheduled_start_time:
                description:
                    - Auto start time in ISO-8601 format HH:mm.
                type: str
            scheduled_stop_time:
                description:
                    - Auto stop time in ISO-8601 format HH:mm.
                type: str
    autonomous_maintenance_schedule_type:
        description:
            - The maintenance schedule type of the Autonomous Database Serverless.
        type: str
        choices:
            - Early
            - Regular
    open_mode:
        description:
            - Indicates the Autonomous Database mode.
            - Only applicable during update.
        type: str
        choices:
            - ReadOnly
            - ReadWrite
    permission_level:
        description:
            - The Autonomous Database permission level.
            - Only applicable during update.
        type: str
        choices:
            - Restricted
            - Unrestricted
    role:
        description:
            - The Data Guard role of the Autonomous Database.
            - Only applicable during update.
        type: str
        choices:
            - Primary
            - Standby
            - DisabledStandby
            - BackupCopy
            - SnapshotStandby
    peer_db_id:
        description:
            - The Azure resource ID of the Disaster Recovery peer database.
            - Only applicable during update.
        type: str
    local_adg_auto_failover_max_data_loss_limit:
        description:
            - Maximum data loss limit in seconds for Local Autonomous Data Guard auto failover.
            - Only applicable during update.
        type: int
    long_term_backup_schedule:
        description:
            - Details for the long-term backup schedule.
            - Only applicable during update.
        type: dict
        suboptions:
            repeat_cadence:
                description:
                    - The frequency of the long-term backup schedule.
                type: str
                choices:
                    - OneTime
                    - Weekly
                    - Monthly
                    - Yearly
            time_of_backup:
                description:
                    - The timestamp for the long-term backup schedule (ISO 8601 format).
                type: str
            retention_period_in_days:
                description:
                    - Retention period, in days, for backups.
                type: int
            is_disabled:
                description:
                    - Indicates if the long-term backup schedule should be deleted.
                type: bool
    state:
        description:
            - Assert the state of the Oracle Autonomous Database.
            - Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create an Oracle Autonomous Database
  azure.azcollection.azure_rm_oracle_autonomous_database:
    resource_group: myResourceGroup
    name: myAutonomousDb
    location: eastus
    display_name: myAutonomousDb
    db_workload: OLTP
    compute_model: ECPU
    compute_count: 2
    data_storage_size_in_tbs: 1
    is_auto_scaling_enabled: true
    is_auto_scaling_for_storage_enabled: true
    is_mtls_connection_required: true
    admin_password: "{{ admin_password }}"
    character_set: AL32UTF8
    ncharacter_set: AL16UTF16
    db_version: 19c
    license_model: LicenseIncluded
    subnet_id: "{{ subnet_id }}"
    vnet_id: "{{ vnet_id }}"
    tags:
      environment: dev

- name: Update an Oracle Autonomous Database
  azure.azcollection.azure_rm_oracle_autonomous_database:
    resource_group: myResourceGroup
    name: myAutonomousDb
    compute_count: 4
    data_storage_size_in_tbs: 2
    is_auto_scaling_enabled: false
    tags:
      environment: staging

- name: Delete an Oracle Autonomous Database
  azure.azcollection.azure_rm_oracle_autonomous_database:
    resource_group: myResourceGroup
    name: myAutonomousDb
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Oracle Autonomous Database.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxx/resourceGroups/myRG/providers/Oracle.Database/autonomousDatabases/myDB"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myAutonomousDb
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {"environment": "dev"}
        display_name:
            description:
                - The user-friendly name for the Autonomous Database.
            returned: always
            type: str
            sample: myAutonomousDb
        db_workload:
            description:
                - The Autonomous Database workload type.
            returned: always
            type: str
            sample: OLTP
        compute_model:
            description:
                - The compute model of the Autonomous Database.
            returned: always
            type: str
            sample: ECPU
        compute_count:
            description:
                - The compute amount (CPUs) available to the database.
            returned: always
            type: float
            sample: 2.0
        data_storage_size_in_tbs:
            description:
                - The quantity of data in the database, in terabytes.
            returned: always
            type: int
            sample: 1
        character_set:
            description:
                - The character set for the autonomous database.
            returned: always
            type: str
            sample: AL32UTF8
        ncharacter_set:
            description:
                - The national character set for the Autonomous Database.
            returned: always
            type: str
            sample: AL16UTF16
        db_version:
            description:
                - A valid Oracle Database version for Autonomous Database.
            returned: always
            type: str
            sample: 19c
        license_model:
            description:
                - The Oracle license model.
            returned: always
            type: str
            sample: LicenseIncluded
        lifecycle_state:
            description:
                - The current lifecycle state of the Autonomous Database.
            returned: always
            type: str
            sample: Available
        provisioning_state:
            description:
                - Azure resource provisioning state.
            returned: always
            type: str
            sample: Succeeded
        is_auto_scaling_enabled:
            description:
                - Whether auto scaling is enabled for CPU.
            returned: always
            type: bool
            sample: true
        is_auto_scaling_for_storage_enabled:
            description:
                - Whether auto scaling is enabled for storage.
            returned: always
            type: bool
            sample: true
        is_mtls_connection_required:
            description:
                - Whether mTLS connections are required.
            returned: always
            type: bool
            sample: true
        subnet_id:
            description:
                - Client subnet ID.
            returned: always
            type: str
        vnet_id:
            description:
                - VNET ID for network connectivity.
            returned: always
            type: str
        connection_strings:
            description:
                - Connection strings for the Autonomous Database.
            returned: always
            type: dict
        connection_urls:
            description:
                - Connection URLs for APEX and SQL Developer Web.
            returned: always
            type: dict
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
    from azure.mgmt.oracledatabase.models import (
        AutonomousDatabase,
        AutonomousDatabaseProperties,
        AutonomousDatabaseUpdate,
        AutonomousDatabaseUpdateProperties,
    )
except ImportError:
    # This is handled in azure_rm_common
    pass


customer_contact_spec = dict(
    email=dict(type='str', required=True)
)

scheduled_operation_spec = dict(
    day_of_week=dict(
        type='str',
        required=True,
        choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ),
    scheduled_start_time=dict(type='str'),
    scheduled_stop_time=dict(type='str')
)

long_term_backup_schedule_spec = dict(
    repeat_cadence=dict(type='str', choices=['OneTime', 'Weekly', 'Monthly', 'Yearly']),
    time_of_backup=dict(type='str'),
    retention_period_in_days=dict(type='int'),
    is_disabled=dict(type='bool')
)


class Actions:
    NoAction, Create, Update, Delete = range(4)


# Properties that can be set at create time only
CREATE_ONLY_PARAMS = [
    'character_set', 'ncharacter_set', 'compute_model', 'db_workload',
    'db_version', 'subnet_id', 'vnet_id', 'private_endpoint_ip',
    'private_endpoint_label', 'autonomous_database_id',
    'is_preview_version_with_service_terms_accepted',
]

# Properties that can be set at both create and update time
CREATE_UPDATE_PARAMS = [
    'admin_password', 'display_name', 'compute_count', 'cpu_core_count',
    'data_storage_size_in_tbs', 'data_storage_size_in_gbs',
    'is_auto_scaling_enabled', 'is_auto_scaling_for_storage_enabled',
    'is_mtls_connection_required', 'is_local_data_guard_enabled',
    'license_model', 'database_edition', 'backup_retention_period_in_days',
    'whitelisted_ips', 'customer_contacts', 'scheduled_operations',
    'autonomous_maintenance_schedule_type',
]

# Properties that can only be set at update time
UPDATE_ONLY_PARAMS = [
    'open_mode', 'permission_level', 'role', 'peer_db_id',
    'local_adg_auto_failover_max_data_loss_limit', 'long_term_backup_schedule',
]

# Mapping: module param name -> SDK property name (only where they differ)
PARAM_TO_SDK = {
    'scheduled_operations': 'scheduled_operations_list',
}


class AzureRMOracleAutonomousDatabase(AzureRMModuleBase):
    """Configuration class for an Azure RM Oracle Autonomous Database resource"""

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
            location=dict(
                type='str'
            ),
            display_name=dict(
                type='str'
            ),
            admin_password=dict(
                type='str',
                no_log=True
            ),
            db_workload=dict(
                type='str',
                choices=['OLTP', 'DW', 'AJD', 'APEX']
            ),
            compute_model=dict(
                type='str',
                choices=['ECPU', 'OCPU']
            ),
            compute_count=dict(
                type='float'
            ),
            cpu_core_count=dict(
                type='int'
            ),
            data_storage_size_in_tbs=dict(
                type='int'
            ),
            data_storage_size_in_gbs=dict(
                type='int'
            ),
            is_auto_scaling_enabled=dict(
                type='bool'
            ),
            is_auto_scaling_for_storage_enabled=dict(
                type='bool'
            ),
            is_mtls_connection_required=dict(
                type='bool'
            ),
            character_set=dict(
                type='str'
            ),
            ncharacter_set=dict(
                type='str'
            ),
            db_version=dict(
                type='str'
            ),
            license_model=dict(
                type='str',
                choices=['LicenseIncluded', 'BringYourOwnLicense']
            ),
            database_edition=dict(
                type='str',
                choices=['StandardEdition', 'EnterpriseEdition']
            ),
            subnet_id=dict(
                type='str'
            ),
            vnet_id=dict(
                type='str'
            ),
            private_endpoint_ip=dict(
                type='str'
            ),
            private_endpoint_label=dict(
                type='str'
            ),
            autonomous_database_id=dict(
                type='str'
            ),
            is_local_data_guard_enabled=dict(
                type='bool'
            ),
            is_preview_version_with_service_terms_accepted=dict(
                type='bool'
            ),
            backup_retention_period_in_days=dict(
                type='int'
            ),
            whitelisted_ips=dict(
                type='list',
                elements='str'
            ),
            customer_contacts=dict(
                type='list',
                elements='dict',
                options=customer_contact_spec
            ),
            scheduled_operations=dict(
                type='list',
                elements='dict',
                options=scheduled_operation_spec
            ),
            autonomous_maintenance_schedule_type=dict(
                type='str',
                choices=['Early', 'Regular']
            ),
            open_mode=dict(
                type='str',
                choices=['ReadOnly', 'ReadWrite']
            ),
            permission_level=dict(
                type='str',
                choices=['Restricted', 'Unrestricted']
            ),
            role=dict(
                type='str',
                choices=['Primary', 'Standby', 'DisabledStandby', 'BackupCopy', 'SnapshotStandby']
            ),
            peer_db_id=dict(
                type='str'
            ),
            local_adg_auto_failover_max_data_loss_limit=dict(
                type='int'
            ),
            long_term_backup_schedule=dict(
                type='dict',
                options=long_term_backup_schedule_spec
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.tags = None
        self.state = None

        self.create_properties = dict()
        self.update_properties = dict()

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        super(AzureRMOracleAutonomousDatabase, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True
        )

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                sdk_key = PARAM_TO_SDK.get(key, key)
                if key in CREATE_ONLY_PARAMS:
                    self.create_properties[sdk_key] = kwargs[key]
                elif key in CREATE_UPDATE_PARAMS:
                    self.create_properties[sdk_key] = kwargs[key]
                    self.update_properties[sdk_key] = kwargs[key]
                elif key in UPDATE_ONLY_PARAMS:
                    self.update_properties[sdk_key] = kwargs[key]

        old_response = None
        changed = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        old_response = self.get_autonomous_database()

        if not old_response:
            if self.state == 'absent':
                self.log("Oracle Autonomous Database does not exist - nothing to delete")
            else:
                changed = True
                self.to_do = Actions.Create
        else:
            self.log("Oracle Autonomous Database already exists")
            if self.state == 'absent':
                changed = True
                self.to_do = Actions.Delete
            else:
                update_tags, self.update_properties['tags'] = self.update_tags(old_response.get('tags'))
                if update_tags:
                    changed = True
                    self.to_do = Actions.Update

                if self._needs_update(old_response):
                    changed = True
                    self.to_do = Actions.Update

                # Remove tags from update_properties if no tag changes needed
                if not update_tags and 'tags' in self.update_properties:
                    del self.update_properties['tags']

        if self.to_do == Actions.Create:
            self.log("Need to create Oracle Autonomous Database")
            if not self.check_mode:
                response = self.create_autonomous_database()
                self.results['state'] = response
            self.results['changed'] = True
        elif self.to_do == Actions.Update:
            self.log("Need to update Oracle Autonomous Database")
            if not self.check_mode:
                response = self.update_autonomous_database()
                self.results['state'] = response
            self.results['changed'] = True
        elif self.to_do == Actions.Delete:
            self.log("Need to delete Oracle Autonomous Database")
            if not self.check_mode:
                self.delete_autonomous_database()
            self.results['changed'] = True
        else:
            self.results['changed'] = False
            self.results['state'] = old_response

        return self.results

    def _needs_update(self, old_response):
        """Check if any updatable properties differ from current state."""
        props = old_response.get('properties', {})
        for param_key in CREATE_UPDATE_PARAMS + UPDATE_ONLY_PARAMS:
            sdk_key = PARAM_TO_SDK.get(param_key, param_key)
            if sdk_key in self.update_properties and sdk_key != 'admin_password':
                new_val = self.update_properties[sdk_key]
                old_val = props.get(sdk_key)
                if new_val is not None and old_val is not None and new_val != old_val:
                    return True
        return False

    def create_autonomous_database(self):
        """Creates the Oracle Autonomous Database."""
        self.log("Creating Oracle Autonomous Database {0}".format(self.name))
        try:
            create_props = dict(data_base_type='Regular')
            create_props.update(self.create_properties)
            properties = AutonomousDatabaseProperties(**create_props)

            resource = AutonomousDatabase(
                location=self.location,
                tags=self.tags,
                properties=properties
            )
            response = self.oracle_database_client.autonomous_databases.begin_create_or_update(
                resource_group_name=self.resource_group,
                autonomousdatabasename=self.name,
                resource=resource
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating Oracle Autonomous Database {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def update_autonomous_database(self):
        """Updates the Oracle Autonomous Database."""
        self.log("Updating Oracle Autonomous Database {0}".format(self.name))
        try:
            update_tags = self.update_properties.pop('tags', None)
            update_props = AutonomousDatabaseUpdateProperties(**self.update_properties) if self.update_properties else None

            update_payload = AutonomousDatabaseUpdate(
                tags=update_tags,
                properties=update_props
            )
            response = self.oracle_database_client.autonomous_databases.begin_update(
                resource_group_name=self.resource_group,
                autonomousdatabasename=self.name,
                properties=update_payload
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error updating Oracle Autonomous Database {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def delete_autonomous_database(self):
        """Deletes the Oracle Autonomous Database."""
        self.log("Deleting Oracle Autonomous Database {0}".format(self.name))
        try:
            response = self.oracle_database_client.autonomous_databases.begin_delete(
                resource_group_name=self.resource_group,
                autonomousdatabasename=self.name
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting Oracle Autonomous Database {0}: {1}".format(self.name, str(exc)))
        return True

    def get_autonomous_database(self):
        """Gets the properties of the specified Oracle Autonomous Database."""
        self.log("Checking if Oracle Autonomous Database {0} exists".format(self.name))
        try:
            response = self.oracle_database_client.autonomous_databases.get(
                resource_group_name=self.resource_group,
                autonomousdatabasename=self.name
            )
            self.log("Response : {0}".format(response))
            self.log("Oracle Autonomous Database {0} found".format(response.name))
            return self.format_item(response)
        except ResourceNotFoundError:
            self.log('Oracle Autonomous Database {0} not found'.format(self.name))
        return False

    def format_item(self, item):
        """Format the SDK response into a module return dictionary."""
        props = item.properties if item.properties else {}
        result = dict(
            id=item.id,
            name=item.name,
            type=item.type,
            location=item.location,
            tags=item.tags,
            resource_group=self.parse_resource_to_dict(item.id).get('resource_group'),
            properties=dict(
                display_name=getattr(props, 'display_name', None),
                db_workload=getattr(props, 'db_workload', None),
                compute_model=getattr(props, 'compute_model', None),
                compute_count=getattr(props, 'compute_count', None),
                cpu_core_count=getattr(props, 'cpu_core_count', None),
                data_storage_size_in_tbs=getattr(props, 'data_storage_size_in_tbs', None),
                data_storage_size_in_gbs=getattr(props, 'data_storage_size_in_gbs', None),
                character_set=getattr(props, 'character_set', None),
                ncharacter_set=getattr(props, 'ncharacter_set', None),
                db_version=getattr(props, 'db_version', None),
                license_model=getattr(props, 'license_model', None),
                database_edition=getattr(props, 'database_edition', None),
                lifecycle_state=getattr(props, 'lifecycle_state', None),
                lifecycle_details=getattr(props, 'lifecycle_details', None),
                provisioning_state=getattr(props, 'provisioning_state', None),
                is_auto_scaling_enabled=getattr(props, 'is_auto_scaling_enabled', None),
                is_auto_scaling_for_storage_enabled=getattr(props, 'is_auto_scaling_for_storage_enabled', None),
                is_mtls_connection_required=getattr(props, 'is_mtls_connection_required', None),
                is_local_data_guard_enabled=getattr(props, 'is_local_data_guard_enabled', None),
                is_remote_data_guard_enabled=getattr(props, 'is_remote_data_guard_enabled', None),
                subnet_id=getattr(props, 'subnet_id', None),
                vnet_id=getattr(props, 'vnet_id', None),
                private_endpoint=getattr(props, 'private_endpoint', None),
                private_endpoint_ip=getattr(props, 'private_endpoint_ip', None),
                private_endpoint_label=getattr(props, 'private_endpoint_label', None),
                autonomous_database_id=getattr(props, 'autonomous_database_id', None),
                backup_retention_period_in_days=getattr(props, 'backup_retention_period_in_days', None),
                open_mode=getattr(props, 'open_mode', None),
                permission_level=getattr(props, 'permission_level', None),
                role=getattr(props, 'role', None),
                ocid=getattr(props, 'ocid', None),
                oci_url=getattr(props, 'oci_url', None),
                connection_strings=self._format_connection_strings(props),
                connection_urls=self._format_connection_urls(props),
                time_created=str(getattr(props, 'time_created', None)) if getattr(props, 'time_created', None) else None,
            ),
        )
        return result

    def _format_connection_strings(self, props):
        """Format connection strings from properties."""
        cs = getattr(props, 'connection_strings', None)
        if cs is None:
            return None
        return dict(
            all_connection_strings=getattr(cs, 'all_connection_strings', None),
            dedicated=getattr(cs, 'dedicated', None),
            high=getattr(cs, 'high', None),
            low=getattr(cs, 'low', None),
            medium=getattr(cs, 'medium', None),
        )

    def _format_connection_urls(self, props):
        """Format connection URLs from properties."""
        cu = getattr(props, 'connection_urls', None)
        if cu is None:
            return None
        return dict(
            apex_url=getattr(cu, 'apex_url', None),
            database_transforms_url=getattr(cu, 'database_transforms_url', None),
            graph_studio_url=getattr(cu, 'graph_studio_url', None),
            machine_learning_notebook_url=getattr(cu, 'machine_learning_notebook_url', None),
            mongo_db_url=getattr(cu, 'mongo_db_url', None),
            ords_url=getattr(cu, 'ords_url', None),
            sql_dev_web_url=getattr(cu, 'sql_dev_web_url', None),
        )


def main():
    """Main execution"""
    AzureRMOracleAutonomousDatabase()


if __name__ == '__main__':
    main()

# Change Log

## v1.16.0 (2023-5-31)

### NEW MODULES
  - azure_rm_vmssnetworkinterface_info: Add VMSS networkinterface to get VMSS network interface info ([#1125](https://github.com/ansible-collections/azure/pull/1125))

### FEATURE ENHANCEMENT
  - azure_rm_managementgroup: Upgrade azure-mgmt-managements to 1.0.0 ([#1117](https://github.com/ansible-collections/azure/pull/1117))
  - azure_rm_managementgroup_info: Upgrade azure-mgmt-managements to 1.0.0 ([#1117](https://github.com/ansible-collections/azure/pull/1117))
  - azure_rm_servicebus: Support tags to azure_rm_servicebus.py ([#1114](https://github.com/ansible-collections/azure/pull/1114))
  - azure_rm_servicebusqueue: Add `max_message_size_in_kb` to azure_rm_servicebusqueue ([#1092](https://github.com/ansible-collections/azure/pull/1092))
  - azure_rm_servicebustopic: Add `max_message_size_in_kb` to azure_rm_servicebusqueue ([#1092](https://github.com/ansible-collections/azure/pull/1092))
  - plugins/doc_fragments/azure_rm: Update the description of `include_vm_resource_groups` ([#1077](https://github.com/ansible-collections/azure/pull/1077))
  - azure_rm_galleryimageversion: Fix append tags for azure_rm_galleryimageversion ([#1100](https://github.com/ansible-collections/azure/pull/1100))
  - azure_rm_lock: Add support for `notes` ([#1097](https://github.com/ansible-collections/azure/pull/1097))
  - azure_rm_devtestlab: Upgrade azure-mgmt-devtestlabs to 9.0.0 ([#958](https://github.com/ansible-collections/azure/pull/958))
  - azure_rm_virtualmachine:
    - Upgrade azure-mgmt-marketplaceordering to 1.1.0 ([#940](https://github.com/ansible-collections/azure/pull/940))
    - Add support for new `managed_disk_type` type `UltraSSD_LRS` ([#1136](https://github.com/ansible-collections/azure/pull/1136))
  - azure_rm_virtualmachinescaleset:
    - Upgrade azure-mgmt-marketplaceordering to 1.1.0 ([#940](https://github.com/ansible-collections/azure/pull/940))
    - Add support for new `managed_disk_type` type `UltraSSD_LRS` ([#1136](https://github.com/ansible-collections/azure/pull/1136))
  - azure_rm_virtualnetworkpeering_info: Add support for `peering_sync_level` ([#1085](https://github.com/ansible-collections/azure/pull/1085))
  - azure_rm_containerinstance: Add support for `subnet_ids` ([#1090](https://github.com/ansible-collections/azure/pull/1090))
  - azure_rm_containerinstance_info: Add support for `subnet_ids` ([#1090](https://github.com/ansible-collections/azure/pull/1090))
  - azure_rm_storageaccount: Add support for failover ([#1141](https://github.com/ansible-collections/azure/pull/1141))


### BUG FIXING
  - azure_rm_loganalyticsworkspace: Fix test cases ([#1129](https://github.com/ansible-collections/azure/pull/1129))
  - azure_rm_virtualmachine_info: Ensure `display_status` is initialised before it is used ([#1123](https://github.com/ansible-collections/azure/pull/1123))
  - azure_rm_webapp:
    - Add support for creating with `python` ([#1128](https://github.com/ansible-collections/azure/pull/1128))
    - Fix azure_rm_webapp fails when state is `absent` ([#1079](https://github.com/ansible-collections/azure/pull/1079))
  - azure_rm_virtualmachine: Add option to choose whether or not to create a network security group ([#1056](https://github.com/ansible-collections/azure/pull/1056))
  - azure_rm_networkinterace: Fix idempotent failure ([#1037](https://github.com/ansible-collections/azure/pull/1037))
  - azure_rm_virtualnetwork: Update documentation of `azure_rm_virtualnetwork` to reflect that the `dns_servers` limit on length is no longer 2 ([#1082](https://github.com/ansible-collections/azure/pull/1082))
  - azure_rm_rediscache: Remove references to Redis 4 and support upgrading to Redis 6 ([#1132](https://github.com/ansible-collections/azure/pull/1132))
  - azure_rm_virtualnetwork_info: Update documentation in azure_rm_virtualnetwork_info and include a small change to match other patterns for getting network info. ([#1087](https://github.com/ansible-collections/azure/pull/1087))
  - azure_rm_snapshot: Add supprot for `incremental` ([#1135](https://github.com/ansible-collections/azure/pull/1135))
  - azure_rm_appgateway: Fix `version_added` in module document ([#1139](https://github.com/ansible-collections/azure/pull/1139))
  - azure_rm_*: Documentation fixes ([#1151](https://github.com/ansible-collections/azure/pull/1151))
  - azure_rm_devtestlab/aliases: Disable `azure_rm_devtestlab` test ([#1144](https://github.com/ansible-collections/azure/pull/1144))
  - inventory/azure_rm: **inventory** - Ignore response status code other than 200 ([#1166](https://github.com/ansible-collections/azure/pull/1166))
  - azure_rm_keyvaultkey: Use creds in module args when auth_source is auto ([#1010](https://github.com/ansible-collections/azure/pull/1010))
  - azure_rm_keyvaultkey_info: Use creds in module args when `auth_source` is `auto` ([#1010](https://github.com/ansible-collections/azure/pull/1010))
  - azure_rm_keyvaultsecret: Use creds in module args when `auth_source` is `auto` ([#1010](https://github.com/ansible-collections/azure/pull/1010))
  - azure_rm_keyvaultsecret_info: Use creds in module args when `auth_source` is `auto` ([#1010](https://github.com/ansible-collections/azure/pull/1010))
  - azure_rm_routetable: Fix route table updates delete all existing routes in the route table ([#1146](https://github.com/ansible-collections/azure/pull/1146))
  - azure_rm_cdnendpoint: Fix failed to clear CND endpoint ([#1154](https://github.com/ansible-collections/azure/pull/1154))
  - azure_rm_resource_info: Add support for `method` ([#1158](https://github.com/ansible-collections/azure/pull/1158))
  - azure_keyvault_secret: Add support for azure cli credential ([#1161](https://github.com/ansible-collections/azure/pull/1161))
  - requirements-azure.txt：Update dependency to resolve upstream issue ([#1169](https://github.com/ansible-collections/azure/pull/1169))

## v1.15.0 (2023-03-15)

### NEW MODULES
  - azure_rm_multiplemanageddisks: New module to create/update/delete/attach multiple disks ([#936](https://github.com/ansible-collections/azure/pull/936))
  - azure_rm_sqlelasticpool: Add azure_rm_sqlelasticpool.py to create Elastic Pool ([#1027](https://github.com/ansible-collections/azure/pull/1027))
  - azure_rm_sqlelasticpool_info: Add azure_rm_sqlelasticpool_info.py to get Elastic Pool info ([#1027](https://github.com/ansible-collections/azure/pull/1027))
  - azure_rm_sqlmanagedinstance: Add azure_rm_sqlmanagedinstance module ([#1039](https://github.com/ansible-collections/azure/pull/1039))
  - azure_rm_sqlmanagedinstance_info: Add azure_rm_sqlmanagedinstance module ([#1039](https://github.com/ansible-collections/azure/pull/1039))

### FEATURE ENHANCEMENT
  - requirements-azure.txt: Upgrade azure-mgmt-apimanagement to 3.0.0 ([#943](https://github.com/ansible-collections/azure/pull/943))
  - azure_rm_openshiftmanagedcluster: Add new choices to vm_size in azure_rm_openshiftmanagedcluster.py ([#979](https://github.com/ansible-collections/azure/pull/979))
  - azure_rm_appgateway: Add new parameters to azure_rm_appgateway ([#990](https://github.com/ansible-collections/azure/pull/990))
  - azure_rm.py: Add compose support in inventory/azure_rm.py ([#1065](https://github.com/ansible-collections/azure/pull/1065))
  - azure_rm_backupazurevm: add option for recovery point expiry time ([#1057](https://github.com/ansible-collections/azure/pull/1057))
  - runtime.yml: Keep action_groups and modules list consistent #([1042](https://github.com/ansible-collections/azure/pull/1042))
  - azure_rm_virtualnetworkpeering: Add synchronizing of VNet peering when sync level is LocalNotInSync ([#1025](https://github.com/ansible-collections/azure/pull/1025))
  - azure_rm_deployment: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_deployment_info: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_lock: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_subscription: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_subscription_info: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_resourcegroup: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_resourcegroup_info: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_virtualmachine: Upgrade azure-mgmt-resource to 21.1.0 ([#960](https://github.com/ansible-collections/azure/pull/960))
  - azure_rm_storageblob: Make batch_upload honour `force` attribute in azure_rm_storageblob ([#1018](https://github.com/ansible-collections/azure/pull/1018))
  - azure_rm_virtualnetwork: Add `flow_timeout_in_minutes` to azure_rm_virtualnetwork ([#1036](https://github.com/ansible-collections/azure/pull/1036))
  - azure_rm_virtualnetwork_info: Add `flow_timeout_in_minutes` to azure_rm_virtualnetwork ([#1036](https://github.com/ansible-collections/azure/pull/1036))
  - requirements-azure.txt: Bump cryptography from 38.0.1 to 38.0.3 ([#1035](https://github.com/ansible-collections/azure/pull/1035))
  - azure_rm_galleryimageversion_info: Read paginated response for gallery image versions ([#1073](https://github.com/ansible-collections/azure/pull/1073))
  - azure_rm_virtualmachine: Add `security_profile` options to azure_rm_virtualmachine ([#1033](https://github.com/ansible-collections/azure/pull/1033))
  - azure_rm_virtualmachine_info: Add `security_profile` options to azure_rm_virtualmachine ([#1033](https://github.com/ansible-collections/azure/pull/1033))

### BUG FIXING
  - azure_rm_deployment: Fix Ansible azure_rm_deployment module returns error but deployment in Azure was successful ([#986](https://github.com/ansible-collections/azure/pull/986))
  - azure_rm.py: support for environment variable ANSIBLE_AZURE_VM_RESOURCE_GROUPS ([#975](https://github.com/ansible-collections/azure/pull/975))
  - azure_rm_common.py: Ensure trailing slash on base_url ([#984](https://github.com/ansible-collections/azure/pull/984))
  - azure_rm_virtualmachine: Correct spelling errors in documents ([#1012](https://github.com/ansible-collections/azure/pull/1012))
  - azure_rm_storageblob: Format the md5 value returned by azure_rm_storageblob.py ([#1038](https://github.com/ansible-collections/azure/pull/1038))
  - aure_rm_loadbalancer: The zone default value is None if not configured ([#1060](https://github.com/ansible-collections/azure/pull/1060))
  - README.md: Correct spelling errors in documents ([#1059](https://github.com/ansible-collections/azure/pull/1059))
  - azure_rm_securitygroup: Fixed idempotent error due to protocol ([#1064](https://github.com/ansible-collections/azure/pull/1064))
  - azure_rm_roleassignment: Correct document case's config ([#1053](https://github.com/ansible-collections/azure/pull/1053))
  - azure_rm_privatednsrecordset: Change the defined long type to int ([#1058](https://github.com/ansible-collections/azure/pull/1058))
  - azure_rm_keyvault: Add the required restriction to the parameter ([#1054](https://github.com/ansible-collections/azure/pull/1054))
  - azure_rm_dnsrecordset: Change the defined long type to int ([#1052](https://github.com/ansible-collections/azure/pull/1052))
  - azure_rm_common.py: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_backuppolicy: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_manageddisk: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_multiplemanageddisks: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_sqlmanagedinstance: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_servicebussaspolicy: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_virtualmachine: Add Ansible 2.14 and python 3.11 to CI ([#1074](https://github.com/ansible-collections/azure/pull/1074))
  - azure_rm_securitygroup: azure_rm_securitygroup is changed without actual changes when only capitalization differs ([#1096](https://github.com/ansible-collections/azure/pull/1096))

## v1.14.0 (2022-10-31)

### NEW MODULES
  - azure_rm_firewallpolicy: Add new module `azure_rm_firewallpolicy` ([#705](https://github.com/ansible-collections/azure/pull/705))
  - azure_rm_privatelinkservice: Add new module `azure_rm_privatelinkservice` ([#858](https://github.com/ansible-collections/azure/pull/858))
  - azure_rm_privatelinkservice_info: Add new module `azure_rm_privatelinkservice_info` ([#858](https://github.com/ansible-collections/azure/pull/858))
  - azure_rm_privateendpointconnection: Add new module `azure_rm_privateendpointconnection` ([#858](https://github.com/ansible-collections/azure/pull/858))
  - azure_rm_privateendpointconnection_info: Add new module `azure_rm_privateendpointconnection_info` ([#858](https://github.com/ansible-collections/azure/pull/858))
  - azure_rm_natgateway: Add new module `azure_rm_natgateway` ([#860](https://github.com/ansible-collections/azure/pull/860))
  - azure_rm_natgateway_info: Add new module `azure_rm_natgateway_info` ([#860](https://github.com/ansible-collections/azure/pull/860))
  - azure_rm_bastionhost: Add new module `azure_rm_bastionhost` ([#873](https://github.com/ansible-collections/azure/pull/873))
  - azure_rm_bastionhost_info: Add new module `azure_rm_bastionhost_info` ([#873](https://github.com/ansible-collections/azure/pull/873))
  - azure_rm_account_info: Add new module `azure_rm_account_info` to get facts for current logged-in user ([#922](https://github.com/ansible-collections/azure/pull/922))
  - azure_rm_virtualhubconnection: Add new module `azure_rm_virtualhubconnection` ([#939](https://github.com/ansible-collections/azure/pull/939))
  - azure_rm_virtualhubconnection_info: Add new module `azure_rm_virtualhubconnection_info` ([#939](https://github.com/ansible-collections/azure/pull/939))
  - azure_rm_aksagentpool: Add new module `azure_rm_aksagentpool` ([#974](https://github.com/ansible-collections/azure/pull/974))
  - azure_rm_aksagentpool_info: Add new module `azure_rm_aksagentpool_info` ([#974](https://github.com/ansible-collections/azure/pull/974))
  - azure_rm_aksagentpoolversion_info: Add new module `azure_rm_aksagentpoolversion_info` ([#974](https://github.com/ansible-collections/azure/pull/974))

### FEATURE ENHANCEMENT
  - azure_rm_container*: Azure container registry tags ([#830](https://github.com/ansible-collections/azure/pull/830))
  - azure_rm_loadbalancer: Support for `disable_outbound_snat` configuration ([#744](https://github.com/ansible-collections/azure/pull/744))
  - azure_rm_manageddisk:
    - Support for create `StandardSSD_ZRS` and `Premium_ZRS` managed disks ([#855](https://github.com/ansible-collections/azure/pull/855))
    - Support for mount disk to multiple VMs ([#867](https://github.com/ansible-collections/azure/pull/867))
  - azure_rm_manageddisk_info: Support to mount disk to multiple VMs ([#867](https://github.com/ansible-collections/azure/pull/867))
  - azure_rm_virtualmachine: 
    - Support for create `StandardSSD_ZRS` and `Premium_ZRS` managed disks ([#855](https://github.com/ansible-collections/azure/pull/855))
    - Support for configure `enableAutomaticUpdates` ([#933](https://github.com/ansible-collections/azure/pull/933))
  - azure_rm_storageaccount: 
    - Support for configure `static_website` ([#878](https://github.com/ansible-collections/azure/pull/878))
    - Support for `public_network_access` ([#875](https://github.com/ansible-collections/azure/pull/875))
    - Support for create Azure Data Lake Storage Gen2 storage account ([#998](https://github.com/ansible-collections/azure/pull/998))
    - Support for encrypt storage account ([#937](https://github.com/ansible-collections/azure/pull/937))
  - azure_rm_storageaccount_info: 
    - Support for `public_network_access` ([#875](https://github.com/ansible-collections/azure/pull/875))
    - Support for Azure Data Lake Storage Gen2 ([#998](https://github.com/ansible-collections/azure/pull/998))
    - Support for encrypt storage account ([#937](https://github.com/ansible-collections/azure/pull/937))
  - azure_keyvault_secret: Add environment variables to keyvault lookup plugin ([#978](https://github.com/ansible-collections/azure/pull/978))
  - README.md: Added prompt to install virtual environment ([#910](https://github.com/ansible-collections/azure/pull/910))
  - azure_rm_keyvaultkey: Adding support for `key_type`, `key_attributes`, `key_size`, `curve` ([#930](https://github.com/ansible-collections/azure/pull/930))
  - azure_rm_virtualmachinescaleset: Add new parameter `os_disk_size_gb`, allowing set os disk size ([#961](https://github.com/ansible-collections/azure/pull/961))
  - azure_rm_privateendpoint_info: Add connection details ([#965](https://github.com/ansible-collections/azure/pull/965))
  - azure_rm_aks: Support for upgrade nodepool kubernetes version ([#966](https://github.com/ansible-collections/azure/pull/966))
  - azure_rm_virtualnetworkgateway: Support set Virtual Network Gateway Generation ([#921](https://github.com/ansible-collections/azure/pull/921))
  - azure_rm_storage*: Update Storage dependencies ([#833](https://github.com/ansible-collections/azure/pull/833))
  - azure_rm_appserviceplan*: Update azure.mgmt.web ([#849](https://github.com/ansible-collections/azure/pull/849))
  - azure_rm_functionapp*: Update dependencies ([#849](https://github.com/ansible-collections/azure/pull/849))
  - azure_rm_webapp*: Update dependencies ([#849](https://github.com/ansible-collections/azure/pull/849))
  - azure_rm_backup*: Upgrade azure-mgmt-recoveryservice relate dependence ([#895](https://github.com/ansible-collections/azure/pull/895))
  - azure_rm_dns*: Upgrade azure-mgmt-dns to `v8.0.0` ([#879](https://github.com/ansible-collections/azure/pull/879))
  - azure_rm_cognitivesearch: Upgrade azure-mgmt-search to `v8.0.0` ([#896](https://github.com/ansible-collections/azure/pull/896))
  - azure_rm_cognitivesearch_info: Upgrade azure-mgmt-search to `v8.0.0` ([#896](https://github.com/ansible-collections/azure/pull/896))
  - azure_rm_privatedns*: Upgrade azure-mgmt-privatedns to `v1.0.0` ([#880](https://github.com/ansible-collections/azure/pull/880))
  - azure_rm_aks*: Upgrade azure-mgmt-containerservice to `v20.0.0` ([#881](https://github.com/ansible-collections/azure/pull/881))
  - azure_rm_containerinstance*: Upgrade azure-mgmt-containerinstance to `v9.0.0` ([#882](https://github.com/ansible-collections/azure/pull/882))
  - azure_rm_mysql*: Upgrade azure-mgmt-rdbms to `v10.0.0` ([#884](https://github.com/ansible-collections/azure/pull/884))
  - azure_rm_mariadb*: Upgrade azure-mgmt-rdbms to `v10.0.0` ([#884](https://github.com/ansible-collections/azure/pull/884))
  - azure_rm_postgresql*: Upgrade azure-mgmt-rdbms to `v10.0.0` ([#884](https://github.com/ansible-collections/azure/pull/884))
  - azure_rm_trafficmanager*: Upgrade azure-mgmt-trafficmanager to `v1.0.0` ([#886](https://github.com/ansible-collections/azure/pull/886))
  - azure_rm_loganalyticsworkspace: Upgrade azure-mgmt-loganalytics to `v12.0.0` ([#888](https://github.com/ansible-collections/azure/pull/888))
  - azure_rm_loganalyticsworkspace_info: Upgrade azure-mgmt-loganalytics to `v12.0.0` ([#888](https://github.com/ansible-collections/azure/pull/888))
  - azure_rm_servicebus*: Upgrade azure-mgmt-servicebus to `v7.1.0` ([#889](https://github.com/ansible-collections/azure/pull/889))
  - azure_rm_iothub*: Upgrade azure-mgmt-iothub to `v2.2.0` ([#892](https://github.com/ansible-collections/azure/pull/892))
  - azure_rm_datalakestore: Upgrade azure-mgmt-datalake-store to `v1.0.0` ([#898](https://github.com/ansible-collections/azure/pull/898))
  - azure_rm_datalakestore_info: Upgrade azure-mgmt-datalake-store to `v1.0.0` ([#898](https://github.com/ansible-collections/azure/pull/898))
  - azure_rm_eventhub: Upgrade azure-mgmt-eventhubs to `v10.1.0` ([#900](https://github.com/ansible-collections/azure/pull/900))
  - azure_rm_eventhub_info: Upgrade azure-mgmt-eventhubs to `v10.1.0` ([#900](https://github.com/ansible-collections/azure/pull/900))
  - azure_rm_notificationhub: Upgrade azure-mgmt-notificationhubs to `v7.0.0` ([#899](https://github.com/ansible-collections/azure/pull/899))
  - azure_rm_notificationhub_info: Upgrade azure-mgmt-notificationhubs to `v7.0.0` ([#899](https://github.com/ansible-collections/azure/pull/899))
  - azure_rm_cdn*: Upgrade azure-mgmt-cdn to `v11.0.0` ([#945](https://github.com/ansible-collections/azure/pull/945))
  - azure_rm_registration*: Upgrade azure-mgmt-managedservices to `v6.0.0` ([#948](https://github.com/ansible-collections/azure/pull/948))
  - azure_rm_hdinsightcluster: Upgrade hdinsight dependence to `v9.0.0` ([#951](https://github.com/ansible-collections/azure/pull/951))
  - azure_rm_hdinsightcluster_info: Upgrade hdinsight dependence to `v9.0.0` ([#951](https://github.com/ansible-collections/azure/pull/951))
  - azure_rm_role*: Upgrade azure-mgmt-authorizaiton to `v2.0.0` ([#955](https://github.com/ansible-collections/azure/pull/955))
  - azure_rm_cosmosdbaccount: Upgrade azure-mgmt-cosmosdb to `v6.4.0` ([#952](https://github.com/ansible-collections/azure/pull/952))
  - azure_rm_cosmosdbaccount_info: Upgrade azure-mgmt-cosmosdb to `v6.4.0` ([#952](https://github.com/ansible-collections/azure/pull/952))
  - azure_rm_keyvault*: upgrade azure-mgmt-keyvault to `v10.0.0` ([#959](https://github.com/ansible-collections/azure/pull/959))
  - requirements-azure.txt: Update azure-mgmt-core to `v1.3.0` ([#907](https://github.com/ansible-collections/azure/pull/907))

### BUG FIXING
  - azure_rm_keyvault_info: Fix `azure_rm_keyvault_info` `Resource.properties` not found error ([#872](https://github.com/ansible-collections/azure/pull/872))
  - azure_rm_aks: 
    - Change `aad_profile.admin_group_object_ids` to take a list of string ([#865](https://github.com/ansible-collections/azure/pull/865))
    - Fix `authorized_ip_ranges` not set bug ([#912](https://github.com/ansible-collections/azure/pull/912))
  - azure_rm_manageddisk:
    - Add missing parameters ([#925](https://github.com/ansible-collections/azure/pull/925))
    - If the disk exists, obtain parameters not configured ([#876](https://github.com/ansible-collections/azure/pull/876))
    - Add required option(`storage_account_id`) when importing a disk image ([#877](https://github.com/ansible-collections/azure/pull/877))
  - azure_rm_deployment_info: Fix API breaking change, replace `list` with `list_by_resource_group` ([#857](https://github.com/ansible-collections/azure/pull/857))
  - azure_rm_publicipaddress: Fix property get error.([#908](https://github.com/ansible-collections/azure/pull/908))
  - azure_rm_keyvault*: Fixes `credential_scopes` for track2 authentication when connecting to non-Azure Public cloud environments ([#854](https://github.com/ansible-collections/azure/pull/854))
  - azure_rm_keyvault: Expose `soft_delete_retention_in_days` ([#906](https://github.com/ansible-collections/azure/pull/906))
  - azure_rm_virtualmachine: Remove `started` default value ([#915](https://github.com/ansible-collections/azure/pull/915))
  - azure_rm_storageaccount: Add missing account type `Standard_GZRS` and `Standard_RAGZRS` ([#931](https://github.com/ansible-collections/azure/pull/931))
  - azure_rm_common: 
    - Replace `config` with `_config` in `azure_rm_common.py` to support the latest version of azure-mgmt-network ([#904](https://github.com/ansible-collections/azure/pull/904))
    - Fix azurerm MSI authentication with other Azure Cloud ([#894](https://github.com/ansible-collections/azure/pull/894))
    - Fix a sanity error ([#946](https://github.com/ansible-collections/azure/pull/946))
  - azure_rm_azurefirewall: Correct firewall action examples ([#962](https://github.com/ansible-collections/azure/pull/962))
  - azure_rm_webappaccessrestriction: Update test case ([#964](https://github.com/ansible-collections/azure/pull/964))

## v1.13.0 (2022-05-27)

### NEW MODULES
  - azure_rm_automationrunbook: Add new module azure_rm_automationrunbook ([#797](https://github.com/ansible-collections/azure/pull/797))
  - azure_rm_automationrunbook_info: Add new module azure_rm_automationrunbook ([#797](https://github.com/ansible-collections/azure/pull/797))
  - azure_rm_openshiftmanagedcluster_info: Add new module azure_rm_openshiftmanagedcluster_info  ([#755](https://github.com/ansible-collections/azure/pull/755))
  - azure_keyvault_secret: KeyVault Lookup Plugin ([#109](https://github.com/ansible-collections/azure/pull/109))
  - azure_rm_datafactory: Add new module azure_rm_datafacotry ([#840](https://github.com/ansible-collections/azure/pull/840))
  - azure_rm_datafactory_info: Add new module azure_rm_datafacotry ([#840](https://github.com/ansible-collections/azure/pull/840))

### FEATURE ENHANCEMENT
  - azure_rm_common.py: Upgrade azure-mgmt-automation to v1.0.0 ([#791](https://github.com/ansible-collections/azure/pull/791))
  - azure_rm_automationaccount: Upgrade azure-mgmt-automation to v1.0.0 ([#791](https://github.com/ansible-collections/azure/pull/791))
  - azure_rm_automationaccount_info: Upgrade azure-mgmt-automation to v1.0.0 ([#791](https://github.com/ansible-collections/azure/pull/791))
  - azure_rm_loadbalancer: Add support for `zones` ([#801](https://github.com/ansible-collections/azure/pull/801))
  - azure_rm_loadbalancer_info: Add support for `zones` ([#801](https://github.com/ansible-collections/azure/pull/801))
  - azure_rm.py: Update azure_rm examples ([#810](https://github.com/ansible-collections/azure/pull/810))
  - azure_rm_virtualmachinescaleset: Add support for `platform_fault_domain_count`, `orchestration_mode` ([#779](https://github.com/ansible-collections/azure/pull/779))
  - azure_rm_virtualmachinescaleset_info: Add support for `platform_fault_domain_count`, `orchestration_mode` ([#779](https://github.com/ansible-collections/azure/pull/779))
  - azure_rm_rediscache: Add support for `minimum_tls_version`, `public_network_access`, `redis_version` ([#680](https://github.com/ansible-collections/azure/pull/680))
  - azure_rm_rediscache_info: Add support for `minimum_tls_version`, `public_network_access`, `redis_version` ([#680](https://github.com/ansible-collections/azure/pull/680))
  - azure_rm_rediscachefirewallrule: Upgrade to truck2 SDK ([#680](https://github.com/ansible-collections/azure/pull/680))
  - azure_rm_appgateway: Add rewrite rule capability to appgateway module ([#747](https://github.com/ansible-collections/azure/pull/747))
  - azure_rm_appgateway_info: Add rewrite rule capability to appgateway module ([#747](https://github.com/ansible-collections/azure/pull/747))
  - azure_rm_sqlserver: SQL Database enhancement ([#681](https://github.com/ansible-collections/azure/pull/681))
  - azure_rm_common.py: Bump SQL SDK to v3 ([#681](https://github.com/ansible-collections/azure/pull/681))
  - azure_rm_cosmosdbaccount: Add support for `enable_free_tier`, `mongo_version`, `public_network_access`, `ip_range_filter` parameter is being deprecated in favor of `ip_rules` ([#675](https://github.com/ansible-collections/azure/pull/675))
  - azure_rm_cosmosdbaccount_info: Add support for `enable_free_tier`, `mongo_version`, `public_network_access`, `ip_range_filter` parameter is being deprecated in favor of `ip_rules`  ([#675](https://github.com/ansible-collections/azure/pull/675))
  - azure_rm_publicipaddress: Add support for `zones` ([#829](https://github.com/ansible-collections/azure/pull/829))
  - azure_rm_publicipaddress_info: Add support for `zones` ([#829](https://github.com/ansible-collections/azure/pull/829))
  - azure_rm_image: Add support `hyper_v_generation` ([#832](https://github.com/ansible-collections/azure/pull/832))
  - azure_rm_image_info: Add support `hyper_v_generation` ([#832](https://github.com/ansible-collections/azure/pull/832))

### BUG FIXING
  - pr-pipelines.yml: Add python3.9 for CI ([#783](https://github.com/ansible-collections/azure/pull/783))
  - config.yml: Update test configure ([#790](https://github.com/ansible-collections/azure/pull/790))
  - azure_rm_manageddisk: Fixed the inconsistent return value of `attach_caching` caused by the azure-mgmt-compute upgrade ([#799](https://github.com/ansible-collections/azure/pull/799))
  - azure_rm_loadbalancer: Fix forced update bug caused by azure_rm_loadbalancer obtaining subnet predefined value ([#800](https://github.com/ansible-collections/azure/pull/800))
  - azure_rm_virtualmachine: Add license type for RHEL/SLES Azure Hybrid Benefit ([#804](https://github.com/ansible-collections/azure/pull/804))
  - azure_rm_*: Update the document to meet the change requirements of Ansible 2.14 ([#814](https://github.com/ansible-collections/azure/pull/814))
  - azure_rm_appgateway_info: Update azure_rm_appgateway_info to use track2 dependencies ([#817](https://github.com/ansible-collections/azure/pull/817))
  - azure_rm_virtualmachine: Fix virtual machine top issue ([#767](https://github.com/ansible-collections/azure/pull/767))
  - azure_rm_subscription_info: Update azure_rm_subscription_info tags element type ([#819](https://github.com/ansible-collections/azure/pull/819))
  - azure_rm_manageddisk: Fix `os_type` comparison in azure_rm_manageddisk with existing disk ([#621](https://github.com/ansible-collections/azure/pull/621))
  - azure_rm_appgateway: Persist SSL configuration for appgateway ([#746](https://github.com/ansible-collections/azure/pull/746))
  - azure_rm_appgateway_info: Persist SSL configuration for appgateway ([#746](https://github.com/ansible-collections/azure/pull/746))
  - azure_rm_publicipaddress: Fix azure_rm_publicipaddress documentation page throws error ([#822]( https://github.com/ansible-collections/azure/pull/822))
  - azure_keyvault_secret: Fix Ansible dev version Sanity error in plugin file ([#825](https://github.com/ansible-collections/azure/pull/825))
  - azure_rm_rediscache: Fix Ansible dev version Sanity error in plugin file ([#825](https://github.com/ansible-collections/azure/pull/825))
  - azure_rm_keyvaultkey: Improved keyvault interaction auth_source=cli logic ([#823](https://github.com/ansible-collections/azure/pull/823))
  - azure_rm_keyvaultkey_info: Improved keyvault interaction auth_source=cli logic ([#823](https://github.com/ansible-collections/azure/pull/823))
  - azure_rm_keyvaultsecret: Improved keyvault interaction auth_source=cli logic ([#823](https://github.com/ansible-collections/azure/pull/823))
  - azure_rm_keyvaultsecret_info: Improved keyvault interaction auth_source=cli logic ([#823](https://github.com/ansible-collections/azure/pull/823))
  - azure_keyvault_secret: Add `hyper_v_generation` feature to azure_rm_image module ([#832](https://github.com/ansible-collections/azure/pull/832))
  - azure_rm_webapp: Correct documentation of return attribute for azure_rm_webapp ([#846](https://github.com/ansible-collections/azure/pull/846))
  - azure_rm_virtualmachine: When zones is null, there is no need to compare ([#853](https://github.com/ansible-collections/azure/pull/853))
  - All info modules: Change the tags type of the Info module to list and the element type to string ([#821](https://github.com/ansible-collections/azure/pull/821))
  - azcollection: Install collection to local directory during development ([#763](https://github.com/ansible-collections/azure/pull/763))

### BREAKING CHANGES:
  - azure_rm_virtualmachinescaleset: Change default value of `single_placement_group` from `True` to `False` ([#851](https://github.com/ansible-collections/azure/pull/851))

## v1.12.0 (2022-03-14)

### NEW MODULES

### FEATURE ENHANCEMENT
  - azure_rm_privateendpointdnszonegroup: Add `private_dns_zone_id` for `azure_rm_privateendpointdnszonegroup` ([#735](https://github.com/ansible-collections/azure/pull/735))
  - azure_rm_virtualmachineextension: Ignore comparing `protected_settings` ([#580](https://github.com/ansible-collections/azure/pull/580))
  - azure_rm_aks: Add new parameter to enable AAD profile ([#654](https://github.com/ansible-collections/azure/pull/654))
  - azure_rm_*: Upgrade azure-mgmt-network to 19.1.0 ([#729](https://github.com/ansible-collections/azure/pull/729))
  - azure_rm_sqldatabase: Parse datetime module arguments ([#623](https://github.com/ansible-collections/azure/pull/623))
  - azure_rm_sqldatabase_info: Parse datetime module arguments ([#623](https://github.com/ansible-collections/azure/pull/623))
  - azure_rm_virtualmachine: Add VM status detection mechanism ([#772](https://github.com/ansible-collections/azure/pull/772))
  - azure_rm_*: Upgrade azure-mgmt-compute SDK to track2 SDK ([#672](https://github.com/ansible-collections/azure/pull/672))
  - azure_rm_*: Upgrade azure-mgmt-storage to 19.0.0 ([#777](https://github.com/ansible-collections/azure/pull/777))
  - requirements-azure.txt: Update azure-cli-core to 2.34.0 ([#775](https://github.com/ansible-collections/azure/pull/775))
  - azure_rm_virtualmachine: Update `azure_rm_galleryimage` to allow Hyper-V Generation ([#647](https://github.com/ansible-collections/azure/pull/647))

### BUG FIXING
  - azure_rm_roleassignment: Fix mismatch assignment error ([#613](https://github.com/ansible-collections/azure/pull/613))
  - README.md: Delete unnecessary backtick in readme ([#736](https://github.com/ansible-collections/azure/pull/736))
  - azure_rm_availabilityset: Fix `check_mode` support ([#627](https://github.com/ansible-collections/azure/pull/627))
  - azure_rm_manageddisk: Fix `azure_rm_manageddisk` caching comparison ([#624](https://github.com/ansible-collections/azure/pull/624))
  - azure_rm_publicipaddress: Add mandatory field when updating IPAddress ([#752](https://github.com/ansible-collections/azure/pull/752))
  - azure_rm_common: Remove unused and deprecated `VERSION` import ([#751](https://github.com/ansible-collections/azure/pull/751))
  - azure_rm_keyvaultkey: Conditionally call non MSI authorization when interacting with keyvault ([#770](https://github.com/ansible-collections/azure/pull/770))
  - azure_rm_keyvaultkey_info: Conditionally call non MSI authorization when interacting with keyvault ([#770](https://github.com/ansible-collections/azure/pull/770))
  - azure_rm_keyvaultsecret: Conditionally call non MSI authorization when interacting with keyvault ([#770](https://github.com/ansible-collections/azure/pull/770))
  - azure_rm_keyvaultsecret_info: Conditionally call non MSI authorization when interacting with keyvault ([#770](https://github.com/ansible-collections/azure/pull/770))
  - azure_rm_common: Fix typo error. ([#769](https://github.com/ansible-collections/azure/pull/769))
  - azure_rm_cosmosdbaccount: Update test case region ([#776](https://github.com/ansible-collections/azure/pull/776))
  - azure_rm_virtualmachine_info: Fix VM info module for failed VM provisions ([#745](https://github.com/ansible-collections/azure/pull/745))
  - azure_rm_loadbalancer_info: Fix documentation issue ([#719](https://github.com/ansible-collections/azure/pull/719))
  - azure_rm: Fix ansible 2.13 sanity fail ([#778](https://github.com/ansible-collections/azure/pull/778))
  - azure_rm: Append secondary network information to relevant `hostvars` ([#733](https://github.com/ansible-collections/azure/pull/733))


## v1.11.0 (2022-01-18)

### NEW MODULES
  - azure_rm_virtualhub: New Module azure_rm_virtualhub ([#597](https://github.com/ansible-collections/azure/pull/597))
  - azure_rm_virtualhub_info: New Module azure_rm_virtualhub_info ([#597](https://github.com/ansible-collections/azure/pull/597))
  - azure_rm_hostgroup: New Module : azure_rm_hostgroup ([#704](https://github.com/ansible-collections/azure/pull/704))
  - azure_rm_hostgroup_info: New Module : azure_rm_hostgroup ([#704](https://github.com/ansible-collections/azure/pull/704))
  - azure_rm_privateendpointdnszonegroup: Add module for private endpoint DNS zone groups ([#689](https://github.com/ansible-collections/azure/pull/689))
  - azure_rm_privateendpointdnszonegroup_info: Add module for private endpoint DNS zone groups ([#689](https://github.com/ansible-collections/azure/pull/689))
  - azure_rm_monitordiagnosticsetting: Add new monitor diagnostic setting modules ([#701](https://github.com/ansible-collections/azure/pull/701))
  - azure_rm_monitordiagnosticsetting_info: Add new monitor diagnostic setting modules ([#701](https://github.com/ansible-collections/azure/pull/701))
  - azure_rm_storageshare: Azure storage file share module ([#603](https://github.com/ansible-collections/azure/pull/603))
  - azure_rm_storageshare_info: Azure storage file share module ([#603](https://github.com/ansible-collections/azure/pull/603))
  - azure_rm_appgateway_info: Application gateway start/stop ability and info module ([#673](https://github.com/ansible-collections/azure/pull/673))

### FEATURE ENHANCEMENT
  - azure_rm_webapp: Add additional parameters for webapp site config ([#695](https://github.com/ansible-collections/azure/pull/695))
  - azure_rm_webapp_info: Add additional parameters for webapp site config ([#695](https://github.com/ansible-collections/azure/pull/695))
  - azure_rm: Add managed disks list to dynamic inventory hostvars ([#687](https://github.com/ansible-collections/azure/pull/687))
  - azure_rm_networkinterface: Add ability to connect network interface to application gateway backend pool ([#683](https://github.com/ansible-collections/azure/pull/683))
  - azure_rm_networkinterface_info: Add ability to connect network interface to application gateway backend pool ([#683](https://github.com/ansible-collections/azure/pull/683))
  - azure_rm_keyvaultsecret: feat: Add expiry information for keyvaultsecrets ([#660](https://github.com/ansible-collections/azure/pull/660))
  - azure_rm_virtualmachine_info: Verify the VM status after created ([#657](https://github.com/ansible-collections/azure/pull/657))
  - azure_rm_appgateway: Add advanced routing/redirect support for application gateway ([#685](https://github.com/ansible-collections/azure/pull/685))
  - azure_rm_virtualmachine: Add new parameter `proximity_placement_group` ([#611](https://github.com/ansible-collections/azure/pull/611))
  - azure_rm_virtualmachine_info: Add new parameter `proximity_placement_group` ([#611](https://github.com/ansible-collections/azure/pull/611))
  - azure_rm_dnsrecordset: Added Metadata support ([#589](https://github.com/ansible-collections/azure/pull/589))
  - azure_rm_dnsrecordset_info: Added Metadata support ([#589](https://github.com/ansible-collections/azure/pull/589))
  - azure_rm_virtualmachine_info: Add managed disk ID to returned facts for data disks ([#682](https://github.com/ansible-collections/azure/pull/682))
  - azure_rm_appgateway: Application gateway start/stop ability ([#673](https://github.com/ansible-collections/azure/pull/673))
  - azure_rm_aks: Add new feature - `outbound_type` ([#651](https://github.com/ansible-collections/azure/pull/651))
  - azure_rm_common: Support track2 SDK CLI authorization ([#676](https://github.com/ansible-collections/azure/pull/676))

### BUG FIXING
  - azure_rm_common: Supprot track2 SDK ([#670](https://github.com/ansible-collections/azure/pull/670))
  - azure_rm_common: Allow module-level subscription id to be used for cross-subscription resource management ([#694](https://github.com/ansible-collections/azure/pull/694))
  - azure_rm_appserviceplan: Correct idempotency and premium SKU plans ([#693](https://github.com/ansible-collections/azure/pull/693))
  - ignore-2.13.txt: Update ignore file ([#696](https://github.com/ansible-collections/azure/pull/696))
  - ignore-2.12.txt: Update ignore file ([#696](https://github.com/ansible-collections/azure/pull/696))
  - ignore-2.11.txt: Update ignore file ([#696](https://github.com/ansible-collections/azure/pull/696))
  - ignore-2.10.txt: Update ignore file ([#696](https://github.com/ansible-collections/azure/pull/696))
  - azure_rm_virtualmachine: Misc typo fixes ([#698](https://github.com/ansible-collections/azure/pull/698))
  - azure_rm_publicipaddress: Misc typo fixes ([#698](https://github.com/ansible-collections/azure/pull/698))
  - azure_rm_virtualmachinescaleset: Misc typo fixes ([#698](https://github.com/ansible-collections/azure/pull/698))
  - azure_rm_appgateway: Update `state` document ([#674](https://github.com/ansible-collections/azure/pull/674))
  - azure_rm_dnsrecordset_info: Fixed error where recordset relative did not exist ([#706](https://github.com/ansible-collections/azure/pull/706))
  - azure_rm_cosmosdbaccount_info: Correct cosmosdb info module when loading by resource group ([#709](https://github.com/ansible-collections/azure/pull/709))
  - azure_rm_notificationhub: Avoid the case when service returns None ([#718](https://github.com/ansible-collections/azure/pull/718))
  - azure_rm_notificationhub_info: Avoid the case when service returns None ([#718](https://github.com/ansible-collections/azure/pull/718))
  - azure_rm_common: common: Handle exception raised while loading profile ([#610](https://github.com/ansible-collections/azure/pull/610))
  - README.md: Clarify document for installing collection and dependencies ([#716](https://github.com/ansible-collections/azure/pull/716))
  - azure_rm_deployment: azure_rm_deployment : Fixed tags related bug ([#641](https://github.com/ansible-collections/azure/pull/641))
  - azure_rm_subnet: Dissociate routetable from subnet ([#727](https://github.com/ansible-collections/azure/pull/727))
  - azure_rm_securitygroup_info: Align `azure_rm_securitygroup_info` return to match `azure_rm_securitygroup` ([#726](https://github.com/ansible-collections/azure/pull/726))


## v1.10.0 (2021-10-22)

### NEW MODULES
  - azure_rm_virtualmachinesize_info: VirtualMachineSize facts module ([#605](https://github.com/ansible-collections/azure/pull/605))
  - azure_rm_diskencryptionset: New module: azure_rm_diskencryptionset ([#552](https://github.com/ansible-collections/azure/pull/552))
  - azure_rm_diskencryptionset_info: New module: azure_rm_diskencryptionset ([#552](https://github.com/ansible-collections/azure/pull/552))

### FEATURE ENHANCEMENT
  - azure_rm_availabilityset: Add ProximityPlacementGroup to azure_rm_availabilityset ([#612](https://github.com/ansible-collections/azure/pull/612))
  - main.yml: Update vmss test case ([#633](https://github.com/ansible-collections/azure/pull/633))
  - main.yml: Enable VMSS TEST ([#634](https://github.com/ansible-collections/azure/pull/634))
  - azure_rm_keyvault: Add new parameter enable_purge_protection to azure_rm_keyvault ([#643](https://github.com/ansible-collections/azure/pull/643))
  - azure_rm_keyvault_info: Add new parameter enable_purge_protection to azure_rm_keyvault ([#643](https://github.com/ansible-collections/azure/pull/643))
  - azure_rm_containerinstance: Fixed issue #232 Added Volume mount support for container instances ([#338](https://github.com/ansible-collections/azure/pull/338))
  - azure_rm_containerinstance_info: Fixed issue #232 Added Volume mount support for container instances ([#338](https://github.com/ansible-collections/azure/pull/338))
  - ignore-2.13.txt: Copy ignore-2.12.txt to ignore-2.13.txt ([#642](https://github.com/ansible-collections/azure/pull/642))
  - azure_rm_mysqlserver: Add new parameter (azure_rm_mysqlserver.py)--- restarted ([#600](https://github.com/ansible-collections/azure/pull/600))

### BUG FIXING
  - azure_rm_virtualmachineimage_info: Support to get the latest version of a virtual machine image ([#617](https://github.com/ansible-collections/azure/pull/617))
  - azure_rm_virtualmachine: azure_rm_virtualmachine: suppress no_log warning on ssh_password_enabled parameter ([#622](https://github.com/ansible-collections/azure/pull/622))
  - azure_rm_mysqlserver: Remove version 5.6, bump minimum version from 5.6 to 5.7 ([#626](https://github.com/ansible-collections/azure/pull/626))
  - azure_rm_manageddisk: Update azure_rm_manageddisk Doc to reflect return value ([#616]( https://github.com/ansible-collections/azure/pull/616))
  - azure_rm_managementgroup_info: bugfix for azure_rm_managementgroup_info module, subscriptions not detected as correct type ([#630](https://github.com/ansible-collections/azure/pull/630))
  - azure_rm_manageddisk: Fix manageddisk unmount documentation ([#649](https://github.com/ansible-collections/azure/pull/649))
  - azure_rm_securitygroup: Fix azure_rm_securitygroup doc ([#640](https://github.com/ansible-collections/azure/pull/640))


## v1.9.0 (2021-08-23)

### NEW MODULES
  - azure_rm_ddosprotectionplan: New module: azure_rm_ddosprotectionplan ([#493](https://github.com/ansible-collections/azure/pull/493))
  - azure_rm_ddosprotectionplan_info: New module: azure_rm_ddosprotectionplan ([#493](https://github.com/ansible-collections/azure/pull/493))
  - azure_rm_privateendpoint: Azure rm privateendpoint ([#593](https://github.com/ansible-collections/azure/pull/593))
  - azure_rm_privateendpoint_info: Azure rm privateendpoint ([#593](https://github.com/ansible-collections/azure/pull/593))
  - azure_rm_webappaccessrestriction: New modules for webapp network access restrictions ([#594](https://github.com/ansible-collections/azure/pull/594))
  - azure_rm_webappaccessrestriction_info: New modules for webapp network access restrictions ([#594](https://github.com/ansible-collections/azure/pull/594))
  - azure_rm_webappvnetconnection: New modules for webapp vnet connection ([#590](https://github.com/ansible-collections/azure/pull/590))
  - azure_rm_webappvnetconnection_info: New modules for webapp vnet connection ([#590](https://github.com/ansible-collections/azure/pull/590))

### FEATURE ENHANCEMENT
  - azure_rm_networkinterface: Allow IPv6 with NetworkInterfaceIPConfiguration ([#582](https://github.com/ansible-collections/azure/pull/582))
  - azure_rm_postgresqlserver: postgres server backup-support ([#566](https://github.com/ansible-collections/azure/pull/566))
  - azure_rm_virtualmachine: Addition of Spot instance support for VM and VMSS ([#559](https://github.com/ansible-collections/azure/pull/559))
  - azure_rm_virtualmachinescaleset: Addition of Spot instance support for VM and VMSS ([#559](https://github.com/ansible-collections/azure/pull/559))
  - azure_rm_appgateway: Add support for application gateway path-based routing ([#452](https://github.com/ansible-collections/azure/pull/452))
  - main.yml: Virtual machine test case update ([#595](https://github.com/ansible-collections/azure/pull/595))
  - azure_rm_appgateway: Allow application gateway probe to use host header from HTTP settings ([#450](https://github.com/ansible-collections/azure/pull/450))
  - azure_rm_*_info: Fixed dev branch sanity error ([#596](https://github.com/ansible-collections/azure/pull/596))

### BUG FIXING
  - runtime.yml: Add runtime.yml ([#587](https://github.com/ansible-collections/azure/pull/587))
  - galaxy.yml: Add resource tags ([#592](https://github.com/ansible-collections/azure/pull/592))
  - CONTRIBUTING.md: Update contributing notes for dev/testing ([#574](https://github.com/ansible-collections/azure/pull/574))
  - main.yml: BUG FIX: Get latest VM image version ([#606](https://github.com/ansible-collections/azure/pull/606))


## v1.8.0 (2021-08-02)

### NEW MODULES
  - azure_rm_notificationhub: New module: azure_rm_notificationhub ([#496](https://github.com/ansible-collections/azure/pull/496/))
  - azure_rm_notificationhub_info: New module: azure_rm_notificationhub ([#496](https://github.com/ansible-collections/azure/pull/496/))
  - azure_rm_expressroute: New module: azure_rm_expressroute ([#484](https://github.com/ansible-collections/azure/pull/484))
  - azure_rm_expressroute_info: New module: azure_rm_expressroute ([#484](https://github.com/ansible-collections/azure/pull/484))

### FEATURE ENHANCEMENT
  - azure_rm_aks: azure_rm_aks: cluster client & models API version ([#497](https://github.com/ansible-collections/azure/pull/497))
  - azure_rm_aks: add new paramter node_labels for agent_pool ([#577](https://github.com/ansible-collections/azure/pull/577))
  - azure_rm_aks: azure_rm_aks: support system-assigned (managed) identity, ([#514](https://github.com/ansible-collections/azure/pull/514))
  - azure_rm_mysqlserver: Add new feature storage_profile ([#563](https://github.com/ansible-collections/azure/pull/563))

### BUG FIXING
  - azure_rm_virtualmachine_info: Add name to return data_disks ([#565](https://github.com/ansible-collections/azure/pull/565))
  - azure_rm_loadbalancer: enable_floating_ip is for SQL AlwaysOn not SNAT ([#560](https://github.com/ansible-collections/azure/pull/560))
  - azure_rm_containerregistry: Add return value for azure_rm_containerregistry idempotent test ([#578](https://github.com/ansible-collections/azure/pull/578))
  - azure_rm_containerregistry_info: Add return value for azure_rm_containerregistry idempotent test ([#578](https://github.com/ansible-collections/azure/pull/578))
  - azure_rm_roleasignment: azure_rm_roleassignment bugfix ([#464](https://github.com/ansible-collections/azure/pull/464))
  - azure_rm_roleasignment_info: azure_rm_roleassignment bugfix ([#464](https://github.com/ansible-collections/azure/pull/464))
  - azure_rm_aks: Upddate test case ([#585](https://github.com/ansible-collections/azure/pull/585))
  - azure_rm_cosmosdbaccount: Upddate test case ([#585](https://github.com/ansible-collections/azure/pull/585))


## v1.7.0 (2021-06-08)

### NEW MODULES
  - azure_rm_adapplication: New module: azure_rm_adapplication ([#215](https://github.com/ansible-collections/azure/pull/215))
  - azure_rm_adapplication_info: New module: azure_rm_adapplication ([#215](https://github.com/ansible-collections/azure/pull/215))
  - azure_rm_adgroup: New module: azure_rm_adgroup ([#423](https://github.com/ansible-collections/azure/pull/423))
  - azure_rm_adgroup_info: New module: azure_rm_adgroup ([#423](https://github.com/ansible-collections/azure/pull/423))
  - azure_rm_apimanagement: New Module [API Management] ([#322](https://github.com/ansible-collections/azure/pull/322))
  - azure_rm_apimanagement_info: New Module [API Management] ([#322](https://github.com/ansible-collections/azure/pull/322))
  - azure_rm_ipgroup: New module: azure_rm_ipgroup ([#528](https://github.com/ansible-collections/azure/pull/528))
  - azure_rm_ipgroup_info: New module: azure_rm_ipgroup ([#528](https://github.com/ansible-collections/azure/pull/528))
  - azure_rm_eventhub: New module: azure_rm_eventhub ([#519](https://github.com/ansible-collections/azure/pull/519))
  - azure_rm_eventhub_info: New module: azure_rm_eventhub ([#519](https://github.com/ansible-collections/azure/pull/519))
  - azure_rm_proximityplacementgroup: New module: azure_rm_proximityplacementgroup ([#501](https://github.com/ansible-collections/azure/pull/501))
  - azure_rm_proximityplacementgroup_info: New module: azure_rm_proximityplacementgroup ([#501](https://github.com/ansible-collections/azure/pull/501))
  - azure_rm_privatednszonelink: New module: azure_rm_privatednszonelink ([#495](https://github.com/ansible-collections/azure/pull/495))
  - azure_rm_privatednszonelink_info: New module: azure_rm_privatednszonelink ([#495](https://github.com/ansible-collections/azure/pull/495))

### FEATURE ENHANCEMENT
  - azure_rm_virtualmachine_info: Add availability zones to azure_rm_virtualmachine_info module ([#523](https://github.com/ansible-collections/azure/pull/523))
  - azure: Add log_mode and log_path to azure.py ([#540](https://github.com/ansible-collections/azure/pull/540))

### BUG FIXING
  - ado: Optimizing ado.sh ([#510](https://github.com/ansible-collections/azure/pull/510))
  - azure_rm_securitygroup: azure_rm_securitygroup - idempotent when args are lists ([#507](https://github.com/ansible-collections/azure/pull/507))
  - azure_rm_openshiftmanagedcluster: Fix an issue identifying a creation/deletion error [(#542](https://github.com/ansible-collections/azure/pull/542))
  - azure_rm_adapplication: disable tlsv1_1 in app gateway test. ([#544](https://github.com/ansible-collections/azure/pull/544))
  - pr-pipelines: increase integration testing timeout ([#549](https://github.com/ansible-collections/azure/pull/549))
  - tests/integration/targets/azure_rm_apimanagement/tasks/main.yml: Update sleep relate method ([#550](https://github.com/ansible-collections/azure/pull/550))
  - tests/integration/targets/azure_rm_appgateway/aliases: Disable azure_rm_appgateway relate test ([#558](https://github.com/ansible-collections/azure/pull/558))


## v1.6.0 (2021-04-29)

### NEW MODULES
  - azure_rm_search: Add new module to deploy Azure Cognitive Search 'azure_rm_cognitivesearch' ([#372](https://github.com/ansible-collections/azure/pull/372))
  - azure_rm_search_info: Add new module to deploy Azure Cognitive Search 'azure_rm_cognitivesearch' ([#372](https://github.com/ansible-collections/azure/pull/372))
  - azure_rm_apimanagementservice: Added new module for Azure API management service. ([#333](https://github.com/ansible-collections/azure/pull/333#))
  - azure_rm_apimanagementservice_info: Added new module for Azure API management service. ([#333](https://github.com/ansible-collections/azure/pull/333#))
  - azure_rm_virtualwan: Add new module relate with Virtual WAN ([#329](https://github.com/ansible-collections/azure/pull/329))
  - azure_rm_virtualwan_info: Add new module relate with Virtual WAN ([#329](https://github.com/ansible-collections/azure/pull/329))
  - azure_rm_vpnsite: Add new module relate with VPN site ([#328](https://github.com/ansible-collections/azure/pull/328))
  - azure_rm_vpnsite_info: Add new module relate with VPN site ([#328](https://github.com/ansible-collections/azure/pull/328))
  - azure_rm_vpnsitelink_info: Add new module relate with VPN site ([#328](https://github.com/ansible-collections/azure/pull/328))
  - azure_rm_aduser: Add new module for AD Users ([#402](https://github.com/ansible-collections/azure/pull/402))
  - azure_rm_aduser_info: Add new module for AD Users ([#402](https://github.com/ansible-collections/azure/pull/402))

### FEATURE ENHANCEMENT
  - ignore-2.12: Add 2.11 to test matrix, add ignore-2.12.txt ([#480](https://github.com/ansible-collections/azure/pull/480))
  - azure_rm_appgateway: Support subnet lookup for app gateway ([#451](https://github.com/ansible-collections/azure/pull/451))
  - azure_rm_storageaccount: Update azure_rm_storageaccount relate test yml ([#488](https://github.com/ansible-collections/azure/pull/488))
  - pr-pipeline: use python3.8 as default version,and using ubuntu20. ([#509](https://github.com/ansible-collections/azure/pull/509))

### BUG FIXING
  - azure: Paultaiton 20210409 requirements doc ([#485](https://github.com/ansible-collections/azure/pull/485))
  - azure_rm_storageaccount: Allow storage account type Premium_ZRS for FileStorage and BlockBlobStorage ([#482](https://github.com/ansible-collections/azure/pull/482))
  - azure_rm_*: Fix sanity test related errors ([#506](https://github.com/ansible-collections/azure/pull/506))
  - azure_rm: Fixing sanity test issue for ansible 2.11 ([#511](http://fanyi.youdao.com/?keyfrom=dict2.index))
  - azure_rm: Fixing inventory issue ([#518](https://github.com/ansible-collections/azure/pull/518))
  - azure_rm_aduser: fixing update account_enabled bug in azure_rm_aduser.py ([#536](https://github.com/ansible-collections/azure/pull/536))
  - azure_rm_common: fixing ad related auth issue when using service principal. ([#537](https://github.com/ansible-collections/azure/pull/537))
  - azure_rm_aduser: change class name of azure_rm_aduser ([#538](https://github.com/ansible-collections/azure/pull/538))

## v1.5.0 (2021-03-26)

### NEW MODULES
  - azure_rm_aksupgrade_info: Add new module to get available upgrade versions for an AKS cluster ([#405](https://github.com/ansible-collections/azure/pull/405))
  - azure_rm_backuppolicy: Add new module to manage backup policies ([#373](https://github.com/ansible-collections/azure/pull/373))
  - azure_rm_backuppolicy_info: Add new module to manage backup policies ([#373](https://github.com/ansible-collections/azure/pull/373))
  - azure_rm_managementgroup_info: New module azure_rm_managementgroup_info ([#428](https://github.com/ansible-collections/azure/pull/428))
  - azure_rm_datalakestore: Add new module azure_rm_datalakestore ([#352](https://github.com/ansible-collections/azure/pull/352))
  - azure_rm_datalakestore_info: Add new module azure_rm_datalakestore ([#352](https://github.com/ansible-collections/azure/pull/352))

### FEATURE ENHANCEMENT
  - azure_rm_aks: add creation and deletion of nodepools ([#440](https://github.com/ansible-collections/azure/pull/440))
  - azure_rm_loganalyticsworkspace: Add tags for azure_rm_loganalyticsworkspace ([#434](https://github.com/ansible-collections/azure/pull/434))
  - sanity-requirements-azure: Bump cryptography from 3.2 to 3.3.2 ([#424](https://github.com/ansible-collections/azure/pull/424))
  - azure_rm_keyvaultsecret: Conditionally call MSI auth when interacting with keyvault ([#356](https://github.com/ansible-collections/azure/pull/356))
  - azure_rm_keyvaultsecret_info: Conditionally call MSI auth when interacting with keyvault ([#356](https://github.com/ansible-collections/azure/pull/356))
  - azure_rm_keyvaultkey: Conditionally call MSI auth when interacting with keyvault ([#356](https://github.com/ansible-collections/azure/pull/356))
  - azure_rm_keyvaultkey_info: Conditionally call MSI auth when interacting with keyvault ([#356](https://github.com/ansible-collections/azure/pull/356))
  - azure_rm_keyvault: Set the default value of enable_soft_delete to true ([#463](https://github.com/ansible-collections/azure/pull/463))
  - azure_rm_keyvault_info: Set the default value of enable_soft_delete to true ([#463](https://github.com/ansible-collections/azure/pull/463))

### BUG FIXING
  - azure_tags: Improve the documentation of tags ([#415](https://github.com/ansible-collections/azure/pull/415))
  - azure_rm_registrationassignment: fixed SyntaxWarning ([#427](https://github.com/ansible-collections/azure/pull/427))
  - azure_rm_adserviceprincipal: Update azure_rm_adserviceprincipal examples ([#414](https://github.com/ansible-collections/azure/pull/414))
  - azure_rm_keyvault_info: change description for access policies return value ([#426](https://github.com/ansible-collections/azure/pull/426))
  - azure_rm_*: modules: remove ANSIBLE_METADATA ([#436](https://github.com/ansible-collections/azure/pull/436))
  - azure_rm_backuppolicy: Update azure_rm_backupolicy add version ([#449](https://github.com/ansible-collections/azure/pull/449))
  - azure_rm_backuppolicy_info: Update azure_rm_backupolicy add version ([#449](https://github.com/ansible-collections/azure/pull/449))
  - azure_rm_image: Revert images API version ([#432](https://github.com/ansible-collections/azure/pull/432))
  - azure_rm_image_info: Revert images API version ([#432](https://github.com/ansible-collections/azure/pull/432))
  - azure_rm_openshiftmanagedcluster: resolve issue (#268) ([#307](https://github.com/ansible-collections/azure/pull/307))
  - azure_rm_virtualnetwork: Unrestrict the virtual network of multiple DNS servers when I(purge_a… ([#462](https://github.com/ansible-collections/azure/pull/462))
  - azure_rm_storageaccount: Correct doc for storageaccount network_acls options ([#456](https://github.com/ansible-collections/azure/pull/456))
  - azure_rm_storageaccount: Update azure_rm_storageaccount.py ([#458](https://github.com/ansible-collections/azure/pull/458))
  - azure_rm_datalakestore: Transfer azure_rm_datalakestore test group 10 ([#465](https://github.com/ansible-collections/azure/pull/465))
  - azure_rm_datalakestore: Delete datalake resource group after pipeline test ([#466](https://github.com/ansible-collections/azure/pull/466))


## v1.4.0 (2021-01-26)

### NEW MODULES
  - azure_rm_route_info: add azure_rm_route_info module ([#334](https://github.com/ansible-collections/azure/pull/334))

### FEATURE ENHANCEMENT
  - azure_rm_postgresqlserver: add storage_autogrow option to postgresqlserver ([#387](https://github.com/ansible-collections/azure/pull/387))
  - azure_rm_keyvaultsecret: add content type parameter to azure_rm_keyvaultsecret ([#317](https://github.com/ansible-collections/azure/pull/317))
  - azure_rm_keyvaultsecret_info: add content type parameter to azure_rm_keyvaultsecret ([#317](https://github.com/ansible-collections/azure/pull/317))
  - azure_rm_mysqlserver: add missing Mysql version 8.0 ([#319](https://github.com/ansible-collections/azure/pull/319))

### BUG FIXING
  - Test_unit: add resource group for datalake store testing in ado pipeline ([#375](https://github.com/ansible-collections/azure/pull/375))
  - README.md: update README to include a link to documentation ([#376](https://github.com/ansible-collections/azure/pull/376))
  - azure_rm_deployment: update azure_rm_deployment document ([#384](https://github.com/ansible-collections/azure/pull/384))
  - azure_rm_azurefirewall: add support for tags in exec_module ([#360](https://github.com/ansible-collections/azure/pull/360))
  - Test_unit: disable generate VM using password for regression testing purpose ([#393](https://github.com/ansible-collections/azure/pull/393))
  - azure_rm_keyvaultsecret_info: Fix doc on returned field name ([#389](https://github.com/ansible-collections/azure/pull/389))
  - azure_rm_virtualnetworkpeering: azure_rm_virtualnetworkpeering: Fix unable to remove non-existing pee…([#400](https://github.com/ansible-collections/azure/pull/400))
  - azure_rm_loadbalancer: check mode for loadbalancer ([#316](https://github.com/ansible-collections/azure/pull/316))
  - azure_rm_backupazurevm: Add function that azure_rm_backupazurevm resource in different resour… ([#404](https://github.com/ansible-collections/azure/pull/404))


## v1.3.1 (2020-12-17)

### BUG FIXING
  - CHANGELOG: Some corrections needed in links to get them to work ([#366](https://github.com/ansible-collections/azure/pull/366))
  - azure_rm: Retrieve computer_name using dictionary get method ([#368](https://github.com/ansible-collections/azure/pull/368))


## v1.3.0 (2020-12-16)

### NEW MODULES
  - azure_rm_vmbackuppolicy: Azure Recovery Services VM Backup Policy ([#271](https://github.com/ansible-collections/azure/pull/271))
  - azure_rm_vmbackuppolicy_info: Azure Recovery Services VM Backup Policy Info ([#271](https://github.com/ansible-collections/azure/pull/271))
  - azure_rm_subscription_info: Azure rm subscription info ([#280](https://github.com/ansible-collections/azure/pull/280))
  - azure_rm_privatednsrecordset: add new module for supporting DNS recordset operations in Private DNS zone ([#286](https://github.com/ansible-collections/azure/pull/286))
  - azure_rm_registrationassignment: Registration Assignment for Azure Lighthouse ([#359](https://github.com/ansible-collections/azure/pull/359))
  - azure_rm_registrationassignment_info: Registraion Assignment Info for Azure Lightouse ([#359](https://github.com/ansible-collections/azure/pull/359))
  - azure_rm_registrationdefinition: Registration Definition for Azure Lighthouse ([#359](https://github.com/ansible-collections/azure/pull/359))
  - azure_rm_registrationdefinition_info: Registration Definition Info for Azure Lighthouse ([#359](https://github.com/ansible-collections/azure/pull/359))

### FEATURE ENHANCEMENT
  - azure_rm_subnet: add delegations compatibility to azure_rm_subnet ([#264](https://github.com/ansible-collections/azure/pull/264))
  - azure_rm_loganalyticsworkspace: add force deletion capability to log analytics module ([#273](https://github.com/ansible-collections/azure/pull/273))
  - azure_rm_sqldatabase: add sku option for sqldatabase ([#291](https://github.com/ansible-collections/azure/pull/291))
  - azure_rm_aks: update azure_rm_aks document ([#294](https://github.com/ansible-collections/azure/pull/294))
  - azure_rm_manageddisk_info: add new parameter managed_by ([#302](https://github.com/ansible-collections/azure/pull/302))
  - Bump cryptography version from 3.0 to 3.2 ([#306](https://github.com/ansible-collections/azure/pull/306))
  - azure_rm_subnet: add example of service_endpoints configuration ([#309](https://github.com/ansible-collections/azure/pull/309))
  - azure_rm: add computer_name parameter to available variables ([#312](https://github.com/ansible-collections/azure/pull/312))
  - azure_rm_webapp: add support for multi-container apps to azure_rm_webapp ([#257](https://github.com/ansible-collections/azure/pull/257))
  - azure_rm_virtualmachineextension: add no_log to protected_settings variable ([#278](https://github.com/ansible-collections/azure/pull/278))

### BUG FIXING
  - azure_rm_keyvault: fix azure_rm_keyvault idempotency ([#295](https://github.com/ansible-collections/azure/pull/295))
  - azure_rm_roleassignment: fix azure_rm_roleassignment idempotence error ([#296](https://github.com/ansible-collections/azure/pull/296))
  - azure_rm_roleassignment: fix azure_rm_roleassignment related bugs ([#301](https://github.com/ansible-collections/azure/pull/301))
  - azure_rm_autoscale: fix typo ([#314](https://github.com/ansible-collections/azure/pull/314))
  - Fix sanity fail in python3.8 environment ([#355](https://github.com/ansible-collections/azure/pull/355))
  - azure_rm: extend doc fragment from base constructed class to fix error ([#364](https://github.com/ansible-collections/azure/pull/364))


## v1.2.0 (2020-10-09)

### NEW MODULES
  - azure_rm_backupazurevm:  ([#248](https://github.com/ansible-collections/azure/pull/248))
  - azure_rm_backupazurevm_info: ([#248](https://github.com/ansible-collections/azure/pull/248))
  - azure_rm_recoveryservicesvault: ([#254](https://github.com/ansible-collections/azure/pull/254))
  - azure_rm_openshiftmanagedcluster: ([#276](https://github.com/ansible-collections/azure/pull/276))

### FEATURE ENHANCEMENT
  - add python 3.8 support ([#246](https://github.com/ansible-collections/azure/pull/246))
  - azure_rm_publicipaddress: support public Ipv6 address ([#125](https://github.com/ansible-collections/azure/pull/125))
  - azure_rm_subnet: add private-endpoint-network-policies ([#256](https://github.com/ansible-collections/azure/pull/256))
  - azure_rm: fetch availability zone info into hostvars ([#243](https://github.com/ansible-collections/azure/pull/243))
  - azure_rm: make inventory_hostname configurable with hostvar_expressions ([#105](https://github.com/ansible-collections/azure/pull/105))

### BUG FIXING
  - azure_rm_openshiftmanagedcluster: fix issue [#270](https://github.com/ansible-collections/azure/issues/270) and [#269](https://github.com/ansible-collections/azure/issues/269)
            ([#285](https://github.com/ansible-collections/azure/pull/285))


## v1.1.0 (2020-09-03)

### FEATURE ENHANCEMENT
  - azure_rm_storageaccount: allow blob public access parameter ([#219](https://github.com/ansible-collections/azure/pull/219))
  - azure_rm_virtualmachine: update boot diganostics config ([#208](https://github.com/ansible-collections/azure/pull/208))
  - azure_rm_aks: add load_balancer_sku option ([#199](https://github.com/ansible-collections/azure/pull/199))
  - azure_rm: improve OS detection when VM has no osProfile ([#197](https://github.com/ansible-collections/azure/pull/197))
  - azure_rm_subnet: support IPv6 address ([#240](https://github.com/ansible-collections/azure/pull/240))
  - azure_rm_networkinterface: add new module parameter address_prefixes ([#239](https://github.com/ansible-collections/azure/pull/239))
  - azure_rm_common: support azure-cli credentials with multiple subscriptions ([#195](https://github.com/ansible-collections/azure/pull/195))
  - azure_rm_mariadbserver: support version 10.3 ([#244](https://github.com/ansible-collections/azure/pull/244))

### BUG FIXING
  - azure_rm_manageddisk: fix increments LUN on disks already attached error ([#237](https://github.com/ansible-collections/azure/pull/237))
  - azure_rm_appgateway: fix rule type reference error ([#99](https://github.com/ansible-collections/azure/pull/99))


## v1.0.0 (2020-08-12)

### FEATURE ENHANCEMENT
  - azure_rm_appgateway: support version 2 SKUS ([#198](https://github.com/ansible-collections/azure/pull/198))
  - azure_rm_storageaccount: support minimum tls version ([#207](https://github.com/ansible-collections/azure/pull/207))

### BUG FIXING
  - azure_rm_roledefinition: fails when `description` is set ([#214](https://github.com/ansible-collections/azure/pull/214))
  - azure_rm_virtualmachine: boot diagnostics related error ([#200](https://github.com/ansible-collections/azure/pull/200))


## v0.3.0 (2020-07-24)

### FEATURE ENHANCEMENT
  - azure_rm_storageblob: add batch upload feature ([#203](https://github.com/ansible-collections/azure/pull/203))

### BUG FIXING
  - azure_rm_deployment_info: getting the template_link when it does not exist ([#180](https://github.com/ansible-collections/azure/pull/180))
  - azure_rm_virtualmachine: protect against no diskSizeGB ([#185](https://github.com/ansible-collections/azure/pull/185))
  - azure_rm_deployment: misleading status code in module failure message ([#204](https://github.com/ansible-collections/azure/pull/204))
  - azure_rm_adserviceprincipal: invalid update check logic ([#205](https://github.com/ansible-collections/azure/pull/205))


## v0.2.0 (2020-07-03)

### NEW MODULES
  - azure_rm_privatezone module ([#122](https://github.com/ansible-collections/azure/pull/122))
  - azure_rm_adserviceprincipal module ([#179](https://github.com/ansible-collections/azure/pull/179))
  - azure_rm_adserviceprincipal_info module ([#179](https://github.com/ansible-collections/azure/pull/179))
  - azure_rm_adpassword module ([#179](https://github.com/ansible-collections/azure/pull/179))
  - azure_rm_adpassword_info module ([#179](https://github.com/ansible-collections/azure/pull/179))

### FEATURE ENHANCEMENT
  - add ability to remove all subnet service endpoints ([#148](https://github.com/ansible-collections/azure/pull/148))
  - update network client api version ([#157](https://github.com/ansible-collections/azure/pull/157))
  - add ephemeral os disk support for azure_rm_virualmachinescaleset ([#128](https://github.com/ansible-collections/azure/pull/128))
  - add ephemeral os disk support for azure_rm_virtualmachine ([#124](https://github.com/ansible-collections/azure/pull/124))
  - add FileEndpoint to azure_rm_storageaccount_info ([#102](https://github.com/ansible-collections/azure/pull/102))
  - add support for managing the 'Firewall and virtual networks' settings in azure_rm_storageaccount ([#108](https://github.com/ansible-collections/azure/pull/108))

### BUG FIXING
  - bug fixing in azure_rm_aks ([#170](https://github.com/ansible-collections/azure/pull/170))
  - migrate missing doc_fragments that went missing ([#115](https://github.com/ansible-collections/azure/pull/115))

## v0.1.3 (2020-05-13)

- add new parameter in azure_rm_aks
- fix retrun value docs in azure_rm_finctionapp and auzre_rm_functionapp_info 
- change README.md and update CHANGELOG.md 
- fix example in azure_rm_roledefinition_info
- add Icmp rule support in azure_rm_securitygroup
- add public_ip_per_vm parameter in azure_rm_virutalmachinescaleset
- add tags in azure_rm_galleryimageversion
- add sku type in azure_rm_virtualnetworkgateway
- add tags in azure_rm_containerregistry_info
- format azure_rm_managementgroup
- add new parameter in azure_rm_storageaccount 
- fixes accesss policy update in azure_rm_keyvault

## v0.1.2 (2020-03-19)

- migrate exisiting azure modules from ansible core

## v0.1.1 (2020-03-03)

- add module azure_rm_managementgroup

## v0.1.0 (2019-12-18)

- Add inventory plugin

## v0.0.2 (2019-11-15)

- Remove deprecated content
- Fix galaxy.yml

## v0.0.1 (2019-11-05)

- Init release

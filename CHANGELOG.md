# Change Log

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

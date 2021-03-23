# Change Log

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

# Change Log
## v3.10.0 (2025-10-30)

### NEW MODULES
  - extensions/eda/plugins/event_source/azure_event_hub.py: ([#2078](https://github.com/ansible-collections/azure/pull/2078))

### FEATURE ENHANCEMENT
  - azure_rm_aks.py: Add 'none' option to network_plugin for AKS module ([#2073](https://github.com/ansible-collections/azure/pull/2073))
  - azure_rm_subnet.py: Add support for "NetworkSecurityGroupEnabled" and "Rout eTableEnabled" in private_endpoint_network_policies ([#2080](https://github.com/ansible-collections/azure/pull/2080))
  - azure_rm_storageaccount: Add auth_mode to azure_rm_storageaccount ([#2079](https://github.com/ansible-collections/azure/pull/2079))
  - azure_keyvault_secret.py: Update lookup plugins to support ENV vars ([#2084](https://github.com/ansible-collections/azure/pull/2084))
  - azure_service_principal_attribute.py: Update lookup plugins to support ENV vars ([#2084](https://github.com/ansible-collections/azure/pull/2084))
  - requirements.txt: Re-generate requirments file ([#2087](https://github.com/ansible-collections/azure/pull/2087))

### BUG FIXING
  - README.md:
    - Update `SUPPORT` section in readme ([#2071](https://github.com/ansible-collections/azure/pull/2071))
    - Fix a type in README.md ([#2072](https://github.com/ansible-collections/azure/pull/2072))
  - azure_rm.py: Fix wrong conditional for vmss presence ([#2083](https://github.com/ansible-collections/azure/pull/2083))


## v3.9.0 (2025-09-29)

### NEW MODULES
  - azure_rm_monitordatacollectionendpoint.py:([#2058](https://github.com/ansible-collections/azure/pull/2058))
  - azure_rm_monitordatacollectionendpoint_info.py:([#2058](https://github.com/ansible-collections/azure/pull/2058))
  - azure_rm_monitordatacollectionruleassociation.py:([#2058](https://github.com/ansible-collections/azure/pull/2058))
  - azure_rm_monitordatacollectionruleassociation_info.py:([#2058](https://github.com/ansible-collections/azure/pull/2058))
  - azure_rm_serviceendpointpolicy.py: ([#2064](https://github.com/ansible-collections/azure/pull/2064))
  - azure_rm_serviceendpointpolicy_info.py: ([#2064](https://github.com/ansible-collections/azure/pull/2064))
  - azure_rm_serviceendpointpolicydefinitionfo.py: ([#2064](https://github.com/ansible-collections/azure/pull/2064))
  - azure_rm_serviceendpointpolicydefinition_info.py: ([#2064](https://github.com/ansible-collections/azure/pull/2064))

### FEATURE ENHANCEMENT
  - azure_rm_storageaccount.py: Add support for 'key_vault_properties' and 'encryption_identity' ([#2049](https://github.com/ansible-collections/azure/pull/2049))
  - azure_rm_storageaccount_info.py: Support return 'key_vault_properties' and 'encryption_identity' ([#2049](https://github.com/ansible-collections/azure/pull/2049))
  - pr-pipelines.yml: [Infra]: update ado yamls to use pool-ubuntu-2404 ([#2046](https://github.com/ansible-collections/azure/pull/2046))
  - azure_rm_virtualnetworkgateway.py: Add some SKU type options ([#2051](https://github.com/ansible-collections/azure/pull/2051))
  - plugins/inventory/azure_rm.py: Support gather virtual machine instance view info ([#2055](https://github.com/ansible-collections/azure/pull/2055))
  - azure_rm_publicipaddress.py: Add support for 'public_ip_prefix' ([#2059](https://github.com/ansible-collections/azure/pull/2059))
  - azure_rm_publicipaddress_info.py: Support return 'public_ip_prefix' ([#2059](https://github.com/ansible-collections/azure/pull/2059))
  - meta/extensions.yml: Update meta/extensions.yml to include eda path ([#2056](https://github.com/ansible-collections/azure/pull/2056))
  - azure_rm_subnet.py:
    - Add support for default_outbound_access ([#2062](https://github.com/ansible-collections/azure/pull/2062))
    - Add support for 'sharing_scopes' and 'service_endpoint_policies' ([#2064](https://github.com/ansible-collections/azure/pull/2064))
  - azure_rm_subnet_info.py:
    - Support return 'default_outbound_access' ([#2062](https://github.com/ansible-collections/azure/pull/2062))
    - Support return 'sharing_scopes' and 'service_endpoint_policies' ([#2064](https://github.com/ansible-collections/azure/pull/2064))

### BUG FIXING
  - azure_rm_securitygroup.py: Fix compare error where the returned ID is in uppercase ([#2048](https://github.com/ansible-collections/azure/pull/2048))
  - plugins/action/azure_rm_arcssh.py: Fix exception handling in azure_rm_arcssh ([#2053](https://github.com/ansible-collections/azure/pull/2053))
  - plugins/module_utils/azure_rm_common_rest.py: Distinguish Exception([#2053](https://github.com/ansible-collections/azure/pull/2053))


## v3.8.0 (2025-08-29)
### NEW MODULES
  - azure_rm_monitormetricalerts.py: ([#1952](https://github.com/ansible-collections/azure/pull/2016))
  - azure_rm_monitormetricalerts_info.py: ([#1952](https://github.com/ansible-collections/azure/pull/2016))
  - azure_rm_monitoractivitylogalerts.py: ([#1971](https://github.com/ansible-collections/azure/pull/1971))
  - azure_rm_monitoractivitylogalerts_info.py: ([#1971](https://github.com/ansible-collections/azure/pull/1971))
  - azure_rm_dedicatedhost.py: ([#1955](https://github.com/ansible-collections/azure/pull/1955))
  - azure_rm_dedicatedhost_info.py: ([#1955](https://github.com/ansible-collections/azure/pull/1955))

### FEATURE ENHANCEMENT
  - plugins/module_utils/azure_rm_common.py:
    - Set monitor management client for metric alert ([#1952](https://github.com/ansible-collections/azure/pull/2016))
    - Set monitor management client for activity log alert ([#1971](https://github.com/ansible-collections/azure/pull/1971))
    - Delete import get cli profile ([#2030](https://github.com/ansible-collections/azure/pull/2030))
    - Get 'subscription_id' when configuring the authentication parameter ([#2033](https://github.com/ansible-collections/azure/pull/2033))
    - Replacement will send raw.githubusercontent.com request method ([#2039](https://github.com/ansible-collections/azure/pull/2039))
  - plugins/module_utils/azure_rm_common_ext.py: Enhance default_compare ([1971](https://github.com/ansible-collections/azure/pull/1971))
  - azure_rm_aks.py: Add support addon's wqazureKeyvaultSecretsProvider ([#2026](https://github.com/ansible-collections/azure/pull/2026))
  - README.md: Update readme.md per https://access.redhat.com/articles/7068606 ([#2029](https://github.com/ansible-collections/azure/pull/2029))
  - azure_rm_azurefirewall.py: Add supportr 'destination_fqdns' ([#2031](https://github.com/ansible-collections/azure/pull/2031))
  - azure_rm_azurefirewall_info.py: Support return 'destination_fqdns' ([#2031](https://github.com/ansible-collections/azure/pull/2031))
  - requirements.txt: Update azure-cli-core to v2.75.0 ([#2032](https://github.com/ansible-collections/azure/pull/2032))
  - tests/utils/ado/ado.sh: Specify the ansible-lint version to v25.8.1 ([#2038](https://github.com/ansible-collections/azure/pull/2038))

### BUG FIXING
  - azure_rm_keyvaultcertificate.py: Convert the certificate data of type bytearray to base64 ([#1996](https://github.com/ansible-collections/azure/pull/1996))
  - azure_rm_galleryimageversion.py: Fix the keyword input error when assigning values to a dictionary ([#2037](https://github.com/ansible-collections/azure/pull/2037))
  - azure_rm_publicipaddress.py: Keep the check mode consistent with the print output ([#2043](https://github.com/ansible-collections/azure/pull/2043))


## v3.7.0 (2025-07-29)

### NEW MODULES
  - azure_rm_monitordatacollectionrules.py: ([#1952](https://github.com/ansible-collections/azure/pull/1952))
  - azure_rm_monitordatacollectionrules_info.py: ([#1952](https://github.com/ansible-collections/azure/pull/1952))
  - plugins/doc_fragments/azure_kql.py: ([#1944](https://github.com/ansible-collections/azure/pull/1994))
  - plugins/inventory/azure_kql.py: ([#1944](https://github.com/ansible-collections/azure/pull/1994))
  - azure_rm_monitoractiongroups.py: ([1964](https://github.com/ansible-collections/azure/pull/1964))
  - azure_rm_monitoractiongroups_info: ([1964](https://github.com/ansible-collections/azure/pull/1964))
  - extensions/eda/plugins/event_source/azure_service_bus.py: ([#1967](https://github.com/ansible-collections/azure/pull/1967))
  - extensions/eda/plugins/event_source/schemas/azure_service_bus.json: ([#1967](https://github.com/ansible-collections/azure/pull/1967))
  - azure_rm_containerregistryscopemap.py: ([#2019](https://github.com/ansible-collections/azure/pull/2019))
  - azure_rm_containerregistryscopemap_info.py: ([#2019](https://github.com/ansible-collections/azure/pull/2019))
  - azure_rm_containerregistrytoken.py: ([#2023](https://github.com/ansible-collections/azure/pull/2023))
  - azure_rm_containerregistrytoken_info.py: ([#2023](https://github.com/ansible-collections/azure/pull/2023))
  - azure_rm_containerregistrytokenpassword.py: ([#2023](https://github.com/ansible-collections/azure/pull/2023))

### FEATURE ENHANCEMENT
  - plugins/module_utils/azure_rm_common.py:
    - Add the constraint of requied_by and set monitor client for data collection rule ([1952](https://github.com/ansible-collections/azure/pull/1952))
    - Set monitor client for action groups ([1964](https://github.com/ansible-collections/azure/pull/1964))
    - Set container registry client for scope map: ([#2019](https://github.com/ansible-collections/azure/pull/2019))
    - Set container registry client for token: ([#2023](https://github.com/ansible-collections/azure/pull/2023))
  - azure_rm_loadbalancer: Support to append sub-properties instead of overwriting ([#1969](https://github.com/ansible-collections/azure/pull/1969))
  - azure_rm_virtualmachinescaleset.py: Support Priority Type Regular on azure_rm_virtualmachinescaleset Module ([#2001](https://github.com/ansible-collections/azure/pull/2001))
  - azure_rm_privatednszonelink.py: Add support for 'resolution_policy' ([#1962](https://github.com/ansible-collections/azure/pull/1962))
  - azure_rm_privatednszonelink_info.py: Support return 'resolution_policy' ([#1962](https://github.com/ansible-collections/azure/pull/1962))
  - azure_rm_subnet.py: Add support for Microsoft.App/environments in subnet delegations ([#2007](https://github.com/ansible-collections/azure/pull/2007))
  - tests/unit/event_source/test_azure_service_bus.py: Add async functionality ([#2017](https://github.com/ansible-collections/azure/pull/2017))
  - textensions/eda/plugins/event_source/azure_service_bus.py: Add async functionality ([#2017](https://github.com/ansible-collections/azure/pull/2017))
  - pr-pipeline.yml: Delete the creation of resource groups that are not needed ([#2014](https://github.com/ansible-collections/azure/pull/2014))
  - azure_rm_sqlmanagedinstance.py: Add waiting processing LROPoller results ([#2018](https://github.com/ansible-collections/azure/pull/2018))
  - azure_rm_virtualwan.py: Add waiting processing LROPoller results ([#2021](https://github.com/ansible-collections/azure/pull/2021))
  - azure_rm_virtualhubconnection.py: Add waiting processing LROPoller results ([#2022](https://github.com/ansible-collections/azure/pull/2022))
  - azure_rm_virtualhub.py: Add waiting processing LROPoller results ([#2020](https://github.com/ansible-collections/azure/pull/2020))

### BUG FIXING
  - plugins/module_utils/security_domain_utils.py: Add future import and metaclass boilerplate ([#1987](https://github.com/ansible-collections/azure/pull/1987))
  - plugins/modules/azure_rm_keyvaultsecret_info.py: Fix the handling error that get disabled secret ([#1992](https://github.com/ansible-collections/azure/pull/1992))
  - azure_rm_virtualmachine.py: Used required_by instead of required_if ([#1998](https://github.com/ansible-collections/azure/pull/1998))
  - azure_rm_virtualnetwork.py: Used required_by instead of required_if ([#1998](https://github.com/ansible-collections/azure/pull/1998))


## v3.6.0 (2025-06-30)

### NEW MODULES
  - azure_rm_virtualnetworkgateway_info.py: ([#1966](https://github.com/ansible-collections/azure/pull/1966))
  - azure_rm_tag.py: ([#1943](https://github.com/ansible-collections/azure/pull/1943))
  - azure_rm_tag_info.py: ([#1943](https://github.com/ansible-collections/azure/pull/1943))
  - azure_rm_postgresqlflexiblebackup.py: ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_postgresqlflexiblebackup_info.py: ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_postgresqlflexiblevirtualendpoint.py: ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_postgresqlflexiblevirtualendpoint_info.py: ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_postgresqlflexibleadministrator.py: ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_postgresqlflexibleadministrator_info.py: ([1914](https://github.com/ansible-collections/azure/pull/1914))

### FEATURE ENHANCEMENT
  - ad.sh: Cleanup ado.sh ([#1972](https://github.com/ansible-collections/azure/pull/1972))
  - pr-pipeline.yml:
    - Set default for pr-pipeline to latest versions (python+ansible) ([#1972](https://github.com/ansible-collections/azure/pull/1972))
    - Restore the trigger that synchronizes the dev branch during the PR test ([#1978](https://github.com/ansible-collections/azure/pull/1978))
  - azure_rm_virtualnetworkgatewayconnection_info.py: Support return 'local_network_gateway2' ([#1958](https://github.com/ansible-collections/azure/pull/1958))
  - azure_rm_loadbalancer.py: Add support for 'outbound_rules' ([#1965](https://github.com/ansible-collections/azure/pull/1965))
  - azure_rm_loadbalancer_info.py: Support return 'outbound_rules' ([#1965](https://github.com/ansible-collections/azure/pull/1965))
  - azure_rm_keyvault.py: New function to purge the deleted vaults ([#1981](https://github.com/ansible-collections/azure/pull/1981))
  - azure_rm_postgresqlflexibleserver.py: Add support for 'auth_config' ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_postgresqlflexibleserver_info.py: Support return 'auth_config' ([1914](https://github.com/ansible-collections/azure/pull/1914))
  - azure_rm_manageddisk_info.py: Support return 'last_ownership_update_time' ([#1984](https://github.com/ansible-collections/azure/pull/1984))

### BUG FIXING
  - azure_rm_managementgroup_info.py: Fix the error of devel branch ansible detecting invalid document ([#1975](https://github.com/ansible-collections/azure/pull/1975))
  - azure_rm_virtualnetworkgatewayconnection.py: Fix the bug that IPSec type connection not work ([#1958](https://github.com/ansible-collections/azure/pull/1958))
  - azure_rm_loganalyticsworkspace_info.py: Fix the function reference error ([#1983](https://github.com/ansible-collections/azure/pull/1983))


## v3.5.0 (2025-06-18)

### NEW MODULES
  - security_domain_utils: ([#1717](https://github.com/ansible-collections/azure/pull/1717))
  - azure_rm_keyvaultsecuritydomain: ([#1717](https://github.com/ansible-collections/azure/pull/1717))

### FEATURE ENHANCEMENT
  - Integration tests:
    - Separate the VM test into different region ([#1951](https://github.com/ansible-collections/azure/pull/1951))
    - Update test cases to work under ansible-2.19 Group2 ([#1953](https://github.com/ansible-collections/azure/pull/1953))
  - azure_rm_keyvault: Add support for `hsm_name`, `administrators` and `identity` ([#1717](https://github.com/ansible-collections/azure/pull/1717))
  - azure_rm_keyvault_info: Add support for `hsm_name`, `administrators` and `identity` ([#1717](https://github.com/ansible-collections/azure/pull/1717))
  - Remove deprecated code since ansible-2.9 has been EOL [1949](https://github.com/ansible-collections/azure/pull/1949)
  - pr-pipelines.yml: Add python `v3.12` and `v3.13` to CI pipeline ([#1954](https://github.com/ansible-collections/azure/pull/1954))
  - requirements.txt: Bump `azure-cli-core` to `v2.74.0`  ([#1956](https://github.com/ansible-collections/azure/pull/1956))
  - sanity-requirements.txt: Bump sanity test dependency ([#1956](https://github.com/ansible-collections/azure/pull/1956))

### BUG FIXING
  - azure_rm_resource_info: Fix failure on response with bytes body ([#1957](https://github.com/ansible-collections/azure/pull/1957))

## v3.4.0 (2025-05-29)

### NEW MODULES
  - azure_rm_afdroute: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdroute_info: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdorigingroup: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdorigingroup_info: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdorigin: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdorigin_info: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdruleset: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdruleset_info: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdrules: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - azure_rm_afdrules_info: ([#1885](https://github.com/ansible-collections/azure/pull/1885))
  - extensions/audit/event_query.yml: This event_query file is used by Ansible Automation Platform. It allows for the tracking of resources in cloud providers. ([#1922](https://github.com/ansible-collections/azure/pull/1922))
  - azure_rm_recoveryservicesvaultconfig: ([#1926](https://github.com/ansible-collections/azure/pull/1926))
  - azure_rm_recoveryservicesvaultconfig_info: ([#1926](https://github.com/ansible-collections/azure/pull/1926))
  - azure_rm_keyvaultcertificate: ([#1806](https://github.com/ansible-collections/azure/pull/1806))
  - azure_rm_keyvaultcertificate_info: ([#1806](https://github.com/ansible-collections/azure/pull/1806))

### FEATURE ENHANCEMENT
  - azure_rm_keyvaultsecret_info: Optimize the return value ([#1851](https://github.com/ansible-collections/azure/pull/1851))
  - azure_rm_galleryimageversion: Set the timeout for creating an image version ([#1848](https://github.com/ansible-collections/azure/pull/1848))
  - azure_rm_adapplication: Add support for `notes` ([#1852](https://github.com/ansible-collections/azure/pull/1852))
  - azure_rm_adapplication_info: Add support for `notes` ([#1852](https://github.com/ansible-collections/azure/pull/1852))
  - azure_rm_virtualmachine:
    - Add support for datadisk `name` ([#1847](https://github.com/ansible-collections/azure/pull/1847))
    - Add support for `shared_gallery_image_id` ([#1883](https://github.com/ansible-collections/azure/pull/1883))
  - azure_rm_aks: Compatible with `os_type` case sensitivity ([#1879](https://github.com/ansible-collections/azure/pull/1879))
  - azure_rm_image: Add support for `os_disk_encryption_set` and `data_disk_encryption_set` ([#1891](https://github.com/ansible-collections/azure/pull/1891))
  - azure_rm_image_info: Add support for `os_disk_encryption_set` and `data_disk_encryption_set` ([#1891](https://github.com/ansible-collections/azure/pull/1891))
  - azure_rm_virtualmachinescaleset:
    - Add support for `os_disk_encryption_set` ([#1892](https://github.com/ansible-collections/azure/pull/1892))
    - Add support for `application_security_groups` and `private_ip_address_version` ([#1910](https://github.com/ansible-collections/azure/pull/1910))
  - azure_rm_virtualmachinescaleset_info: Add support for `application_security_groups` and `private_ip_address_version` ([#1910](https://github.com/ansible-collections/azure/pull/1910))
  - azure_rm_backuppolicy: Add support for `policy_type` ([#1887](https://github.com/ansible-collections/azure/pull/1887))
  - plugins/module_utils/azure_rm_common:
    - Upgrade azure_rm_galleryimageverison dependency api version to `v2023-07-03` ([#1845](https://github.com/ansible-collections/azure/pull/1845))
    - Migrate postgresql flexible relate SDK to `azure-mgmt-postgresqlflexibleservers` ([#1876](https://github.com/ansible-collections/azure/pull/1876))
    - Support alternative MSGraph cloud endpoints ([#1912](https://github.com/ansible-collections/azure/pull/1912))
    - Migrate mysql flexible relate SDK to `azure-mgmt-mysqlflexibleservers` ([#1906](https://github.com/ansible-collections/azure/pull/1906))
  - azure_rm_adserviceprincipal: Add support for `notes`, `account_enabled` and `service_principal_type` ([1902](https://github.com/ansible-collections/azure/pull/1902))
  - azure_rm_adserviceprincipal_info: Support return `notes`, `account_enabled` and `service_principal_type` ([1902](https://github.com/ansible-collections/azure/pull/1902))
  - plugins/inventory/azure_rm: 
    - Upgrade Compute API version to `v2024-07-01` ([#1918](https://github.com/ansible-collections/azure/pull/1918))
    - Upgrade Network API version to `v2024-05-01` ([#1918](https://github.com/ansible-collections/azure/pull/1918))
  - azure_rm_aksagentpool: Add support for `os_disk_type`, `capacity_reservation_group_id`, `host_group_id` etc.   ([#1913](https://github.com/ansible-collections/azure/pull/1913))
  - azure_rm_aksagentpool_info: Add support for `os_disk_type`, `capacity_reservation_group_id`, `host_group_id` etc.([#1913](https://github.com/ansible-collections/azure/pull/1913))
  - Integration tests:
    - Add a test case for `azure_rm_manageddisk` ([#1866](https://github.com/ansible-collections/azure/pull/1866))
    - Add idempotency test for `azure_rm_backuppolicy` ([#1889](https://github.com/ansible-collections/azure/pull/1889))
    - Add test for keeping public IPs on `azure_rm_networkinterface` updates ([#1917](https://github.com/ansible-collections/azure/pull/1917))
    - Update test cases to work under ansible-2.19 Group1 ([#1940](https://github.com/ansible-collections/azure/pull/1940))
    - Update test cases to work under ansible-2.19 Group7 ([#1941](https://github.com/ansible-collections/azure/pull/1941))
    - Update test cases to work under ansible-2.19 Group9 ([#1942](https://github.com/ansible-collections/azure/pull/1942))
    - Show failure of idempotency in integration tests for `azure_rm_roleassignment` ([#1864](https://github.com/ansible-collections/azure/pull/1864))
    - Update pipeline test ([#1893]( https://github.com/ansible-collections/azure/pull/1893))
    - Move VM-related tests to group1 ([#1924]( https://github.com/ansible-collections/azure/pull/1924))

### BUG FIXING
  - azure_rm_manageddisk: Gets the image return value during idempotent testing ([#1860](https://github.com/ansible-collections/azure/pull/1860))
  - azure_rm_roleassignment: Ignore case when comparing strings ([#1869](https://github.com/ansible-collections/azure/pull/1869))
  - azure_rm_servicebus: Update `premium_messaging_partitions` settings ([#1871](https://github.com/ansible-collections/azure/pull/1871))
  - azure_rm_publicipaddress: Delete sku type `basic` ([#1877](https://github.com/ansible-collections/azure/pull/1877))
  - plugins/inventory/azure_rm: Decrease the timeout period ([#1878](https://github.com/ansible-collections/azure/pull/1878))
  - azure_rm_networkinterface:
    - Fix tags cannot be updated ([#1881](https://github.com/ansible-collections/azure/pull/1881))
    - Fix the bug of public ip loss ([#1921](https://github.com/ansible-collections/azure/pull/1921))
  - azure_rm_adserviceprincipal: Fix `app_role_assignment_required` not set bug ([#1861](https://github.com/ansible-collections/azure/pull/1861))
  - azure_rm_backuppolicy: Fix the idempotent issue ([#1890](https://github.com/ansible-collections/azure/pull/1890))
  - azure_rm_virtualmachine: Fix the bug of getting disk name ([#1845](https://github.com/ansible-collections/azure/pull/1845))
  - azure_rm_recoveryservicesvault: Fix idempotent fail ([#1908](https://github.com/ansible-collections/azure/pull/1908)
  - azure_rm_virtualnetworkpeering: Support virtual networks cross subscription ([#1909](https://github.com/ansible-collections/azure/pull/1909))
  - azure_rm_privateendpoint_info: Fix the error in the document description ([#1933](https://github.com/ansible-collections/azure/pull/1933))
  - azure_rm_virtualmachine_info: Correct spelling for VM info property identity ([#1936](https://github.com/ansible-collections/azure/pull/1936))
  - azure_rm_networkflowlog: Fix the bug of location was not set to the default resource group of location ([#1939](https://github.com/ansible-collections/azure/pull/1939))
  - azure_rm_automationaccount_info: Fix documentation error ([#1928](https://github.com/ansible-collections/azure/pull/1928))
  - azure_rm_gallery: Fix `description` setting bug ([#1935](https://github.com/ansible-collections/azure/pull/1935))
  - azure_rm_gallery_info: Fix `description` setting bug ([#1935](https://github.com/ansible-collections/azure/pull/1935))


## v3.3.1 (2025-03-13)

### Fix compile issue with python v3.6

## v3.3.0 (2025-03-12)

### NEW MODULES
  - azure_rm_diskaccess: ([#1831](https://github.com/ansible-collections/azure/pull/1831))
  - azure_rm_diskaccess_info: ([#1831](https://github.com/ansible-collections/azure/pull/1831))
  - azure_rm_resourcehealthstates_info: ([#1838](https://github.com/ansible-collections/azure/pull/1838))

### FEATURE ENHANCEMENT
  - README.md:
    - Add pipx alternative for deps installation ([#1797](https://github.com/ansible-collections/azure/pull/1797))
    - Update README.md: ([#1832](https://github.com/ansible-collections/azure/pull/1832))
  - azure_rm_storageaccount: Add support for `immutable_storage_with_versioning` ([#1802](https://github.com/ansible-collections/azure/pull/1802))
  - azure_rm_storageaccount_info: Support return `immutable_storage_with_versioning` ([#1802](https://github.com/ansible-collections/azure/pull/1802))
  - azure_rm_trafficmanagerprofile: Add support for `custom_header`, `expected_status_code_ranges`, `max_return` and `allowed_endpoint_record_types` ([#1800](https://github.com/ansible-collections/azure/pull/1800))
  - azure_rm_trafficmanagerprofile_info: Support return `custom_header`, `expected_status_code_ranges`, `max_return` and `allowed_endpoint_record_types` ([#1800](https://github.com/ansible-collections/azure/pull/1800))
  - azure_rm_virtualmachine:
    - Allow creation from snapshot image ([#1816](https://github.com/ansible-collections/azure/pull/1816))
    - Add support `user_data` ([#1844](https://github.com/ansible-collections/azure/pull/1844))
  - azure_rm_virtualmachine_info:
    - Support return `storage_profile.os_disk` ([#1816](https://github.com/ansible-collections/azure/pull/1816))
    - Support return `write_accelerator_enabled` ([#1808](https://github.com/ansible-collections/azure/pull/1808))
    - support return `maintenance_redeploy_status` ([#1822](https://github.com/ansible-collections/azure/pull/1822))
  - azure_rm_manageddisk:
    - Add support for `write_accelerator_enabled` ([#1808](https://github.com/ansible-collections/azure/pull/1808))
    - Add `upload`, `fromimage`, `restore`, `uploadpreparedsecure`  to `create_option` and add support for `performance_plus`, `upload_size_bytes`, `gallery_image_reference`, `image_reference`, `logical_sector_size`, `source_resource_id`, `security_profile` ([#1833](https://github.com/ansible-collections/azure/pull/1833))
  - azure_rm_manageddisk_info: Support return `performance_plus`, `upload_size_bytes`, `gallery_image_reference`, `image_reference`, `logical_sector_size`, `source_resource_id`, `security_profile` ([#1833](https://github.com/ansible-collections/azure/pull/1833))
  - azure_rm.py: Add cache support to inventory plugin cache ([#1828](https://github.com/ansible-collections/azure/pull/1828))
  - azure_keyvault_secret: Add support for `use_cli`, use CLI credential ([#1836](https://github.com/ansible-collections/azure/pull/1836))

### BUG FIXING
  - tests/integration/targets/azure_rm_dnsrecordset/tasks/main.yml: Update the random value ([#1803](https://github.com/ansible-collections/azure/pull/1803))
  - azure_rm_roleassignment: Delete scope tail `/` when comparing scopes ([#1807](https://github.com/ansible-collections/azure/pull/1807))
  - azure_rm_subnet_info: Fix incorrect API call ([#1826](https://github.com/ansible-collections/azure/pull/1826))
  - azure_rm_virtualmachine_info: Fix the bug that `capacity_reservation_group` not being handled ([#1827](https://github.com/ansible-collections/azure/pull/1827))
  - azure_rm_aks: Fixed the bug that `agent_pool.security_profile` returning `None` ([#1835](https://github.com/ansible-collections/azure/pull/1835))
  - azure_rm_servicebus: Do not compare the `zone_redundant` return value during idempotency testing ([#1840](https://github.com/ansible-collections/azure/pull/1840))
  - azure_rm_subnet: Fixed the bug caused by the user defining `subscription_id` in `route_table` ([#1837](https://github.com/ansible-collections/azure/pull/1837))


## v3.2.0 (2025-02-06)

### NEW MODULES
  - azure_rm_applicationfirewallpolicy: ([#1783](https://github.com/ansible-collections/azure/pull/1783))
  - azure_rm_applicationfirewallpolicy_info: ([#1783](https://github.com/ansible-collections/azure/pull/1783))
  - azure_rm_arcssh: Builds on HCI inventory and adds ARC support as well ([#1735](https://github.com/ansible-collections/azure/pull/1735))

### FEATURE ENHANCEMENT
  - azure_rm_dnsrecordset: Add support for `target_resource` ([#1767](https://github.com/ansible-collections/azure/pull/1767))
  - azure_rm_dnsrecordset_info: Support return `target_resource` ([#1767](https://github.com/ansible-collections/azure/pull/1767))
  - azure_rm_loadbalancer: Add support for `enable_tcp_reset` to `load_balancing_rules` ([#1774](https://github.com/ansible-collections/azure/pull/1774))
  - azure_rm_privateendpoint: Add support for `application_security_groups`, `custom_dns_configs`,`custom_network_interface_name`, `ip_configurations` ([#1771](https://github.com/ansible-collections/azure/pull/1771))
  - azure_rm_privateendpoint_info: Add support for `application_security_groups`, `custom_dns_configs`,`custom_network_interface_name`, `ip_configurations` ([#1771](https://github.com/ansible-collections/azure/pull/1771))
  - azure_rm_manageddisk:
    - Add support for `public_network_access` and `network_access_policy` ([#1782](https://github.com/ansible-collections/azure/pull/1782))
    - Add support for display/modification of disk performance `tier` ([#1787](https://github.com/ansible-collections/azure/pull/1787))
  - azure_rm_manageddisk_info:
    - Support return `public_network_access` and `network_access_policy` ([#1782](https://github.com/ansible-collections/azure/pull/1782))
    - Support return `tier` ([#1787](https://github.com/ansible-collections/azure/pull/1787))
  - azure_rm_iotdevice: Add support for `device_scope` ([#1790](https://github.com/ansible-collections/azure/pull/1790))
  - azure_rm_cdnprofile: Add more `sku` selection options ([#1789](https://github.com/ansible-collections/azure/pull/1789))
  - azure_rm_webapp: Add support for updating `startup_file` ([#1792](https://github.com/ansible-collections/azure/pull/1792))
  - azure_rm_appgateway: Add support for setting WAF policy ([#1725](https://github.com/ansible-collections/azure/pull/1725))
  - azure_rm_servicebus: Add support for `minimum_tls_version`, `zone_redundant`, `disable_local_auth`, `public_network_access` and `premium_messaging_partitions` ([#1793](https://github.com/ansible-collections/azure/pull/1793))
  - plugins/inventory/azure_rm.py: Add support for `batch_fetch_interval` and `batch_fetch_timeout` ([#1804](https://github.com/ansible-collections/azure/pull/1804))
  - azure_rm_aduser_info: Add support for `surname` and `given_name` ([#1815](https://github.com/ansible-collections/azure/pull/1815))
  - azure_rm_keyvaultsecret - Remove unnecessary constraints ([#1810](https://github.com/ansible-collections/azure/pull/1810))

### BUG FIXING
  - inventory azure_rm: Return the VM NIC details ([#1770](https://github.com/ansible-collections/azure/pull/1770))
  - azure_keyvault_secret: Include Key Vault URL to error messages ([#1785](https://github.com/ansible-collections/azure/pull/1785))


## v3.1.0 (2024-12-02)

### NEW MODULES
  - azure_rm_batchaccountapplication:  ([#1753](https://github.com/ansible-collections/azure/pull/1753))
  - azure_rm_batchaccountapplication_info: ([#1753](https://github.com/ansible-collections/azure/pull/1753))
  - azure_rm_batchaccountpool: ([#1753](https://github.com/ansible-collections/azure/pull/1753))
  - azure_rm_batchaccountpool_info: ([#1753](https://github.com/ansible-collections/azure/pull/1753))
  - azure_rm_batchaccountapplicationpackage: ([#1753](https://github.com/ansible-collections/azure/pull/1753))
  - azure_rm_batchaccountapplicationpackage_info: ([#1753](https://github.com/ansible-collections/azure/pull/1753))

### FEATURE ENHANCEMENT
  - azure_rm_storageblob: Add support for `standard_blob_tier` ([#1764](https://github.com/ansible-collections/azure/pull/1764))
  - azure_rm_keyvault:
    - Add support for `enable_rbac_authorization` ([#1737](https://github.com/ansible-collections/azure/pull/1737))
    - Add support for `netowrk_acls` ([#1738](https://github.com/ansible-collections/azure/pull/1738))
  - azure_rm_keyvault_info:
    - Add support for `enable_rbac_authorization` ([#1737](https://github.com/ansible-collections/azure/pull/1737))
    - Add support for `netowrk_acls` ([#1738](https://github.com/ansible-collections/azure/pull/1738))
  - azure_rm_devtestlabvirtualmachine: Add support for `is_authentication_with_ssh_key` ([#1736](https://github.com/ansible-collections/azure/pull/1736))
  - azure_rm_devtestlabvirtualmachine_info: Add support for `is_authentication_with_ssh_key` ([#1736](https://github.com/ansible-collections/azure/pull/1736))
  - azure_rm_aks: Add support for `windows_profile` ([#1740](https://github.com/ansible-collections/azure/pull/1740))
  - azure_rm_aksagentpool: Add `AzureLinux`, `Windows2019` and `Windows2022` to `os_sku` ([#1740](https://github.com/ansible-collections/azure/pull/1740))
  - azure_rm_autoscale: Add support for `metric_namespace` ([#1743](https://github.com/ansible-collections/azure/pull/1743))
  - azure_rm_autoscale_info: Add support for `metric_namespace` ([#1743](https://github.com/ansible-collections/azure/pull/1743))
  - azure_rm_privateendpoint: Add support for `manual_private_link_service_connections` ([#1745](https://github.com/ansible-collections/azure/pull/1745))
  - azure_rm_privateendpoint_info: Add support for `manual_private_link_service_connections` ([#1745](https://github.com/ansible-collections/azure/pull/1745))
  - azure_rm_iothub: Rename `container` to `container_name` ([#1763](https://github.com/ansible-collections/azure/pull/1763))
  - azure_rm_virtualmachine: Add support for `community_gallery_image_id` ([#1759](https://github.com/ansible-collections/azure/pull/1759))
  - azure_rm_virtualmachine_info: Add support for `community_gallery_image_id` ([#1759](https://github.com/ansible-collections/azure/pull/1759))
  - azure_rm_virtualmachinescaleset: Add support for `community_gallery_image_id` ([#1759](https://github.com/ansible-collections/azure/pull/1759))
  - azure_rm_virtualmachinescaleset_info: Add support for `community_gallery_image_id` ([#1759](https://github.com/ansible-collections/azure/pull/1759))
  - requirements.txt:
    - Update the SDK that relies on msrest and msrestazure to the latest version ([#1755](https://github.com/ansible-collections/azure/pull/1755))
    - Upgrade azure-mgmt-network to v28.0.0 ([#1769](https://github.com/ansible-collections/azure/pull/1769))
  - README.md: Bump ansible to `v2.16` ([#1758](https://github.com/ansible-collections/azure/pull/1758))

### BUG FIXING
  - azure_rm_manageddisk: Fixes bug caused by SDK upgrade([ #1756](https://github.com/ansible-collections/azure/pull/1756))
  - azure_rm.py: Fix Flexible VMSS issue and add support for setting environment variable `ANSIBLE_AZURE_VMSS_RESOURCE_GROUPS` ([#1752](https://github.com/ansible-collections/azure/pull/1752))
  - azure_rm_keyvaultsecret: Fix lint issue ([#1758](https://github.com/ansible-collections/azure/pull/1758))

### BREAKING CHANGE
  - azure_rm_adapplication: Deprecate `available_to_other_tenants` ([#1754](https://github.com/ansible-collections/azure/pull/1754))
  - azure_rm_adapplication_info: Deprecate `available_to_other_tenants` ([#1754](https://github.com/ansible-collections/azure/pull/1754))

## v3.0.0 (2024-10-31)

### NEW MODULES
  - azure_rm_virtualnetworkgatewayconnection: Support to managed virtual network gateway connection's resource ([#1627](https://github.com/ansible-collections/azure/pull/1627))
  - azure_rm_virtualnetworkgatewayconnection_info: Support to fetch the virtual network gateway connection resource ([#1627](https://github.com/ansible-collections/azure/pull/1627))
  - azure_rm_mysqlflexibleserver: Support managed flexible server ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexibleserver_info: Support to fetch managed flexible server ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexibleconfiguration: Support managed flexible server configuration ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexibleconfiguration_info: Support to fetch managed flexible server configuration ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexibledatabase: Support managed flexible server database ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexibledatabase_info: Support to fetch flexible server database ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexiblefirewallrule: Support managed flexible server firewall rule ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_rm_mysqlflexiblefirewallrule_info: Support to fetch flexible server firewall rule ([#1586](https://github.com/ansible-collections/azure/pull/1586))
  - azure_identity_multiple_user: Managed identity cleanup ([#1724](https://github.com/ansible-collections/azure/pull/1724))
  - azure_identity_single: Managed identity cleanup ([#1724](https://github.com/ansible-collections/azure/pull/1724))
  - azure_rm_imagesku_info: VM Image SKUs support in Ansible collection for Azure module creation ([#1719](https://github.com/ansible-collections/azure/pull/1719))

### FEATURE ENHANCEMENT
  - azure_rm_eventhub: Add support for managed identity ([#1696](https://github.com/ansible-collections/azure/pull/1696))
  - test case:
    - Use the password plug-in to generate a login key ([#1699](https://github.com/ansible-collections/azure/pull/1699))
    - Set the value of open port ([#1704](https://github.com/ansible-collections/azure/pull/1704))
    - Update `azure_rm_sqlelasticpool` test case ([#1714](https://github.com/ansible-collections/azure/pull/1714))
  - azure_rm_openshiftmanagedcluster: Add support `outbound_type` ([#1664](https://github.com/ansible-collections/azure/pull/1664))
  - requirements.txt:
    - Upgrade `azure-mgmt-containerinstance` to `v10.1.0` ([#1709](https://github.com/ansible-collections/azure/pull/1709))
    - Upgrade `azure-mgmt-containerregistry` to `v10.3.0` ([#1709](https://github.com/ansible-collections/azure/pull/1709))
    - Upgrade `azure-containerregistry` to `v1.2.0` ([#1709](https://github.com/ansible-collections/azure/pull/1709))
    - Upgrade `azure-mgmt-sql` to `v4.0.0b19` ([#1709](https://github.com/ansible-collections/azure/pull/1709))
    - Upgrade `azure-mgmt-cosmosdb` to `v10.0.0b3` ([#1709](https://github.com/ansible-collections/azure/pull/1709))
    - Upgrade `azure-mgmt-compute` to `v33.0.0` ([#1700](https://github.com/ansible-collections/azure/pull/1700))
    - Upgrade `azure-mgmt-network` to `v26.0.0` ([#1697](https://github.com/ansible-collections/azure/pull/1697))
    - Upgrade `cryptography` from `v42.0.4` to `v43.0.1` ([#1702](https://github.com/ansible-collections/azure/pull/1702))
    - Upgrade `azure-mgmt-notificationhubs` to `v` ([#1706](https://github.com/ansible-collections/azure/pull/1706))
    - Upgrade `azure-mgmt-eventhub` to `v11.1.0` ([#1706](https://github.com/ansible-collections/azure/pull/1706))
    - Update some dependency packages ([#1703](https://github.com/ansible-collections/azure/pull/1703))
    - Update some dependency packages ([#1707](https://github.com/ansible-collections/azure/pull/1707))
    - Update all packages to the latest version ([#1712](https://github.com/ansible-collections/azure/pull/1712))
    - Upgrade `azure-mgmt-notificationhub` api version `v2023-09-01` ([#1723](https://github.com/ansible-collections/azure/pull/1723))
    - Upgrade `azure-mgmt-recoveryservicesbackup` to `v9.1.0` ([#1733](https://github.com/ansible-collections/azure/pull/1733))
    - Update `azure-identity` to `v1.19.0` ([#1746](https://github.com/ansible-collections/azure/pull/1746))
    - Update `azure-core` to `v1.31.0` ([#1746](https://github.com/ansible-collections/azure/pull/1746))
  - azure_rm_loganalyticsworkspace: Add support for identity Management ([#1683](https://github.com/ansible-collections/azure/pull/1683))
  - azure_rm_hdinsightcluster: Add support for identity Management ([#1695](https://github.com/ansible-collections/azure/pull/1695))
  - azure_rm_hdinsightcluster_info: Add support for identity Management ([#1695](https://github.com/ansible-collections/azure/pull/1695))
  - azure_aksagentpool: Add support for `tags` ([#1718](https://github.com/ansible-collections/azure/pull/1718))
  - azure_aksagentpool_info: Add support for `tags` ([#1718](https://github.com/ansible-collections/azure/pull/1718))
  - azure_rm_publicipaddress: Add support for `reverse_fqdn` ([#1660](https://github.com/ansible-collections/azure/pull/1660))
  - azure_rm_snapshot_info: Add support for list snapshot instance ([#1659](https://github.com/ansible-collections/azure/pull/1659))
  - azure_rm_sqlmanagedinstance:  Add support for identity Management ([#1633](https://github.com/ansible-collections/azure/pull/1633))
  - azure_rm: Add support for Azure StackHCI vms in the inventory plugin ([#1620](https://github.com/ansible-collections/azure/pull/1620))
  - azure_rm_manageddisk: Add support for `disk_iops_read_write`, `disk_m_bps_read_write`, `disk_iops_read_only`, `disk_m_bps_read_only` ([#1741](https://github.com/ansible-collections/azure/pull/1741))
  - azure_rm_manageddisk_info: Add support for `disk_iops_read_write`, `disk_m_bps_read_write`, `disk_iops_read_only`, `disk_m_bps_read_only` ([#1741](https://github.com/ansible-collections/azure/pull/1741))
  - azure_rm_virtualmachine_info: Add support for getting identity ([#1674](https://github.com/ansible-collections/azure/pull/1674))
  - Add custom user-agent to http header ([#1747](https://github.com/ansible-collections/azure/pull/1747))

### BUG FIXING
  - azure_rm_networkinterface: Fixes errors for application security groups under different subscription ids ([#1711](https://github.com/ansible-collections/azure/pull/1711))
  - azure_rm_common: Get `subscription` instead of `subscription_id` ([#1720](https://github.com/ansible-collections/azure/pull/1720))
  - azure_rm_image: Get `subscription` instead of `subscription_id` ([#1720](https://github.com/ansible-collections/azure/pull/1720))
  - meta/runtime.yml: Keeping action_groups and modules list on version `v2.7.0` ([#1694](https://github.com/ansible-collections/azure/pull/1694))
  - azure_rm_*: Fix version_added for `v2.7.0` ([#1693](https://github.com/ansible-collections/azure/pull/1693))
  - azure_rm_openshiftcluster: Remove `vm_size` option ([#1691](https://github.com/ansible-collections/azure/pull/1691))
  - azure_rm_aks: Fixed `ManagedClusterIdentity` object has no attribute get ([#1730](https://github.com/ansible-collections/azure/pull/1730))
  - azure_rm_virtualmachinescalesetinstance: Update document ([#1732](https://github.com/ansible-collections/azure/pull/1732))

### BREAKING CHANGE
  - azure_rm_aks: Deprecate `docker_bridge_cidr` ([#1718](https://github.com/ansible-collections/azure/pull/1718))
  - azure_rm_openshiftmanagedcluster: Deprecate `vm_size` options ([#1691](https://github.com/ansible-collections/azure/pull/1691))
  - azure_rm_sqlmanagedinstance: Deprecate `identity.tenant_id` and `identity.principal_id` ([#1633](https://github.com/ansible-collections/azure/pull/1633))


## v2.7.0 (2024-08-30)

### NEW MODULES
  - azure_rm_afdendpoint: Add support for managed Azure Front Door Endpoint ([#1589](https://github.com/ansible-collections/azure/pull/1589))
  - azure_rm_afdendpoint_info: Add support for get Azure Front Door Endpoint ([#1589](https://github.com/ansible-collections/azure/pull/1589))
  - azure_rm_openshiftmanagedclusterversion_info: Add support to fetch Azure Red Hat OpenShift managed cluster ([#1602](https://github.com/ansible-collections/azure/pull/1602))

### FEATURE ENHANCEMENT
  - azure_rm_cdnprofile:
    - Add support for `Standard` and `Premium` ([#1588](https://github.com/ansible-collections/azure/pull/1588))
    - Add support for managed identity ([#1621](https://github.com/ansible-collections/azure/pull/1621))
  - azure_rm_aduer: Add support for `password_force_change` and `password_force_change_mfa` ([#1376](https://github.com/ansible-collections/azure/pull/1376))
  - azure_rm_appgateway: Add support managed identity ([#1598](https://github.com/ansible-collections/azure/pull/1598))
  - azure_rm_batchaccount: Add support managed identity ([#1611](https://github.com/ansible-collections/azure/pull/1611))
  - azure_rm_batchaccount_info: Add support managed identity ([#1611](https://github.com/ansible-collections/azure/pull/1611))
  - azure_rm_iothub:
    - Add support managed identity ([#1615](https://github.com/ansible-collections/azure/pull/1615))
    - Upgrade `azure-mgmt-iothub` to `v3.0.0` ([#1641](https://github.com/ansible-collections/azure/pull/1641))
  - azure_rm_adapplication: Add support for `app_diff` ([#1560](https://github.com/ansible-collections/azure/pull/1560))
  - azure_rm_aduser: Add support for `mobile_phone` ([#1623](https://github.com/ansible-collections/azure/pull/1623))
  - azure_rm_aduser_info: Add support for `mobile_phone` ([#1623](https://github.com/ansible-collections/azure/pull/1623))
  - azure_rm_manageddisk_info: Add support for `time_created` ([#1638](https://github.com/ansible-collections/azure/pull/1638))
  - azure_rm_storageaccount: Add support managed identity ([#1639](https://github.com/ansible-collections/azure/pull/1639))
  - azure_rm_storageaccount_info: Add support managed identity ([#1639](https://github.com/ansible-collections/azure/pull/1639))
  - pr-pipeline.yml:
    - Add new resource group test location `westus2` ([#1642](https://github.com/ansible-collections/azure/pull/1642))
    - Upgrade azure-mgmt-containerservice to v31.0.0 ([#1677](https://github.com/ansible-collections/azure/pull/1677))
  - azure_rm_postgresqlflexibleserver: Add more options for `version` ([#1650](https://github.com/ansible-collections/azure/pull/1650))
  - azure_rm_servicebus: Add support managed identity ([#1643](https://github.com/ansible-collections/azure/pull/1643))
  - azure_rm_servicebus_info: Add support managed identity ([#1643](https://github.com/ansible-collections/azure/pull/1643))
  - azure_rm_virtualnetwork_info: List usage of the subnets within a virtual network ([#1673](https://github.com/ansible-collections/azure/pull/1673))
  - azure_rm_rediscache: Add support managed identity ([#1651](https://github.com/ansible-collections/azure/pull/1651))
  - azure_rm_rediscache_info: Add support managed identity ([#1651](https://github.com/ansible-collections/azure/pull/1651))
  - azure_rm_recoveryservicesvault: Add support managed identity ([#1678](https://github.com/ansible-collections/azure/pull/1678))
  - azure_rm_recoveryservicesvault_info: Add support managed identity ([#1678](https://github.com/ansible-collections/azure/pull/1678))
  - azure_rm_aksagent: Add support for `node_taints` ([#1685](https://github.com/ansible-collections/azure/pull/1685))
  - azure_rm_aks: Add support for `auto_upgrade_profile` ([#1682](https://github.com/ansible-collections/azure/pull/1682))
  - azure_rm_diskencryptionset: Add support managed identity ([#1676](https://github.com/ansible-collections/azure/pull/1676))
  - azure_rm_sqlserver: Add support managed identity ([#1626](https://github.com/ansible-collections/azure/pull/1626))
  - azure_rm_sqlserver_info: Add support managed identity ([#1626](https://github.com/ansible-collections/azure/pull/1626))
  - azure_rm_cosmosdbaccount: Add support managed identity ([#1645](https://github.com/ansible-collections/azure/pull/1645))
  - azure_rm_cosmosdbaccount_info: Add support managed identity ([#1645](https://github.com/ansible-collections/azure/pull/1645))
  - azure_rm_functionapp: Add support managed identity` ([#1690](https://github.com/ansible-collections/azure/pull/1645))

### BUG FIXING
  - azure_rm_snapshot: Upgrade azure_rm_snapshot api-version to `v2022-03-02` ([#1597](https://github.com/ansible-collections/azure/pull/1597))
  - azure_rm_storageblob: Fix auth mode login for `azure_rm_storageblob` ([#1605](https://github.com/ansible-collections/azure/pull/1605))
  - azure_rm_postgresqlserver: Update the `admin_password` descriptions ([#1634](https://github.com/ansible-collections/azure/pull/1634))
  - azure_rm_*: Update test case ([#1619](https://github.com/ansible-collections/azure/pull/1619))
  - azure_rm_galleryimageversion: Wait 10 minutes to get the `imageversion` state ([#1625](https://github.com/ansible-collections/azure/pull/1625))
  - azure_rm_openshiftmanagedcluster_info: Fixed errors caused by empty dictionary ([#1632](https://github.com/ansible-collections/azure/pull/1632))
  - azure_rm_galleryimageversion_info: Check for presence of key instead of value ([#1637](https://github.com/ansible-collections/azure/pull/1637))
  - azure_rm_openshiftmanagedcluster: Enhance null check ([#1629](https://github.com/ansible-collections/azure/pull/1629))
  - azure_rm_openshiftmanagedclusterkubeconfig_info: Update client ([#1631](https://github.com/ansible-collections/azure/pull/1631))
  - azure_rm: Implement long running polling for inventory plugin([#1649](https://github.com/ansible-collections/azure/pull/1649))
  - azure_rm_manageddisk: Fix update bug ([#1666](https://github.com/ansible-collections/azure/pull/1666))
  - azure_rm_postgresqlconfiguration: Fix SDK call to use Configuration class ([#1670](https://github.com/ansible-collections/azure/pull/1670))
  - azure_rm_virtualmachineextension: Enable automatic update for vm extensions ([#1662](https://github.com/ansible-collections/azure/pull/1662))
  - azure_rm_virtualnetwork: Fix the bug that failed to detect IPV6 ([#1652](https://github.com/ansible-collections/azure/pull/1652))
  - azure_rm_virtualmachinescaleset: Fixed the issue that tags cannot be updated ([#1654](https://github.com/ansible-collections/azure/pull/1654))
  - azure_rm_aksagentpool: Ignore `node_public_ip_prefix_id` when updating AKS pool ([#1668](https://github.com/ansible-collections/azure/pull/1668))
  - azure_rm_aksagentpool_info: Ignore `node_public_ip_prefix_id` when updating AKS pool  ([#1668](https://github.com/ansible-collections/azure/pull/1668))
  - azure_rm_virtualmachine: Fix latest image version not returned ([#1669](https://github.com/ansible-collections/azure/pull/1669))
  - azure_rm_networkinterface:
    - Set primary key when the `ip_configuration` has more than 2 ([#1679](https://github.com/ansible-collections/azure/pull/1679))
    - Add support for create second `ip_configuration` ([#1686](https://github.com/ansible-collections/azure/pull/1686))
  - azure_rm_loadbalancer: Fixed load balancing idempotent issue ([#1688](https://github.com/ansible-collections/azure/pull/1688))
  - azure_rm_cdnprofile: Fixed a bug when identity is None ([#1689](https://github.com/ansible-collections/azure/pull/1689))
  - azure_rm_cdnprofile_info: Fixed a bug when identity is None ([#1689](https://github.com/ansible-collections/azure/pull/1689))
  - azure_rm_diskencryptionset_info: Fixed a bug when identity is None ([#1689](https://github.com/ansible-collections/azure/pull/1689))


## v2.6.0 (2024-07-01)

### FEATURE ENHANCEMENT
  - Minimum supported Ansible core version to v2.15 - Ansible v2.15 EOL(https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-community-changelogs) 

## v2.5.0 (2024-06-28)

### NEW MODULES
  - azure_rm_capacityreservationgroup: Add support for managed capacity reservation group ([#1557](https://github.com/ansible-collections/azure/pull/1557))
  - azure_rm_capacityreservationgroup_info: Add support for get capacity reservation group ([#1557](https://github.com/ansible-collections/azure/pull/1557))
  - azure_rm_networkwatcher: Add support for managed network watcher ([#1576](https://github.com/ansible-collections/azure/pull/1576))
  - azure_rm_networkwatcher_info: Add support for get network watcher facts ([#1576](https://github.com/ansible-collections/azure/pull/1576))
  - azure_rm_networkflowlogs: Add support for managed network flow logs ([#1576](https://github.com/ansible-collections/azure/pull/1576))
  - azure_rm_networkflowlogs_info: Add support for get network flow logs ([#1576](https://github.com/ansible-collections/azure/pull/1576))

### FEATURE ENHANCEMENT
  - azure_rm_webapp: Add support for `identity` ([#1566](https://github.com/ansible-collections/azure/pull/1566))
  - azure_rm_webapp_info: Add support for `identity` ([#1566](https://github.com/ansible-collections/azure/pull/1566))
  - azure_rm_galleryimageversion: Allow creating gallery image versions from storage accounts ([#1466](https://github.com/ansible-collections/azure/pull/1466))
  - requirements.txt:
    - Bump `azure-storage-blob` from 12.11.0 to 12.13.0 ([#1572](https://github.com/ansible-collections/azure/pull/1572))
    - Update `azure-cli-core` to 2.61.0 ([#1593](https://github.com/ansible-collections/azure/pull/1593))
    - Bump `azure-identity` from 1.14.0 to 1.16.1 ([#1596](https://github.com/ansible-collections/azure/pull/1596))
    - Limit `azure-iot-hub` to `x86_64 platforms` ([#1609](https://github.com/ansible-collections/azure/pull/1609))
  - azure_rm_containerinstance: Add support for `identity` ([#1581](https://github.com/ansible-collections/azure/pull/1581))
  - azure_rm_containerinstance_info: Add support for `identity` ([#1581](https://github.com/ansible-collections/azure/pull/1581))
  - azure_rm_storageaccount: Add support for `allow_shared_key_access` ([#1583](https://github.com/ansible-collections/azure/pull/1583))
  - azure_rm_virtualmachinescaleset: Add support for `identity` ([#1585](https://github.com/ansible-collections/azure/pull/1585))
  - azure_rm_virtualmachinescaleset_info: Add support for `identity` ([#1585](https://github.com/ansible-collections/azure/pull/1585))

### BUG FIXING
  - azure_rm_webapp: Delete the imported logging module ([#1567](https://github.com/ansible-collections/azure/pull/1567))
  - azure_rm_postgresqlflexiblefirewallrule: Delete the imported logging module ([#1567](https://github.com/ansible-collections/azure/pull/1567))
  - azure_rm_adgroup_info: Return None if not a member of the group ([#1579](https://github.com/ansible-collections/azure/pull/1579))


## v2.4.0 (2024-05-30)

### NEW MODULES
  - azure_rm_storageaccountmanagementpolicy: Add support for manage storage account management policy ([#1536](https://github.com/ansible-collections/azure/pull/1536))
  - azure_rm_storageaccountmanagementpolicy_info: Add support for manage storage account management policy ([#1536](https://github.com/ansible-collections/azure/pull/1536))
  - azure_rm_virtualnetworkgatewaynatrule: Add support for managed virtual network gateway nat rule ([#1525](https://github.com/ansible-collections/azure/pull/1525))
  - azure_rm_virtualnetworkgatewaynatrule_info: Add support for virtual network gateway nat rule ([#1525](https://github.com/ansible-collections/azure/pull/1525))
  - azure_rm_localnetworkgateway: Add support for mange local network gateway ([#1523](https://github.com/ansible-collections/azure/pull/1523))
  - azure_rm_localnetworkgateway_info: Add fetch for mange local network gateway facts ([#1523](https://github.com/ansible-collections/azure/pull/1523))
  - azure_rm_sqlmidatabase: Add support for managed SQL managed database ([#1548](https://github.com/ansible-collections/azure/pull/1548))
  - azure_rm_sqlmidatabase_info: Add support for fetch the managed SQL managed database ([#1548](https://github.com/ansible-collections/azure/pull/1548))
  - azure_rm_sqlmidblongtermretentionpolicy: Add support for managed SQL managed database long term retention policy ([#1548](https://github.com/ansible-collections/azure/pull/1548))
  - azure_rm_sqlmidblongtermretentionpolicy_info: Add support for fetch managed SQL managed database long term retention policy ([#1548](https://github.com/ansible-collections/azure/pull/1548))
  - azure_rm_sqlmidbshorttermretentionpolicy: Add support for fetch managed SQL managed database short term retention policy ([#1548](https://github.com/ansible-collections/azure/pull/1548))
  - azure_rm_sqlmidbshorttermretentionpolicy_info: Add support for fetch managed SQL managed database short term retention policy ([#1548](https://github.com/ansible-collections/azure/pull/1548))
  - azure_rm_vmsku_info: Add support for list VM SKUs ([#1546](https://github.com/ansible-collections/azure/pull/1546))
  - tests/integration/requirements.txt: Symlink requirements-azure.txt from tests/integration ([#1551](https://github.com/ansible-collections/azure/pull/1551))

### FEATURE ENHANCEMENT
  - azure_rm_aduser: Add support for `on_premises_extension_attributes` ([#1518](https://github.com/ansible-collections/azure/pull/1518))
  - azure_rm_aduser_info: Add support for `on_premises_extension_attributes` ([#1518](https://github.com/ansible-collections/azure/pull/1518))
  - azure_keyvault_secret: Add support for `cloud_type` ([#1517](https://github.com/ansible-collections/azure/pull/1517))
  - azure_rm_postgresqlflexibleserver: Add support for `identity` ([#1528](https://github.com/ansible-collections/azure/pull/1528))
  - azure_rm_postgresqlflexibleserver_info: Add support for `identity` ([#1528](https://github.com/ansible-collections/azure/pull/1528))
  - plugins/inventory/azure_rm.py: Expand Inventory filter integration tests ([#1547](https://github.com/ansible-collections/azure/pull/1547))
  - azure_rm_webapp: Add support for `site_auth_settings` ([#1538](https://github.com/ansible-collections/azure/pull/1538))
  - azure_rm_webapp_info: Add support for `site_auth_settings` ([#1538](https://github.com/ansible-collections/azure/pull/1538))
  - azure_rm_aks:
    - Add support for UserAssigned Identity ([#1543](https://github.com/ansible-collections/azure/pull/1543))
    - Add `managedNATGateway` and `userAssignedNATGateway` to `outbound_type` ([#1537](https://github.com/ansible-collections/azure/pull/1537))
  - azure_rm_webappaccessrestriction: Add more parameters to `ip_security_restrictions` ([#1558](https://github.com/ansible-collections/azure/pull/1558))
  - azure_rm_webappaccessrestriction_info: Add more parameters to `ip_security_restrictions` ([#1558](https://github.com/ansible-collections/azure/pull/1558))
  - azure_rm_virtualmachine: Add support for attaching existing managed data disks at VM creation ([#1430](https://github.com/ansible-collections/azure/pull/1430))
  - azure_rm_aksagentpool: Add support for more parameters ([#1477](https://github.com/ansible-collections/azure/pull/1477))
  - azure_rm_aksagentpool_info: Add support for  more parameters ([#1477](https://github.com/ansible-collections/azure/pull/1477))
  - azure_rm_adgroup: Allow service principals and nested groups to be returned in membership attributes ([#1507](https://github.com/ansible-collections/azure/pull/1507))
  - azure_rm_adgroup_info: Allow service principals and nested groups to be returned in membership attributes ([#1507](https://github.com/ansible-collections/azure/pull/1507))
  - azure_rm_backupazurevm: No need to json serialization the response ([#1531](https://github.com/ansible-collections/azure/pull/1531))

### BUG FIXING
  - azure_rm_adapplication: Fix `optional_claims` handling ([#1480](https://github.com/ansible-collections/azure/pull/1480))
  - azure_rm_cognitivesearch: Fix test failed ([#1520](https://github.com/ansible-collections/azure/pull/1520))
  - azure_rm_common.py: Fix the inconsistency between custom classes and Python SDK attributes ([#1554](https://github.com/ansible-collections/azure/pull/1554))
  - meta/runtime.yml:
    - Keep action_groups and modules list consistent ([#1553](https://github.com/ansible-collections/azure/pull/1553))
    - Delete the deprecate modules ([#1556](https://github.com/ansible-collections/azure/pull/1556))
  - azure_rm_rediscache_info: Fix typo ([#1550](https://github.com/ansible-collections/azure/pull/1550))
  - plugins/inventory/azure_rm.py: Fix inventory host processing ([#1545](https://github.com/ansible-collections/azure/pull/1545))
  - azure_rm_accesstoken_info: Fix authorization issue ([#1541](https://github.com/ansible-collections/azure/pull/1541))
  - azure_rm_adgroup: Support update functionality ([#1530](https://github.com/ansible-collections/azure/pull/1530))
  - azure_rm_webapp: Delete the imported logging module ([#1567](https://github.com/ansible-collections/azure/pull/1567))
  - azure_rm_postgresqlflexiblefirewallrule: Delete the logging module ([#1567](https://github.com/ansible-collections/azure/pull/1567))
  - azure_rm_loadbalancer: Remove functionality which should have been removed for Ansible 2.9 ([#1508](https://github.com/ansible-collections/azure/pull/1508))
  - azure_rm_networkinterface: Remove functionality which should have been removed for Ansible 2.9 ([#1508](https://github.com/ansible-collections/azure/pull/1508))
  - azure_rm_localnetworkgateway: Fix documentation mistakes ([#1563](https://github.com/ansible-collections/azure/pull/1563))
  - azure_rm_virtualmachine: Create `_own_nsg_` tag only if `created_nsg` is `true` ([#1565](https://github.com/ansible-collections/azure/pull/1565))
  - azure_rm_storageblob: Fix authentication issue when shared keys disabled ([#1564](https://github.com/ansible-collections/azure/pull/1564))
  - azure_rm_virtualmachinescalesetinstance_info: Fixed obtaining flexible VMSS instances failed ([#1529](https://github.com/ansible-collections/azure/pull/1529))

### BREAKING CHANGE: 
  - azure_rm_datalakestore: Deprecate `azure-mgmt-datalake-store` ([#1555](https://github.com/ansible-collections/azure/pull/1555))
  - azure_rm_datalakestore_info: Deprecate `azure_rm_datalakestore_info` ([#1555](https://github.com/ansible-collections/azure/pull/1555))
  - requirements.txt: Rename `requirements-azure.txt` to `requirements.txt` ([#1552](https://github.com/ansible-collections/azure/pull/1552))
  - sanity-requirements.txt: Rename `sanity-requirements-azure.txt` to `sanity-requirements.txt` ([#1552](https://github.com/ansible-collections/azure/pull/1552))

## v2.3.0 (2024-03-27)

### NEW MODULES
  - azure_rm_akscredentials_info: Support to obtain Azure Kubernetes Service Credentials ([#1484](https://github.com/ansible-collections/azure/pull/1484))

### FEATURE ENHANCEMENT
  - sanity-requirements-azure.txt:
    - Bump cryptography from 41.0.6 to 42.0.2 ([#1450](https://github.com/ansible-collections/azure/pull/1450))
    - Bump cryptography from 42.0.2 to 42.0.4 ([#1458](https://github.com/ansible-collections/azure/pull/1458))
  - azure_rm_networkinterface_info: Return the subnet ID ([#1462](https://github.com/ansible-collections/azure/pull/1462))
  - azure_rm_appgateway: Add support for `port` and `match` in `probes` ([#1470](https://github.com/ansible-collections/azure/pull/1470))
  - azure_rm_common.py:
    - Add support for import new version `azure-mgmt-recoveryservicesbackup` modules ([#1469](https://github.com/ansible-collections/azure/pull/1469))
    - Add support for `disable_instance_discovery` ([#1442](https://github.com/ansible-collections/azure/pull/1442))
    - Respect `AZURE_CLIENT_ID`, `ANSIBLE_AZURE_AUTH_SOURCE` on inventory plugin ([#713](https://github.com/ansible-collections/azure/pull/713))
  - azure_rm_aksversion_info: Add support for `allow_preview` ([#1456](https://github.com/ansible-collections/azure/pull/1456))
  - azure_rm_adgroup: Add Support for `description` ([#1492](https://github.com/ansible-collections/azure/pull/1492))
  - azure_rm_adgroup_info: Add support for `description` ([#1492](https://github.com/ansible-collections/azure/pull/1492))
  - azure_rm_wbapp: Support to create Web App with Java11/Java17/Java21 ([#1495](https://github.com/ansible-collections/azure/pull/1495))
  - azure_rm_adapplication: Add support for `spa_redirect_urls` and `public_client_redirect_urls` ([#1494](https://github.com/ansible-collections/azure/pull/1494))
  - azure_rm_adapplication_info: Add support for `spa_redirect_urls` and `public_client_redirect_urls` ([#1494](https://github.com/ansible-collections/azure/pull/1494))
  - azure_rm_galleryimage: Add support for `architecture` ([#1493](https://github.com/ansible-collections/azure/pull/1493))
  - azure_rm_keyvaultsecret: Support recover/purge deleted secrets ([#1489](https://github.com/ansible-collections/azure/pull/1489))
  - azure_rm_keyvaultsecret_info: Support recover/purge deleted secrets ([#1489](https://github.com/ansible-collections/azure/pull/1489))
  - azure_rm_recoveryservicesvault_info: Support listing the vaults in same resource group ([#1487](https://github.com/ansible-collections/azure/pull/1487))
  - azure_rm_resource_info: Add support for `tags` ([#1498](https://github.com/ansible-collections/azure/pull/1498))
  - azure_rm_aduser: Add support for `company_name` ([#1504](https://github.com/ansible-collections/azure/pull/1504))
  - azure_rm_aduser_info: Add support for `company_name` ([#1504](https://github.com/ansible-collections/azure/pull/1504))
  - azure_rm_aks: Support manage pod identities in managed Kubernetes cluster ([#1497](https://github.com/ansible-collections/azure/pull/1497))
  - azure_rm_adserviceprincipal_info: Fix listing all service principals ([#1482](https://github.com/ansible-collections/azure/pull/1482))
  - azure_rm_virtualmachie: Add support for swap OS disk ([#1435](https://github.com/ansible-collections/azure/pull/1435))

### BUG FIXING
  - azure_rm_adgroup: Fix unsupported header in azure_rm_adgroup ([#1467](https://github.com/ansible-collections/azure/pull/1467))
  - azure_rm_keyvaultkey_info: Typos fix ([#1468](https://github.com/ansible-collections/azure/pull/1468))
  - azure_rm_sqlmanagedinstance: Typos fix ([#1468](https://github.com/ansible-collections/azure/pull/1468))
  - azure_rm_sqlmanagedinstance_info: Typos fix ([#1468](https://github.com/ansible-collections/azure/pull/1468))
  - azure_rm_virtualmachine: Typos fix ([#1468](https://github.com/ansible-collections/azure/pull/1468))
  - ../azure_rm_storageaccount/tasks/main.yml: Removing leftover storage account from test ([#1449](https://github.com/ansible-collections/azure/pull/1449))
  - azure_rm_aduser_info: Parse paginated replies for listing all users/groups ([#1448](https://github.com/ansible-collections/azure/pull/1448))
  - azure_rm_adgroup_info: Parse paginated replies for listing all users/groups ([#1448](https://github.com/ansible-collections/azure/pull/1448))
  - azure_rm.py: Allow for template expressions in some parameters ([#1446](https://github.com/ansible-collections/azure/pull/1446))
  - azure_rm_galleryimageversion_info: Check the return value ([#1436](https://github.com/ansible-collections/azure/pull/1436))
  - azure_rm_servicebus_info: Fixed return value format error ([#1503](https://github.com/ansible-collections/azure/pull/1503))
  - azure_rm_appgateway: Ensure `enable_http2` works when targeting existing Application Gateways ([#1439](https://github.com/ansible-collections/azure/pull/1439))
  - azure_rm_datalakestore: Disable testings due to the Azure Data Lake Store Gen1 retired ([#1501](https://github.com/ansible-collections/azure/pull/1501))
  - azure_rm_datalakestore_info: Disable testings due to the Azure Data Lake Store Gen1 retired ([#1501](https://github.com/ansible-collections/azure/pull/1501))
  - azure_rm_gallery_info: Detects the return value and returns None if the return value is empty ([#1483](https://github.com/ansible-collections/azure/pull/1483))
  - azure_rm_account_info: Change the default value of `is_ad_resource` to True ([#1510](https://github.com/ansible-collections/azure/pull/1510))


## v2.2.0 (2024-02-04)

### NEW MODULES
  - azure_rm_publicipprefix ([#1403](https://github.com/ansible-collections/azure/pull/1403))
  - azure_rm_publicipprefix_info ([#1403](https://github.com/ansible-collections/azure/pull/1403))
  - azure_rm_sshpublickey ([#1190](https://github.com/ansible-collections/azure/pull/1190))
  - azure_rm_sshpublickey_info ([#1190](https://github.com/ansible-collections/azure/pull/1190))
  - azure_rm_postgresqlflexibleserver ([1192](https://github.com/ansible-collections/azure/pull/1192))
  - azure_rm_postgresqlflexibleserver_info ([1192](https://github.com/ansible-collections/azure/pull/1192))
  - azure_rm_postgresqlflexibleconfiguration_info ([1192](https://github.com/ansible-collections/azure/pull/1192))
  - azure_rm_postgresqlflexibledatabase ([1192](https://github.com/ansible-collections/azure/pull/1192))
  - azure_rm_postgresqlflexibledatabase_info ([1192](https://github.com/ansible-collections/azure/pull/1192))
  - azure_rm_postgresqlflexiblefirewallrule ([1192](https://github.com/ansible-collections/azure/pull/1192))
  - azure_rm_postgresqlflexiblefirewallrule_info ([1192](https://github.com/ansible-collections/azure/pull/1192))

### FEATURE ENHANCEMENT
  - azure_rm_adapplication: Add support for `sign_in_audience` ([#1401](https://github.com/ansible-collections/azure/pull/1401))
  - plugins/inventory/azure_rm.py:
    - Add support for export `lincense_type` ([#1411](https://github.com/ansible-collections/azure/pull/1411))
    - Set `andible_host` to Public IP Address, use Private IP Address if not exist ([#1406](https://github.com/ansible-collections/azure/pull/1406))
    - Add support for export `subnet` ([#1422](https://github.com/ansible-collections/azure/pull/1422))
  - azure_rm_virtualmachine: Add support for `additional_capabilities` ([#1399](https://github.com/ansible-collections/azure/pull/1399))
  - azure_rm_storageaccount: Add support for `enable_nfs_v3` ([#1346](https://github.com/ansible-collections/azure/pull/1346))
  - azure_rm_subnet: Add `Microsoft.ContainerService/managedClusters` to subnet delegations ([#1414](https://github.com/ansible-collections/azure/pull/1414))
  - azure_rm_adapplication_info: 
    - Searching by tenant returns all AD applications ([#1420](https://github.com/ansible-collections/azure/pull/1420)) 
    - Enhance search for application by `app_display_name` ([#1420](https://github.com/ansible-collections/azure/pull/1420))
  - azure_rm_appgateway: Add support `tags` ([#1373](https://github.com/ansible-collections/azure/pull/1373))

### BUG FIXING
  - azure_rm_common.py:
    - Fix missing `client_id` in payload error when using only username/password ([#1409](https://github.com/ansible-collections/azure/pull/1409))
    - Add missing Azure API Profiles ([#1395](https://github.com/ansible-collections/azure/pull/1395))
    - Fix MSI authorization credentials ([#1393](https://github.com/ansible-collections/azure/pull/1393))
    - Fix the `client_id` value ([#1421](https://github.com/ansible-collections/azure/pull/1421))
  - azure_rm_virtualmachine:
    - Fix `os_profile` error [#1397](https://github.com/ansible-collections/azure/pull/1397))
    - Fixed disk mount error ([#1407](https://github.com/ansible-collections/azure/pull/1407))
    - Fixed properties mapping error ([#1410](https://github.com/ansible-collections/azure/pull/1410))
    - Detect the VM's `powerstate` value ([#1412](https://github.com/ansible-collections/azure/pull/1412))
    - Limit zones to at most one ([#1392](https://github.com/ansible-collections/azure/pull/1392))
  - azure_rm_*: Deprecate custom properties ([#1388](https://github.com/ansible-collections/azure/pull/1388))
  - azure_rm_networkinterface: Fixed `subscription_id` not used ([#1416](https://github.com/ansible-collections/azure/pull/1416))
  - azure_rm_adgroup: 
    - Update test cases to use `object_id` ([#1418](https://github.com/ansible-collections/azure/pull/1418))
    - Fix test case ([#1426](https://github.com/ansible-collections/azure/pull/1426))
  - azure_rm_adapplication: Fix test case ([#1425](https://github.com/ansible-collections/azure/pull/1425))


## v2.1.1 (2023-12-19)

### FEATURE ENHANCEMENT
  - **/task/main.yml: Remove unneeded waits in test cases ([#1374](https://github.com/ansible-collections/azure/pull/1374))
  - azure_rm_securitygroup: Add upper letter protocol to security group ([#1381](https://github.com/ansible-collections/azure/pull/1381))
  - Update min Ansible core version to v2.14 - Ansible v2.13 EOF Nov.6 2023 ([#1382](https://github.com/ansible-collections/azure/pull/1382))

### BUG FIXING
  - plugins/inventory/azure_rm.py: Restore the return of `public_ipv4_address` and fix the bug that the VM does not have a public IP address ([#1379](https://github.com/ansible-collections/azure/pull/1379))


## v2.1.0 (2023-12-13)

### NEW MODULES
  - azure_rm_accesstoken_info ([#1318](https://github.com/ansible-collections/azure/pull/1318))
  - azure_rm_openshiftmanagedclusterkubeconfig_info ([#1238](https://github.com/ansible-collections/azure/pull/1238))
  - azure_rm_sshpublickey ([#1190](https://github.com/ansible-collections/azure/pull/1190))
  - azure_rm_sshpublickey_info ([#1190](https://github.com/ansible-collections/azure/pull/1190))

### FEATURE ENHANCEMENT
  - azure_rm_storageaccount: Add support for `large_file_shares_state` ([#1210](https://github.com/ansible-collections/azure/pull/1210))
  - azure_rm_storageaccount_info: Add support for `large_file_shares_state`([#1210](https://github.com/ansible-collections/azure/pull/1210))
  - azure_rm(`inventory`): 
    - Add support for `include_host_filters` ([#1347](https://github.com/ansible-collections/azure/pull/1347))
    - Enhance inventory name checking  ([#1348](https://github.com/ansible-collections/azure/pull/1348))
  - azure_rm_webapp : Add support for `http20_enabled` ([#1360](https://github.com/ansible-collections/azure/pull/1360))
  - azure_rm_webapp_info : Add support for `http20_enabled` ([#1360](https://github.com/ansible-collections/azure/pull/1360))
  - azure_rm_virtualmachine : Add retry logic for VM state synchronization ([#1354](https://github.com/ansible-collections/azure/pull/1354))
  - azure_rm_virtualmachinescaleset : Add retry logic for VM state synchronization ([#1354](https://github.com/ansible-collections/azure/pull/1354))
  - azure_keyvault_secret: Added support for `use_msi`(disable MSI autodiscover feature in `azure_keyvault_secret` lookup plugin) ([#1353](https://github.com/ansible-collections/azure/pull/1353))
  - sanity-requirements-azure.txt: Bump cryptography from `41.0.4` to `41.0.6` ([#1349](https://github.com/ansible-collections/azure/pull/1349))

### BUG FIXING
  - AD resources : Fix get resource with CLI credentials ([#1364](https://github.com/ansible-collections/azure/pull/1364))
  - azure_rm_iotdevice: Fixed the issue of failed to obtain alias parameters  ([#1278](https://github.com/ansible-collections/azure/pull/1278))
  - azure_rm_iotdevicemodule: Fixed the issue of failed to obtain alias parameters ([#1278](https://github.com/ansible-collections/azure/pull/1278))
  - azure_rm_virtualmachine: Support update `proximity_placement_group` ([#1329](https://github.com/ansible-collections/azure/pull/1329))
  - azure_rm_common: Fix the CLI authorization obtain token error ([#1340](https://github.com/ansible-collections/azure/pull/1340))
  - azure_rm_adapplication: Fix get application error ([#1345](https://github.com/ansible-collections/azure/pull/1345))
  - azure_rm_adapplication_info: Fix get application error ([#1345](https://github.com/ansible-collections/azure/pull/1345))
  - azure_rm_manageddisk: Support unmount disk from VMs in different resource group ([#1201](https://github.com/ansible-collections/azure/pull/1201))
  - azure_rm_resource: Fix failure on response for non-json body ([#1341](https://github.com/ansible-collections/azure/pull/1341))
  - azure_rm_deployment: Fix delete the whole resource group when state is `absent` ([#1231](https://github.com/ansible-collections/azure/pull/1231))
  - azure_rm_adgroup: Fix get group error ([#1355](https://github.com/ansible-collections/azure/pull/1355))
  - azure_rm_adgroup_info: Fix get group error ([#1355](https://github.com/ansible-collections/azure/pull/1355))
  - azure_rm_aduser_info: Fix get user error ([#1355](https://github.com/ansible-collections/azure/pull/1355))
  - azure_rm(`inventory`): Fix dynamic VM fetch failure when `batch_fetch=true` ([#1344](https://github.com/ansible-collections/azure/pull/1344))
  - azure_rm_adapplication: Fix parameter error ([#1369](https://github.com/ansible-collections/azure/pull/1369))

### BREAKING CHANGE
  - azure_rm: Rename `public_ipv4_addresses` to `public_ip_address`and change type to list ([#1214](https://github.com/ansible-collections/azure/pull/1214))

## v2.0.0 (2023-11-17)

### FEATURE ENHANCEMENT
  - azure_rm_storageblob: Add support for `auth_mode` ([#1315](https://github.com/ansible-collections/azure/pull/1315))
  - azure_rm_galleryimageversion: Add support for `encryption` ([#1311](https://github.com/ansible-collections/azure/pull/1311))
  - azure_rm_galleryimage: Add support for `features` ([#1310](https://github.com/ansible-collections/azure/pull/1310))
  - azure_rm_apimanagement: Bump API version to `v2022-08-01` ([#1327](https://github.com/ansible-collections/azure/pull/1327))

  - azure_rm_apimanagement_info: Bump API version to `v2022-08-01` ([#1327](https://github.com/ansible-collections/azure/pull/1327))
  - azure_rm_apimanagementservice: Bump API version to `v2022-08-01` ([#1327](https://github.com/ansible-collections/azure/pull/1327))
  - azure_rm_apimanagementservice_info: Bump API version to `v2022-08-01` ([#1327](https://github.com/ansible-collections/azure/pull/1327))
  - azure_rm_*: Add `hasattr` method to verify return value ([#1307](https://github.com/ansible-collections/azure/pull/1307))
  - azure_rm_virtualmachine_info: Add `vm_agent_version` to output ([#1289](https://github.com/ansible-collections/azure/pull/1289))
  - azure_rm_virtualmachine:
    - Add support for `os_disk_encryption_set` ([#1306](https://github.com/ansible-collections/azure/pull/1306))
    - Add `disk_encryption_set` for data disks ([#1309](https://github.com/ansible-collections/azure/pull/1309))
  - azure_service_principal_attribute: Move `azure_service_principal_attribute.py` to azure-collecitons lookup file ([#1326](https://github.com/ansible-collections/azure/pull/1326)
  - azure_rm_account_info: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adapplication: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_adapplication_info: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_adgroup: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_adgroup_info: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_adpassword:
    - Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325))
    - Add support for `display_name` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adpassword_info: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_adserviceprincipal: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_adserviceprincipal_info: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_aduser: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - azure_rm_aduser_info: Migrate from ADGraph to MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325)) 
  - pr-pipelines.yml:
    - Add ansible-core v2.16 ([#1305](https://github.com/ansible-collections/azure/pull/1305)) 
    - Update PR validation pipeline timeout to 180 minutes ([#1334](https://github.com/ansible-collections/azure/pull/1334))

### BUG FIXING
  - main.yml: Ansible `is match` does not need a `^` ([#1321](https://github.com/ansible-collections/azure/pull/1321))
  - azure_rm_virtualmachine: Fix caching choices ([#1324](https://github.com/ansible-collections/azure/pull/1324))

### BREAKING CHANGE
  - azure_rm_virtualmachinescaleset: `orchestration_mode` defaults to `Flexible` ([#1331](https://github.com/ansible-collections/azure/pull/1331))
  - azure_rm_adapplication: 
    - Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
    - Deprecate `allow_guests_sign_in` as not supported in MSGraph ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adapplication_info: - Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adgroup: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adgroup_info: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adpassword: 
    - Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
    - Deprecate `value` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adpassword_info: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adserviceprincipal: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_adserviceprincipal_info: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_aduser: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))
  - azure_rm_aduser_info: Deprecate `tenant` ([#1325](https://github.com/ansible-collections/azure/pull/1325))

## v1.19.0 (2023-11-6)

### FEATURE ENHANCEMENT
  - Update all test case Ubuntu Image version to 20.04-LTS, 16.04-LTS will be deprecated ([#1288](https://github.com/ansible-collections/azure/pull/1288))
  - Migrate `msrestazure` to `azure-mgmt-core` and `azure-identity` ([#1267](https://github.com/ansible-collections/azure/pull/1267))
  - Support `ansible-lint` test to `azure.azcollection` ([#1292](https://github.com/ansible-collections/azure/pull/1292))

### BUG FIXING
  - plugins/module_utls/azure_rm_common.py: Add support for custom ADFS endpoint ([#1299](https://github.com/ansible-collections/azure/pull/1299))
  - azure_rm_virtualmachine: Fix `disable_password_authentication` not set bug ([#1301](https://github.com/ansible-collections/azure/pull/1301))
  - azure_rm_azurefiewall_info: Fix `nat_rule_collections` not set bug ([#1308](https://github.com/ansible-collections/azure/pull/1308))
  - azure_rm_*.py: Fixed sanity errors in the module ([#1296](https://github.com/ansible-collections/azure/pull/1296))
  - Add required description to the document ([#1314](https://github.com/ansible-collections/azure/pull/1314))

## v1.18.1 (2023-9-25)

### BUG FIXING
  - inventory/azure_rm: Fix authorization initialization bug. [#1271](https://github.com/ansible-collections/azure/pull/1271)
  - azure_rm_managementgroup_info: Fix `azure_object.type` to equal `Microsoft.Management/managementGroups`. [#1252](https://github.com/ansible-collections/azure/pull/1252)

## v1.18.0 (2023-9-22)

### FEATURE ENHANCEMENT
  - Migrate `msrest` to `azure-core`. [#1245](https://github.com/ansible-collections/azure/pull/1245)
  - Upgrade `GenericRestClient` authorization from ADAL to MSAL - [#1245](https://github.com/ansible-collections/azure/pull/1245)
  - Lazy initialization of AD resource credentials. [#1268](https://github.com/ansible-collections/azure/pull/1268)

## v1.17.0 (2023-8-23)

### FEATURE ENHANCEMENT
  - azure_rm_virtualmachine:
    - Support update User Assigned and System assigned identities ([#1177](https://github.com/ansible-collections/azure/pull/1177))
    - Add support force power off([#1186](https://github.com/ansible-collections/azure/pull/1186))
    - Allow to set boot diagnostics storage account to managed ([#1206](https://github.com/ansible-collections/azure/pull/1206))
  - azure_rm.py:
    - Add creation timestamp to `hostvars` ([#1221](https://github.com/ansible-collections/azure/pull/1221))
    - Add an example on how to add a domain to hostname for dynamic inventory ((#1211](https://github.com/ansible-collections/azure/pull/1211))
  - azure_rm_virtualnetwork: Improve documentation ([#1203](https://github.com/ansible-collections/azure/pull/1203))
  - azure_rm_storageshare: Add support for `enabled_protocols` and `root_squash` ([#1216](https://github.com/ansible-collections/azure/pull/1216))
  - azure_rm_common: Migrate ADAL to MSAL, remove ADAL from direct dependencies ([#1239](https://github.com/ansible-collections/azure/pull/1239))
  - sanity-requirements-azure.txt:
    - Bump cryptography from v38.0.3 to v39.0.1 ([#1076](https://github.com/ansible-collections/azure/pull/1076))
    - Bump cryptography from v39.0.1 to v41.0.3 ([#1244](https://github.com/ansible-collections/azure/pull/1244))
  - azure_rm_batchaccount: Upgrade `azure-mgmt-batch` to v17.0.0 ([#1202](https://github.com/ansible-collections/azure/pull/1202))
  - azure_rm_batchaccount_info: Upgrade `azure-mgmt-batch` to v17.0.0 ([#1202](https://github.com/ansible-collections/azure/pull/1202))
  - pr-pipelines.yml: Update test Ansible version to v2.14.0 ([#1182](https://github.com/ansible-collections/azure/pull/1182))
  - runtime.yml: Keep action_groups and modules list consistent for v1.15.0 and v1.16.0 ([#1188](https://github.com/ansible-collections/azure/pull/1188))
  - azure_rm_aks_info: Support to list all managed cluster ([#1229](https://github.com/ansible-collections/azure/pull/1229))

### BUG FIXING
  - azure_rm_virtualmachine:
    - Fix `version_added in azure_rm_virtualmachine document ([#1180](https://github.com/ansible-collections/azure/pull/1180))
    - Fix setting of encryption at host for VMs ([#1207](https://github.com/ansible-collections/azure/pull/1207))
    - Fix typo `update_security_profle` ([#1194](https://github.com/ansible-collections/azure/pull/1194))
  - README.md: Fix document link in README ([#1189](https://github.com/ansible-collections/azure/pull/1189))
  - azure_rm_keyvaultkey:
    - Fix an error when `client_id` and `secret` are empty ([#1185](https://github.com/ansible-collections/azure/pull/1185))
    - Upgrade `azure-keyvault` to v4.2.0 ([#1198](https://github.com/ansible-collections/azure/pull/1198))
  - azure_rm_keyvaultkey_info:
    - Fix an error when `client_id` and `secret` are empty ([#1185](https://github.com/ansible-collections/azure/pull/1185))
    - Upgrade `azure-keyvault` to v4.2.0 ([#1198](https://github.com/ansible-collections/azure/pull/1198))
  - azure_rm_keyvaultsecret:
    - Fix an error when `client_id` and `secret` are empty ([#1185](https://github.com/ansible-collections/azure/pull/1185))
    - Upgrade `azure-keyvault` to v4.2.0 ([#1198](https://github.com/ansible-collections/azure/pull/1198))
  - azure_rm_keyvaultsecret_info:
    - Fix an error when `client_id` and `secret` are empty ([#1185](https://github.com/ansible-collections/azure/pull/1185))
    - Upgrade `azure-keyvault` to v4.2.0 ([#1198](https://github.com/ansible-collections/azure/pull/1198))
  - azure_rm_manageddisk: source_account_id should be storage_account_id ([#1187](https://github.com/ansible-collections/azure/pull/1187))
  - azure_rm_mmultipleanageddisk: `source_account_id` should be ~~~~`storage_account_id` ([#1187](https://github.com/ansible-collections/azure/pull/1187))
  - azure_rm_virtualmachine_info: Fix the issue when `security_profile` not returned  ([#1205](https://github.com/ansible-collections/azure/pull/1205))
  - azure_rm_backupazurevm: Use the module configured `subscrtion_id` if available ([#1225](https://github.com/ansible-collections/azure/pull/1225))
  - azure_keyvault_secret: Removed subscription_id from azure_keyvault_secret lookup when using az cli auth ([#1175](https://github.com/ansible-collections/azure/pull/1175))

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

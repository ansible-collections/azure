#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_appgateway
version_added: "0.1.2"
short_description: Manage Application Gateway instance
description:
    - Create, update and delete instance of Application Gateway.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the application gateway.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - SKU of the application gateway resource.
        suboptions:
            name:
                description:
                    - Name of an application gateway SKU.
                choices:
                    - 'standard_small'
                    - 'standard_medium'
                    - 'standard_large'
                    - 'standard_v2'
                    - 'waf_medium'
                    - 'waf_large'
                    - 'waf_v2'
            tier:
                description:
                    - Tier of an application gateway.
                choices:
                    - 'standard'
                    - 'standard_v2'
                    - 'waf'
                    - 'waf_v2'
            capacity:
                description:
                    - Capacity (instance count) of an application gateway.
    ssl_policy:
        description:
            - SSL policy of the application gateway resource.
        suboptions:
            disabled_ssl_protocols:
                description:
                    - List of SSL protocols to be disabled on application gateway.
                choices:
                    - 'tls_v1_0'
                    - 'tls_v1_1'
                    - 'tls_v1_2'
            policy_type:
                description:
                    - Type of SSL Policy.
                choices:
                    - 'predefined'
                    - 'custom'
            policy_name:
                description:
                    - Name of Ssl C(predefined) policy.
                choices:
                    - 'ssl_policy20150501'
                    - 'ssl_policy20170401'
                    - 'ssl_policy20170401_s'
            cipher_suites:
                description:
                    - List of SSL cipher suites to be enabled in the specified order to application gateway.
                choices:
                    - tls_ecdhe_rsa_with_aes_256_gcm_sha384
                    - tls_ecdhe_rsa_with_aes_128_gcm_sha256
                    - tls_ecdhe_rsa_with_aes_256_cbc_sha384
                    - tls_ecdhe_rsa_with_aes_128_cbc_sha256
                    - tls_ecdhe_rsa_with_aes_256_cbc_sha
                    - tls_ecdhe_rsa_with_aes_128_cbc_sha
                    - tls_dhe_rsa_with_aes_256_gcm_sha384
                    - tls_dhe_rsa_with_aes_128_gcm_sha256
                    - tls_dhe_rsa_with_aes_256_cbc_sha
                    - tls_dhe_rsa_with_aes_128_cbc_sha
                    - tls_rsa_with_aes_256_gcm_sha384
                    - tls_rsa_with_aes_128_gcm_sha256
                    - tls_rsa_with_aes_256_cbc_sha256
                    - tls_rsa_with_aes_128_cbc_sha256
                    - tls_rsa_with_aes_256_cbc_sha
                    - tls_rsa_with_aes_128_cbc_sha
                    - tls_ecdhe_ecdsa_with_aes_256_gcm_sha384
                    - tls_ecdhe_ecdsa_with_aes_128_gcm_sha256
                    - tls_ecdhe_ecdsa_with_aes_256_cbc_sha384
                    - tls_ecdhe_ecdsa_with_aes_128_cbc_sha256
                    - tls_ecdhe_ecdsa_with_aes_256_cbc_sha
                    - tls_ecdhe_ecdsa_with_aes_128_cbc_sha
                    - tls_dhe_dss_with_aes_256_cbc_sha256
                    - tls_dhe_dss_with_aes_128_cbc_sha256
                    - tls_dhe_dss_with_aes_256_cbc_sha
                    - tls_dhe_dss_with_aes_128_cbc_sha
                    - tls_rsa_with_3des_ede_cbc_sha
                    - tls_dhe_dss_with_3des_ede_cbc_sha
            min_protocol_version:
                description:
                    - Minimum version of Ssl protocol to be supported on application gateway.
                choices:
                    - 'tls_v1_0'
                    - 'tls_v1_1'
                    - 'tls_v1_2'
    gateway_ip_configurations:
        description:
            - List of subnets used by the application gateway.
        suboptions:
            subnet:
                description:
                    - Reference of the subnet resource. A subnet from where application gateway gets its private address.
                suboptions:
                    id:
                        description:
                            - Full ID of the subnet resource. Required if I(name) and I(virtual_network_name) are not provided.
                    name:
                        description:
                            - Name of the subnet. Only used if I(virtual_network_name) is also provided.
                    virtual_network_name:
                        description:
                            - Name of the virtual network. Only used if I(name) is also provided.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    authentication_certificates:
        description:
            - Authentication certificates of the application gateway resource.
        suboptions:
            data:
                description:
                    - Certificate public data - base64 encoded pfx.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    redirect_configurations:
        description:
            - Redirect configurations of the application gateway resource.
        suboptions:
            redirect_type:
                description:
                    - Redirection type.
                choices:
                    - 'permanent'
                    - 'found'
                    - 'see_other'
                    - 'temporary'
            target_listener:
                description:
                    - Reference to a listener to redirect the request to.
            request_routing_rules:
                description:
                    - List of c(basic) request routing rule names within the application gateway to which the redirect is bound.
                version_added: "1.10.0"
            url_path_maps:
                description:
                    - List of URL path map names (c(path_based_routing) rules) within the application gateway to which the redirect is bound.
                version_added: "1.10.0"
            path_rules:
                description:
                    - List of URL path rules within a c(path_based_routing) rule to which the redirect is bound.
                suboptions:
                    name:
                        description:
                            - Name of the URL rule.
                    path_map_name:
                        description:
                            - Name of URL path map.
                version_added: "1.10.0"
            include_path:
                description:
                    - Include path in the redirected url.
            include_query_string:
                description:
                    - Include query string in the redirected url.
            name:
                description:
                    - Name of the resource that is unique within a resource group.
    ssl_certificates:
        description:
            - SSL certificates of the application gateway resource.
        suboptions:
            data:
                description:
                    - Base-64 encoded pfx certificate.
                    - Only applicable in PUT Request.
            password:
                description:
                    - Password for the pfx file specified in I(data).
                    - Only applicable in PUT request.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    frontend_ip_configurations:
        description:
            - Frontend IP addresses of the application gateway resource.
        suboptions:
            private_ip_address:
                description:
                    - PrivateIPAddress of the network interface IP Configuration.
            private_ip_allocation_method:
                description:
                    - PrivateIP allocation method.
                choices:
                    - 'static'
                    - 'dynamic'
            subnet:
                description:
                    - Reference of the subnet resource.
                suboptions:
                    id:
                        description:
                            - Full ID of the subnet resource. Required if I(name) and I(virtual_network_name) are not provided.
                    name:
                        description:
                            - Name of the subnet. Only used if I(virtual_network_name) is also provided.
                    virtual_network_name:
                        description:
                            - Name of the virtual network. Only used if I(name) is also provided.
            public_ip_address:
                description:
                    - Reference of the PublicIP resource.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    frontend_ports:
        description:
            - List of frontend ports of the application gateway resource.
        suboptions:
            port:
                description:
                    - Frontend port.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    backend_address_pools:
        description:
            - List of backend address pool of the application gateway resource.
        suboptions:
            backend_addresses:
                description:
                    - List of backend addresses.
                suboptions:
                    fqdn:
                        description:
                            - Fully qualified domain name (FQDN).
                    ip_address:
                        description:
                            - IP address.
            name:
                description:
                    - Resource that is unique within a resource group. This name can be used to access the resource.
    probes:
        description:
            - Probes available to the application gateway resource.
        suboptions:
            name:
                description:
                    - Name of the I(probe) that is unique within an Application Gateway.
            protocol:
                description:
                    - The protocol used for the I(probe).
                choices:
                    - 'http'
                    - 'https'
            host:
                description:
                    - Host name to send the I(probe) to.
            path:
                description:
                    - Relative path of I(probe).
                    - Valid path starts from '/'.
                    - Probe is sent to <Protocol>://<host>:<port><path>.
            timeout:
                description:
                    - The probe timeout in seconds.
                    - Probe marked as failed if valid response is not received with this timeout period.
                    - Acceptable values are from 1 second to 86400 seconds.
            interval:
                description:
                    - The probing interval in seconds.
                    - This is the time interval between two consecutive probes.
                    - Acceptable values are from 1 second to 86400 seconds.
            unhealthy_threshold:
                description:
                    - The I(probe) retry count.
                    - Backend server is marked down after consecutive probe failure count reaches UnhealthyThreshold.
                    - Acceptable values are from 1 second to 20.
            pick_host_name_from_backend_http_settings:
                description:
                    - Whether host header should be picked from the host name of the backend HTTP settings. Default value is false.
                type: bool
                default: False
    backend_http_settings_collection:
        description:
            - Backend http settings of the application gateway resource.
        suboptions:
            probe:
                description:
                    - Probe resource of an application gateway.
            port:
                description:
                    - The destination port on the backend.
            protocol:
                description:
                    - The protocol used to communicate with the backend.
                choices:
                    - 'http'
                    - 'https'
            cookie_based_affinity:
                description:
                    - Cookie based affinity.
                choices:
                    - 'enabled'
                    - 'disabled'
            request_timeout:
                description:
                    - Request timeout in seconds.
                    - Application Gateway will fail the request if response is not received within RequestTimeout.
                    - Acceptable values are from 1 second to 86400 seconds.
            authentication_certificates:
                description:
                    - List of references to application gateway authentication certificates.
                    - Applicable only when C(cookie_based_affinity) is enabled, otherwise quietly ignored.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            host_name:
                description:
                    - Host header to be sent to the backend servers.
            pick_host_name_from_backend_address:
                description:
                    - Whether host header should be picked from the host name of the backend server. Default value is false.
            affinity_cookie_name:
                description:
                    - Cookie name to use for the affinity cookie.
            path:
                description:
                    - Path which should be used as a prefix for all C(http) requests.
                    - Null means no path will be prefixed. Default value is null.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    http_listeners:
        description:
            - List of HTTP listeners of the application gateway resource.
        suboptions:
            frontend_ip_configuration:
                description:
                    - Frontend IP configuration resource of an application gateway.
            frontend_port:
                description:
                    - Frontend port resource of an application gateway.
            protocol:
                description:
                    - Protocol of the C(http) listener.
                choices:
                    - 'http'
                    - 'https'
            host_name:
                description:
                    - Host name of C(http) listener.
            ssl_certificate:
                description:
                    - SSL certificate resource of an application gateway.
            require_server_name_indication:
                description:
                    - Applicable only if I(protocol) is C(https). Enables SNI for multi-hosting.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
    url_path_maps:
        description:
            - List of URL path maps of the application gateway resource.
        suboptions:
            name:
                description:
                    - Name of the resource that is unique within the application gateway. This name can be used to access the resource.
            default_backend_address_pool:
                description:
                    - Backend address pool resource of the application gateway which will be used if no path matches occur.
                    - Mutually exclusive with I(default_redirect_configuration).
            default_backend_http_settings:
                description:
                    - Backend http settings resource of the application gateway; used with I(default_backend_address_pool).
            path_rules:
                description:
                    - List of URL path rules.
                suboptions:
                    name:
                        description:
                            - Name of the resource that is unique within the path map.
                    backend_address_pool:
                        description:
                            - Backend address pool resource of the application gateway which will be used if the path is matched.
                            - Mutually exclusive with I(redirect_configuration).
                    backend_http_settings:
                        description:
                            - Backend http settings resource of the application gateway; used for the path's I(backend_address_pool).
                    redirect_configuration:
                        description:
                            - Name of redirect configuration resource of the application gateway which will be used if the path is matched.
                            - Mutually exclusive with I(backend_address_pool).
                        version_added: "1.10.0"
                    paths:
                        description:
                            - List of paths.
            default_redirect_configuration:
                description:
                    - Name of redirect configuration resource of the application gateway which will be used if no path matches occur.
                    - Mutually exclusive with I(default_backend_address_pool).
                version_added: "1.10.0"
    request_routing_rules:
        description:
            - List of request routing rules of the application gateway resource.
        suboptions:
            rule_type:
                description:
                    - Rule type.
                choices:
                    - 'basic'
                    - 'path_based_routing'
            backend_address_pool:
                description:
                    - Backend address pool resource of the application gateway. Not used if I(rule_type) is C(path_based_routing).
            backend_http_settings:
                description:
                    - Backend C(http) settings resource of the application gateway.
            http_listener:
                description:
                    - Http listener resource of the application gateway.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            redirect_configuration:
                description:
                    - Redirect configuration resource of the application gateway.
            url_path_map:
                description:
                    - URL path map resource of the application gateway. Required if I(rule_type) is C(path_based_routing).
    gateway_state:
        description:
            - Start or Stop the application gateway. When specified, no updates will occur to the gateway.
        type: str
        choices:
            - started
            - stopped
    state:
        description:
            - Assert the state of the application gateway. Use C(present) to create or update and C(absent) to delete.
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Create instance of Application Gateway
  azure_rm_appgateway:
    resource_group: myResourceGroup
    name: myAppGateway
    sku:
      name: standard_small
      tier: standard
      capacity: 2
    gateway_ip_configurations:
      - subnet:
          id: "{{ subnet_id }}"
        name: app_gateway_ip_config
    frontend_ip_configurations:
      - subnet:
          id: "{{ subnet_id }}"
        name: sample_gateway_frontend_ip_config
    frontend_ports:
      - port: 90
        name: ag_frontend_port
    backend_address_pools:
      - backend_addresses:
          - ip_address: 10.0.0.4
        name: test_backend_address_pool
    backend_http_settings_collection:
      - port: 80
        protocol: http
        cookie_based_affinity: enabled
        name: sample_appgateway_http_settings
    http_listeners:
      - frontend_ip_configuration: sample_gateway_frontend_ip_config
        frontend_port: ag_frontend_port
        name: sample_http_listener
    request_routing_rules:
      - rule_type: Basic
        backend_address_pool: test_backend_address_pool
        backend_http_settings: sample_appgateway_http_settings
        http_listener: sample_http_listener
        name: rule1

- name: Create instance of Application Gateway by looking up virtual network and subnet
  azure_rm_appgateway:
    resource_group: myResourceGroup
    name: myAppGateway
    sku:
      name: standard_small
      tier: standard
      capacity: 2
    gateway_ip_configurations:
      - subnet:
          name: default
          virtual_network_name: my-vnet
        name: app_gateway_ip_config
    frontend_ip_configurations:
      - subnet:
          name: default
          virtual_network_name: my-vnet
        name: sample_gateway_frontend_ip_config
    frontend_ports:
      - port: 90
        name: ag_frontend_port
    backend_address_pools:
      - backend_addresses:
          - ip_address: 10.0.0.4
        name: test_backend_address_pool
    backend_http_settings_collection:
      - port: 80
        protocol: http
        cookie_based_affinity: enabled
        name: sample_appgateway_http_settings
    http_listeners:
      - frontend_ip_configuration: sample_gateway_frontend_ip_config
        frontend_port: ag_frontend_port
        name: sample_http_listener
    request_routing_rules:
      - rule_type: Basic
        backend_address_pool: test_backend_address_pool
        backend_http_settings: sample_appgateway_http_settings
        http_listener: sample_http_listener
        name: rule1

- name: Create instance of Application Gateway with path based rules
  azure_rm_appgateway:
    resource_group: myResourceGroup
    name: myAppGateway
    sku:
      name: standard_small
      tier: standard
      capacity: 2
    gateway_ip_configurations:
      - subnet:
          id: "{{ subnet_id }}"
        name: app_gateway_ip_config
    frontend_ip_configurations:
      - subnet:
          id: "{{ subnet_id }}"
        name: sample_gateway_frontend_ip_config
    frontend_ports:
      - port: 90
        name: ag_frontend_port
    backend_address_pools:
      - backend_addresses:
          - ip_address: 10.0.0.4
        name: test_backend_address_pool
    backend_http_settings_collection:
      - port: 80
        protocol: http
        cookie_based_affinity: enabled
        name: sample_appgateway_http_settings
    http_listeners:
      - frontend_ip_configuration: sample_gateway_frontend_ip_config
        frontend_port: ag_frontend_port
        name: sample_http_listener
    request_routing_rules:
      - rule_type: path_based_routing
        http_listener: sample_http_listener
        name: rule1
        url_path_map: path_mappings
    url_path_maps:
      - name: path_mappings
        default_backend_address_pool: test_backend_address_pool
        default_backend_http_settings: sample_appgateway_http_settings
        path_rules:
          - name: path_rules
            backend_address_pool: test_backend_address_pool
            backend_http_settings: sample_appgateway_http_settings
            paths:
              - "/abc"
              - "/123/*"

- name: Create instance of Application Gateway with complex routing and redirect rules
  azure_rm_appgateway:
    resource_group: myResourceGroup
    name: myComplexAppGateway
    sku:
      name: standard_small
      tier: standard
      capacity: 2
    ssl_policy:
      policy_type: "predefined"
      policy_name: "ssl_policy20170401_s"
    ssl_certificates:
      - name: ssl_cert
        password: your-password
        data: "{{ lookup('file', 'certfile') }}"
    gateway_ip_configurations:
      - subnet:
          id: "{{ subnet_output.state.id }}"
          name: app_gateway_ip_config
    frontend_ip_configurations:
      - subnet:
          id: "{{ subnet_output.state.id }}"
          name: sample_gateway_frontend_ip_config
    frontend_ports:
      - name: "inbound-http"
        port: 80
      - name: "inbound-https"
        port: 443
    backend_address_pools:
      - name: test_backend_address_pool1
        backend_addresses:
          - ip_address: 10.0.0.1
      - name: test_backend_address_pool2
        backend_addresses:
          - ip_address: 10.0.0.2
    backend_http_settings_collection:
      - name: "http-profile1"
        port: 443
        protocol: https
        pick_host_name_from_backend_address: true
        probe: "http-probe1"
        cookie_based_affinity: "Disabled"
      - name: "http-profile2"
        port: 8080
        protocol: http
        pick_host_name_from_backend_address: true
        probe: "http-probe2"
        cookie_based_affinity: "Disabled"
    http_listeners:
      - name: "inbound-http"
        protocol: "http"
        frontend_ip_configuration: "sample_gateway_frontend_ip_config"
        frontend_port: "inbound-http"
      - name: "inbound-traffic1"
        protocol: "https"
        frontend_ip_configuration: "sample_gateway_frontend_ip_config"
        frontend_port: "inbound-https"
        host_name: "traffic1.example.com"
        require_server_name_indication: true
        ssl_certificate: "ssl_cert"
      - name: "inbound-traffic2"
        protocol: "https"
        frontend_ip_configuration: "sample_gateway_frontend_ip_config"
        frontend_port: "inbound-https"
        host_name: "traffic2.example.com"
        require_server_name_indication: true
        ssl_certificate: "ssl_cert"
    url_path_maps:
      - name: "path_mappings"
        default_redirect_configuration: "redirect-traffic1"
        path_rules:
          - name: "path_rules"
            backend_address_pool: "test_backend_address_pool1"
            backend_http_settings: "http-profile1"
            paths:
              - "/abc"
              - "/123/*"
    request_routing_rules:
      - name: "app-routing1"
        rule_type: "basic"
        http_listener: "inbound-traffic1"
        backend_address_pool: "test_backend_address_pool2"
        backend_http_settings: "http-profile1"
      - name: "app-routing2"
        rule_type: "path_based_routing"
        http_listener: "inbound-traffic2"
        url_path_map: "path_mappings"
      - name: "redirect-routing"
        rule_type: "basic"
        http_listener: "inbound-http"
        redirect_configuration: "redirect-http"
    probes:
      - name: "http-probe1"
        interval: 30
        path: "/abc"
        protocol: "https"
        pick_host_name_from_backend_http_settings: true
        timeout: 30
        unhealthy_threshold: 2
      - name: "http-probe2"
        interval: 30
        path: "/xyz"
        protocol: "http"
        pick_host_name_from_backend_http_settings: true
        timeout: 30
        unhealthy_threshold: 2
    redirect_configurations:
      - name: "redirect-http"
        redirect_type: "permanent"
        target_listener: "inbound-traffic1"
        include_path: true
        include_query_string: true
        request_routing_rules:
          - "redirect-routing"
      - name: "redirect-traffic1"
        redirect_type: "found"
        target_listener: "inbound-traffic1"
        include_path: true
        include_query_string: true
        url_path_maps:
          - "path_mappings"

- name: Stop an Application Gateway instance
  azure_rm_appgateway:
    resource_group: myResourceGroup
    name: myAppGateway
    gateway_state: stopped

- name: Start an Application Gateway instance
  azure_rm_appgateway:
    resource_group: myResourceGroup
    name: myAppGateway
    gateway_state: started
'''

RETURN = '''
id:
    description:
        - Application gateway resource ID.
    returned: always
    type: str
    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/applicationGateways/myAppGw
name:
    description:
        - Name of application gateway.
    returned: always
    type: str
    sample: myAppGw
resource_group:
    description:
        - Name of resource group.
    returned: always
    type: str
    sample: myResourceGroup
location:
    description:
        - Location of application gateway.
    returned: always
    type: str
    sample: centralus
operational_state:
    description:
        - Operating state of application gateway.
    returned: always
    type: str
    sample: Running
provisioning_state:
    description:
        - Provisioning state of application gateway.
    returned: always
    type: str
    sample: Succeeded
'''

import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from copy import deepcopy
from ansible.module_utils.common.dict_transformations import (
    _snake_to_camel, dict_merge,
)

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrestazure.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete, Start, Stop = range(6)


sku_spec = dict(
    capacity=dict(type='int'),
    name=dict(type='str', choices=['standard_small', 'standard_medium', 'standard_large', 'standard_v2', 'waf_medium', 'waf_large', 'waf_v2']),
    tier=dict(type='str', choices=['standard', 'standard_v2', 'waf', 'waf_v2']),
)


ssl_policy_spec = dict(
    disabled_ssl_protocols=dict(type='list'),
    policy_type=dict(type='str', choices=['predefined', 'custom']),
    policy_name=dict(type='str', choices=['ssl_policy20150501', 'ssl_policy20170401', 'ssl_policy20170401_s']),
    cipher_suites=dict(type='list'),
    min_protocol_version=dict(type='str', choices=['tls_v1_0', 'tls_v1_1', 'tls_v1_2'])
)


probe_spec = dict(
    host=dict(type='str'),
    interval=dict(type='int'),
    name=dict(type='str'),
    path=dict(type='str'),
    protocol=dict(type='str', choices=['http', 'https']),
    timeout=dict(type='int'),
    unhealthy_threshold=dict(type='int'),
    pick_host_name_from_backend_http_settings=dict(type='bool', default=False)
)


redirect_path_rules_spec = dict(
    name=dict(type='str'),
    path_map_name=dict(type='str'),
)


redirect_configuration_spec = dict(
    include_path=dict(type='bool'),
    include_query_string=dict(type='bool'),
    name=dict(type='str'),
    redirect_type=dict(type='str', choices=['permanent', 'found', 'see_other', 'temporary']),
    target_listener=dict(type='str'),
    request_routing_rules=dict(type='list', elements='str'),
    url_path_maps=dict(type='list', elements='str'),
    path_rules=dict(type='list', elements='dict', options=redirect_path_rules_spec),
)


path_rules_spec = dict(
    name=dict(type='str'),
    backend_address_pool=dict(type='str'),
    backend_http_settings=dict(type='str'),
    redirect_configuration=dict(type='str'),
    paths=dict(type='list', elements='str'),
)


url_path_maps_spec = dict(
    name=dict(type='str'),
    default_backend_address_pool=dict(type='str'),
    default_backend_http_settings=dict(type='str'),
    path_rules=dict(
        type='list',
        elements='dict',
        options=path_rules_spec,
        mutually_exclusive=[('backend_address_pool', 'redirect_configuration')],
        required_one_of=[('backend_address_pool', 'redirect_configuration')],
        required_together=[('backend_address_pool', 'backend_http_settings')],
    ),
    default_redirect_configuration=dict(type='str'),
)


class AzureRMApplicationGateways(AzureRMModuleBase):
    """Configuration class for an Azure RM Application Gateway resource"""

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
            sku=dict(
                type='dict',
                options=sku_spec,
            ),
            ssl_policy=dict(
                type='dict',
                options=ssl_policy_spec
            ),
            gateway_ip_configurations=dict(
                type='list'
            ),
            authentication_certificates=dict(
                type='list'
            ),
            ssl_certificates=dict(
                type='list'
            ),
            redirect_configurations=dict(
                type='list',
                elements='dict',
                options=redirect_configuration_spec
            ),
            frontend_ip_configurations=dict(
                type='list'
            ),
            frontend_ports=dict(
                type='list'
            ),
            backend_address_pools=dict(
                type='list'
            ),
            backend_http_settings_collection=dict(
                type='list'
            ),
            probes=dict(
                type='list',
                elements='dict',
                options=probe_spec
            ),
            http_listeners=dict(
                type='list'
            ),
            url_path_maps=dict(
                type='list',
                elements='dict',
                options=url_path_maps_spec,
                mutually_exclusive=[('default_backend_address_pool', 'default_redirect_configuration')],
                required_one_of=[('default_backend_address_pool', 'default_redirect_configuration')],
                required_together=[('default_backend_address_pool', 'default_backend_http_settings')],
            ),
            request_routing_rules=dict(
                type='list'
            ),
            gateway_state=dict(
                type='str',
                choices=['started', 'stopped'],
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.gateway_state = None
        self.to_do = Actions.NoAction

        super(AzureRMApplicationGateways, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "id":
                    self.parameters["id"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'standard_small':
                            ev['name'] = 'Standard_Small'
                        elif ev['name'] == 'standard_medium':
                            ev['name'] = 'Standard_Medium'
                        elif ev['name'] == 'standard_large':
                            ev['name'] = 'Standard_Large'
                        elif ev['name'] == 'standard_v2':
                            ev['name'] = 'Standard_v2'
                        elif ev['name'] == 'waf_medium':
                            ev['name'] = 'WAF_Medium'
                        elif ev['name'] == 'waf_large':
                            ev['name'] = 'WAF_Large'
                        elif ev['name'] == 'waf_v2':
                            ev['name'] = 'WAF_v2'
                    if 'tier' in ev:
                        if ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                        if ev['tier'] == 'standard_v2':
                            ev['tier'] = 'Standard_v2'
                        elif ev['tier'] == 'waf':
                            ev['tier'] = 'WAF'
                        elif ev['tier'] == 'waf_v2':
                            ev['tier'] = 'WAF_v2'
                    self.parameters["sku"] = ev
                elif key == "ssl_policy":
                    ev = kwargs[key]
                    if 'policy_type' in ev:
                        ev['policy_type'] = _snake_to_camel(ev['policy_type'], True)
                    if 'policy_name' in ev:
                        if ev['policy_name'] == 'ssl_policy20150501':
                            ev['policy_name'] = 'AppGwSslPolicy20150501'
                        elif ev['policy_name'] == 'ssl_policy20170401':
                            ev['policy_name'] = 'AppGwSslPolicy20170401'
                        elif ev['policy_name'] == 'ssl_policy20170401_s':
                            ev['policy_name'] = 'AppGwSslPolicy20170401S'
                    if 'min_protocol_version' in ev:
                        if ev['min_protocol_version'] == 'tls_v1_0':
                            ev['min_protocol_version'] = 'TLSv1_0'
                        elif ev['min_protocol_version'] == 'tls_v1_1':
                            ev['min_protocol_version'] = 'TLSv1_1'
                        elif ev['min_protocol_version'] == 'tls_v1_2':
                            ev['min_protocol_version'] = 'TLSv1_2'
                    if 'disabled_ssl_protocols' in ev:
                        protocols = ev['disabled_ssl_protocols']
                        if protocols is not None:
                            for i in range(len(protocols)):
                                if protocols[i] == 'tls_v1_0':
                                    protocols[i] = 'TLSv1_0'
                                elif protocols[i] == 'tls_v1_1':
                                    protocols[i] = 'TLSv1_1'
                                elif protocols[i] == 'tls_v1_2':
                                    protocols[i] = 'TLSv1_2'
                    if 'cipher_suites' in ev:
                        suites = ev['cipher_suites']
                        if suites is not None:
                            for i in range(len(suites)):
                                suites[i] = suites[i].upper()
                elif key == "gateway_ip_configurations":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'subnet' in item and 'name' in item['subnet'] and 'virtual_network_name' in item['subnet']:
                            id = subnet_id(self.subscription_id,
                                           kwargs['resource_group'],
                                           item['subnet']['virtual_network_name'],
                                           item['subnet']['name'])
                            item['subnet'] = {'id': id}
                    self.parameters["gateway_ip_configurations"] = kwargs[key]
                elif key == "authentication_certificates":
                    self.parameters["authentication_certificates"] = kwargs[key]
                elif key == "ssl_certificates":
                    self.parameters["ssl_certificates"] = kwargs[key]
                elif key == "redirect_configurations":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'redirect_type' in item:
                            item['redirect_type'] = _snake_to_camel(item['redirect_type'], True)
                        if 'target_listener' in item:
                            id = http_listener_id(self.subscription_id,
                                                  kwargs['resource_group'],
                                                  kwargs['name'],
                                                  item['target_listener'])
                            item['target_listener'] = {'id': id}
                        if item['request_routing_rules']:
                            for j in range(len(item['request_routing_rules'])):
                                rule_name = item['request_routing_rules'][j]
                                id = request_routing_rule_id(self.subscription_id,
                                                             kwargs['resource_group'],
                                                             kwargs['name'],
                                                             rule_name)
                                item['request_routing_rules'][j] = {'id': id}
                        else:
                            del item['request_routing_rules']
                        if item['url_path_maps']:
                            for j in range(len(item['url_path_maps'])):
                                pathmap_name = item['url_path_maps'][j]
                                id = url_path_map_id(self.subscription_id,
                                                     kwargs['resource_group'],
                                                     kwargs['name'],
                                                     pathmap_name)
                                item['url_path_maps'][j] = {'id': id}
                        else:
                            del item['url_path_maps']
                        if item['path_rules']:
                            for j in range(len(item['path_rules'])):
                                pathrule = item['path_rules'][j]
                                if 'name' in pathrule and 'path_map_name' in pathrule:
                                    id = url_path_rule_id(self.subscription_id,
                                                          kwargs['resource_group'],
                                                          kwargs['name'],
                                                          pathrule['path_map_name'],
                                                          pathrule['name'])
                                    item['path_rules'][j] = {'id': id}
                        else:
                            del item['path_rules']
                    self.parameters["redirect_configurations"] = ev
                elif key == "frontend_ip_configurations":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'private_ip_allocation_method' in item:
                            item['private_ip_allocation_method'] = _snake_to_camel(item['private_ip_allocation_method'], True)
                        if 'public_ip_address' in item:
                            id = public_ip_id(self.subscription_id,
                                              kwargs['resource_group'],
                                              item['public_ip_address'])
                            item['public_ip_address'] = {'id': id}
                        if 'subnet' in item and 'name' in item['subnet'] and 'virtual_network_name' in item['subnet']:
                            id = subnet_id(self.subscription_id,
                                           kwargs['resource_group'],
                                           item['subnet']['virtual_network_name'],
                                           item['subnet']['name'])
                            item['subnet'] = {'id': id}
                    self.parameters["frontend_ip_configurations"] = ev
                elif key == "frontend_ports":
                    self.parameters["frontend_ports"] = kwargs[key]
                elif key == "backend_address_pools":
                    self.parameters["backend_address_pools"] = kwargs[key]
                elif key == "probes":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        if 'pick_host_name_from_backend_http_settings' in item and item['pick_host_name_from_backend_http_settings'] and 'host' in item:
                            del item['host']
                    self.parameters["probes"] = ev
                elif key == "backend_http_settings_collection":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        if 'cookie_based_affinity' in item:
                            item['cookie_based_affinity'] = _snake_to_camel(item['cookie_based_affinity'], True)
                        if 'probe' in item:
                            id = probe_id(self.subscription_id,
                                          kwargs['resource_group'],
                                          kwargs['name'],
                                          item['probe'])
                            item['probe'] = {'id': id}
                    self.parameters["backend_http_settings_collection"] = ev
                elif key == "http_listeners":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'frontend_ip_configuration' in item:
                            id = frontend_ip_configuration_id(self.subscription_id,
                                                              kwargs['resource_group'],
                                                              kwargs['name'],
                                                              item['frontend_ip_configuration'])
                            item['frontend_ip_configuration'] = {'id': id}

                        if 'frontend_port' in item:
                            id = frontend_port_id(self.subscription_id,
                                                  kwargs['resource_group'],
                                                  kwargs['name'],
                                                  item['frontend_port'])
                            item['frontend_port'] = {'id': id}
                        if 'ssl_certificate' in item:
                            id = ssl_certificate_id(self.subscription_id,
                                                    kwargs['resource_group'],
                                                    kwargs['name'],
                                                    item['ssl_certificate'])
                            item['ssl_certificate'] = {'id': id}
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        ev[i] = item
                    self.parameters["http_listeners"] = ev
                elif key == "url_path_maps":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if item['default_backend_address_pool']:
                            id = backend_address_pool_id(self.subscription_id,
                                                         kwargs['resource_group'],
                                                         kwargs['name'],
                                                         item['default_backend_address_pool'])
                            item['default_backend_address_pool'] = {'id': id}
                        else:
                            del item['default_backend_address_pool']
                        if item['default_backend_http_settings']:
                            id = backend_http_settings_id(self.subscription_id,
                                                          kwargs['resource_group'],
                                                          kwargs['name'],
                                                          item['default_backend_http_settings'])
                            item['default_backend_http_settings'] = {'id': id}
                        else:
                            del item['default_backend_http_settings']
                        if 'path_rules' in item:
                            ev2 = item['path_rules']
                            for j in range(len(ev2)):
                                item2 = ev2[j]
                                if item2['backend_address_pool']:
                                    id = backend_address_pool_id(self.subscription_id,
                                                                 kwargs['resource_group'],
                                                                 kwargs['name'],
                                                                 item2['backend_address_pool'])
                                    item2['backend_address_pool'] = {'id': id}
                                else:
                                    del item2['backend_address_pool']
                                if item2['backend_http_settings']:
                                    id = backend_http_settings_id(self.subscription_id,
                                                                  kwargs['resource_group'],
                                                                  kwargs['name'],
                                                                  item2['backend_http_settings'])
                                    item2['backend_http_settings'] = {'id': id}
                                else:
                                    del item2['backend_http_settings']
                                if item2['redirect_configuration']:
                                    id = redirect_configuration_id(self.subscription_id,
                                                                   kwargs['resource_group'],
                                                                   kwargs['name'],
                                                                   item2['redirect_configuration'])
                                    item2['redirect_configuration'] = {'id': id}
                                else:
                                    del item2['redirect_configuration']
                                ev2[j] = item2
                        if item['default_redirect_configuration']:
                            id = redirect_configuration_id(self.subscription_id,
                                                           kwargs['resource_group'],
                                                           kwargs['name'],
                                                           item['default_redirect_configuration'])
                            item['default_redirect_configuration'] = {'id': id}
                        else:
                            del item['default_redirect_configuration']
                        ev[i] = item
                    self.parameters["url_path_maps"] = ev
                elif key == "request_routing_rules":
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'rule_type' in item and item['rule_type'] == 'path_based_routing' and 'backend_address_pool' in item:
                            del item['backend_address_pool']
                        if 'backend_address_pool' in item:
                            id = backend_address_pool_id(self.subscription_id,
                                                         kwargs['resource_group'],
                                                         kwargs['name'],
                                                         item['backend_address_pool'])
                            item['backend_address_pool'] = {'id': id}
                        if 'backend_http_settings' in item:
                            id = backend_http_settings_id(self.subscription_id,
                                                          kwargs['resource_group'],
                                                          kwargs['name'],
                                                          item['backend_http_settings'])
                            item['backend_http_settings'] = {'id': id}
                        if 'http_listener' in item:
                            id = http_listener_id(self.subscription_id,
                                                  kwargs['resource_group'],
                                                  kwargs['name'],
                                                  item['http_listener'])
                            item['http_listener'] = {'id': id}
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        if 'rule_type' in item:
                            item['rule_type'] = _snake_to_camel(item['rule_type'], True)
                        if 'redirect_configuration' in item:
                            id = redirect_configuration_id(self.subscription_id,
                                                           kwargs['resource_group'],
                                                           kwargs['name'],
                                                           item['redirect_configuration'])
                            item['redirect_configuration'] = {'id': id}
                        if 'url_path_map' in item:
                            id = url_path_map_id(self.subscription_id,
                                                 kwargs['resource_group'],
                                                 kwargs['name'],
                                                 item['url_path_map'])
                            item['url_path_map'] = {'id': id}
                        ev[i] = item
                    self.parameters["request_routing_rules"] = ev
                elif key == "etag":
                    self.parameters["etag"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_applicationgateway()

        if not old_response:
            self.log("Application Gateway instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Application Gateway instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Application Gateway instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Update):
            if (old_response['operational_state'] == 'Stopped' and self.gateway_state == 'started'):
                self.to_do = Actions.Start
            elif (old_response['operational_state'] == 'Running' and self.gateway_state == 'stopped'):
                self.to_do = Actions.Stop
            elif ((old_response['operational_state'] == 'Stopped' and self.gateway_state == 'stopped') or
                  (old_response['operational_state'] == 'Running' and self.gateway_state == 'started')):
                self.to_do = Actions.NoAction
            elif (self.parameters['location'] != old_response['location'] or
                    self.parameters['sku']['name'] != old_response['sku']['name'] or
                    self.parameters['sku']['tier'] != old_response['sku']['tier'] or
                    self.parameters['sku']['capacity'] != old_response['sku']['capacity'] or
                    not compare_arrays(old_response, self.parameters, 'authentication_certificates') or
                    not compare_arrays(old_response, self.parameters, 'gateway_ip_configurations') or
                    not compare_arrays(old_response, self.parameters, 'redirect_configurations') or
                    not compare_arrays(old_response, self.parameters, 'frontend_ip_configurations') or
                    not compare_arrays(old_response, self.parameters, 'frontend_ports') or
                    not compare_arrays(old_response, self.parameters, 'backend_address_pools') or
                    not compare_arrays(old_response, self.parameters, 'probes') or
                    not compare_arrays(old_response, self.parameters, 'backend_http_settings_collection') or
                    not compare_arrays(old_response, self.parameters, 'request_routing_rules') or
                    not compare_arrays(old_response, self.parameters, 'http_listeners') or
                    not compare_arrays(old_response, self.parameters, 'url_path_maps')):

                self.to_do = Actions.Update
            else:
                self.to_do = Actions.NoAction

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Application Gateway instance")

            if self.check_mode:
                self.results['changed'] = True
                self.results["parameters"] = self.parameters
                return self.results

            response = self.create_update_applicationgateway()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif (self.to_do == Actions.Start) or (self.to_do == Actions.Stop):
            self.log("Need to Start / Stop the Application Gateway instance")
            self.results['changed'] = True
            response = old_response

            if self.check_mode:
                return self.results
            elif self.to_do == Actions.Start:
                self.start_applicationgateway()
                response["operational_state"] = "Running"
            else:
                self.stop_applicationgateway()
                response["operational_state"] = "Stopped"

        elif self.to_do == Actions.Delete:
            self.log("Application Gateway instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_applicationgateway()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_applicationgateway():
                time.sleep(20)
        else:
            self.log("Application Gateway instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results.update(self.format_response(response))

        return self.results

    def create_update_applicationgateway(self):
        '''
        Creates or updates Application Gateway with the specified configuration.

        :return: deserialized Application Gateway instance state dictionary
        '''
        self.log("Creating / Updating the Application Gateway instance {0}".format(self.name))

        try:
            response = self.mgmt_client.application_gateways.create_or_update(resource_group_name=self.resource_group,
                                                                              application_gateway_name=self.name,
                                                                              parameters=self.parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Application Gateway instance.')
            self.fail("Error creating the Application Gateway instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_applicationgateway(self):
        '''
        Deletes specified Application Gateway instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Application Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.application_gateways.delete(resource_group_name=self.resource_group,
                                                                    application_gateway_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Application Gateway instance.')
            self.fail("Error deleting the Application Gateway instance: {0}".format(str(e)))

        return True

    def get_applicationgateway(self):
        '''
        Gets the properties of the specified Application Gateway.

        :return: deserialized Application Gateway instance state dictionary
        '''
        self.log("Checking if the Application Gateway instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.application_gateways.get(resource_group_name=self.resource_group,
                                                                 application_gateway_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Application Gateway instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Application Gateway instance.')
        if found is True:
            return response.as_dict()

        return False

    def start_applicationgateway(self):
        self.log("Starting the Application Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.application_gateways.start(resource_group_name=self.resource_group,
                                                                   application_gateway_name=self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except CloudError as e:
            self.log('Error attempting to start the Application Gateway instance.')
            self.fail("Error starting the Application Gateway instance: {0}".format(str(e)))

    def stop_applicationgateway(self):
        self.log("Stopping the Application Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.application_gateways.stop(resource_group_name=self.resource_group,
                                                                  application_gateway_name=self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except CloudError as e:
            self.log('Error attempting to stop the Application Gateway instance.')
            self.fail("Error stopping the Application Gateway instance: {0}".format(str(e)))

    def format_response(self, appgw_dict):
        id = appgw_dict.get("id")
        id_dict = parse_resource_id(id)
        d = {
            "id": id,
            "name": appgw_dict.get("name"),
            "resource_group": id_dict.get('resource_group', self.resource_group),
            "location": appgw_dict.get("location"),
            "operational_state": appgw_dict.get("operational_state"),
            "provisioning_state": appgw_dict.get("provisioning_state"),
        }
        return d


def public_ip_id(subscription_id, resource_group_name, name):
    """Generate the id for a frontend ip configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/publicIPAddresses/{2}'.format(
        subscription_id,
        resource_group_name,
        name
    )


def frontend_ip_configuration_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a frontend ip configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/frontendIPConfigurations/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def frontend_port_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a frontend port"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/frontendPorts/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def redirect_configuration_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a redirect configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/redirectConfigurations/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def ssl_certificate_id(subscription_id, resource_group_name, ssl_certificate_name, name):
    """Generate the id for a frontend port"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/sslCertificates/{3}'.format(
        subscription_id,
        resource_group_name,
        ssl_certificate_name,
        name
    )


def backend_address_pool_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for an address pool"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/backendAddressPools/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def probe_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a probe"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/probes/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def backend_http_settings_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a http settings"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/backendHttpSettingsCollection/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def http_listener_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a http listener"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/httpListeners/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def url_path_map_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a url path map"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/urlPathMaps/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def url_path_rule_id(subscription_id, resource_group_name, appgateway_name, url_path_map_name, name):
    """Generate the id for a url path map"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/urlPathMaps/{3}/pathRules/{4}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        url_path_map_name,
        name
    )


def subnet_id(subscription_id, resource_group_name, virtual_network_name, name):
    """Generate the id for a subnet in a virtual network"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/virtualNetworks/{2}/subnets/{3}'.format(
        subscription_id,
        resource_group_name,
        virtual_network_name,
        name
    )


def ip_configuration_id(subscription_id, resource_group_name, network_interface_name, name):
    """Generate the id for a request routing rule in an application gateway"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/networkInterfaces/{2}/ipConfigurations/{3}'.format(
        subscription_id,
        resource_group_name,
        network_interface_name,
        name
    )


def request_routing_rule_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a request routing rule in an application gateway"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/requestRoutingRules/{3}'.format(
        subscription_id,
        resource_group_name,
        appgateway_name,
        name
    )


def compare_arrays(old_params, new_params, param_name):
    old = old_params.get(param_name) or []
    new = new_params.get(param_name) or []

    oldd = array_to_dict(old)
    newd = array_to_dict(new)

    newd = dict_merge(oldd, newd)
    return newd == oldd


def array_to_dict(array):
    '''Converts list object to dictionary object, including any nested properties on elements.'''
    new = {}
    for index, item in enumerate(array):
        new[index] = deepcopy(item)
        if isinstance(item, dict):
            for nested in item:
                if isinstance(item[nested], list):
                    new[index][nested] = array_to_dict(item[nested])
    return new


def main():
    """Main execution"""
    AzureRMApplicationGateways()


if __name__ == '__main__':
    main()

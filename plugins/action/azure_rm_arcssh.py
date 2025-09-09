# Copyright (c) 2024 Bill Peck  <bpeck@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible_collections.azure.azcollection.plugins.plugin_utils import (file_utils, ssh_info, connectivity_utils)
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMAuth
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AZURE_COMMON_ARGS
try:
    from azure.core.exceptions import ClientAuthenticationError, ResourceExistsError, ResourceNotFoundError
except ImportError:
    pass


display = Display()


class ActionModule(ActionBase):
    ''' Configures ssh proxy for connecting to ARC hosts '''

    TRANSFERS_FILES = False
    BYPASS_HOST_LOOP = True

    def __init__(self, *args, **kwargs):
        if not connectivity_utils.HAS_ORAS:
            raise AnsibleActionFail("oras.client is not installed.", orig_exc=connectivity_utils.HAS_ORAS_EXC)
        super(ActionModule, self).__init__(*args, **kwargs)

    def run(self, tmp=None, task_vars=None):
        ''' run the pause action module '''
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        merged_arg_spec = dict()
        merged_arg_spec.update(AZURE_COMMON_ARGS)
        merged_arg_spec.update(
            {
                'inventory_hostname': {'type': 'str'},
                'ansible_host': {'type': 'str'},
                'resource_group': {'type': 'str'},
                'resource_type': {'type': 'str'},
                'private_key_file': {'type': 'str'},
                'local_user': {'type': 'str'},
                'port': {'type': 'int'},
                'ssh_config_file': {'type': 'str'},
                'ssh_relay_file': {'type': 'str'},
                'ssh_proxy_folder': {'type': 'str'}
            }
        )

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec=merged_arg_spec,
        )

        auth_source = os.environ.get('ANSIBLE_AZURE_AUTH_SOURCE', None) or new_module_args.get('auth_source')
        auth_options = dict(
            auth_source=auth_source,
            profile=new_module_args.get('profile'),
            subscription_id=new_module_args.get('subscription_id'),
            client_id=new_module_args.get('client_id'),
            secret=new_module_args.get('secret'),
            tenant=new_module_args.get('tenant'),
            ad_user=new_module_args.get('ad_user'),
            password=new_module_args.get('password'),
            cloud_environment=new_module_args.get('cloud_environment'),
            cert_validation_mode=new_module_args.get('cert_validation_mode'),
            api_profile=new_module_args.get('api_profile'),
            track1_cred=True,
            adfs_authority_url=new_module_args.get('adfs_authority_url')
        )

        inventory_hostname = new_module_args.get('inventory_hostname')
        ansible_host = new_module_args.get('ansible_host')
        resource_group = new_module_args.get('resource_group')
        resource_type = new_module_args.get('resource_type')
        private_key_file = new_module_args.get('private_key_file')
        local_user = new_module_args.get('local_user')
        port = new_module_args.get('port')
        ssh_config_file = new_module_args.get('ssh_config_file')
        ssh_relay_file = new_module_args.get('ssh_relay_file')
        ssh_proxy_folder = new_module_args.get('ssh_proxy_folder')
        result.update(dict(
            changed=False,
            rc=0,
            stderr='',
            stdout=''
        ))

        ########################################################################
        # Begin the hard work!

        azure_auth = AzureRMAuth(**auth_options)
        rest_client = GenericRestClient(azure_auth.azure_credential_track2,
                                        azure_auth.subscription_id,
                                        azure_auth._cloud_environment.endpoints.resource_manager,
                                        credential_scopes=[azure_auth._cloud_environment.endpoints.resource_manager + ".default"])
        # Define error_map with common http error codes
        rest_client.error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
        }

        config_session = ssh_info.ConfigSession(ssh_config_file,
                                                ssh_relay_file,
                                                resource_group,
                                                inventory_hostname,
                                                ansible_host,
                                                private_key_file,
                                                local_user,
                                                port,
                                                resource_type,
                                                ssh_proxy_folder)

        try:
            cert_lifetime = None  # If set to None we default to the max which is 1 hour
            config_session.proxy_path = connectivity_utils.install_client_side_proxy(config_session.ssh_proxy_folder)
            (config_session.relay_info,
             config_session.new_service_config) = connectivity_utils.get_relay_information(rest_client,
                                                                                           azure_auth.subscription_id,
                                                                                           config_session.resource_group_name,
                                                                                           config_session.hostname,
                                                                                           config_session.resource_type,
                                                                                           cert_lifetime,
                                                                                           config_session.port)
        except Exception as e:
            raise AnsibleActionFail("Failed to get relay information.", orig_exc=e)

        config_text = config_session.get_config_text()
        ssh_config_path = config_session.ssh_config_file

        ssh_config_dir = os.path.dirname(ssh_config_path)
        if not os.path.isdir(ssh_config_dir):
            os.makedirs(ssh_config_dir)

        file_utils.write_to_file(ssh_config_path,
                                 'w',
                                 '\n'.join(config_text),
                                 f"Couldn't write ssh config to file {ssh_config_path}.",
                                 'utf-8')

        result['stdout'] = "SSH proxy configured for %s in %s" % (inventory_hostname, config_session.ssh_config_file)
        return result

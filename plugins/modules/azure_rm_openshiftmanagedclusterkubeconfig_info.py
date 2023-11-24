#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang <haiyzhan@micosoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_openshiftmanagedclusterkubeconfig_info
version_added: '1.17.0'
short_description: Get admin kubeconfig of Azure Red Hat OpenShift Managed Cluster
description:
    - get kubeconfig of Azure Red Hat OpenShift Managed Cluster instance.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Resource name.
        required: true
        type: str
    path:
        description:
            - Destination filepath of kubeconfig file
        required: false
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Maxim Babushkin (@maxbab)
'''

EXAMPLES = '''
- name: Obtain kubeconfig file of ARO cluster
  azure_rm_openshiftmanagedclusterkubeconfig_info:
    name: myCluster
    resource_group: myResourceGroup
  register: kubeconf

- name: Print registered kubeconfig file
  debug:
    msg: "{{ kubeconf['kubeconfig'] }}"

- name: Fetch kubeconfig and save it as mycluster_kubeconfig filename
  azure_rm_openshiftmanagedclusterkubeconfig_info:
    name: myCluster
    resource_group: myResourceGroup
    path: ./files/mycluster_kubeconfig

- name: Fetch kubeconfig and save it to specified directory (file will be named as kubeconfig by default)
  azure_rm_openshiftmanagedclusterkubeconfig_info:
    name: myCluster
    resource_group: myResourceGroup
    path: ./files/
'''

RETURN = '''
kubeconfig:
    description:
        - kubeconfig value
    returned: always
    type: str
'''

import base64
import filecmp
import json
import os
import tempfile
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOpenShiftManagedClustersKubeconfigInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str', required=True
            ),
            name=dict(
                type='str', required=True
            ),
            path=dict(
                type='str', required=False
            )
        )

        self.resource_group = None
        self.name = None
        self.path = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2021-09-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMOpenShiftManagedClustersKubeconfigInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient, is_track2=True,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        self.results = self.get_kubeconfig()
        if self.path and self.path_is_valid():
            self.write_kubeconfig_to_file()
        return self.results

    def get_kubeconfig(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.RedHatOpenShift' +
                    '/openShiftClusters' +
                    '/{{ cluster_name }}' +
                    '/listAdminCredentials')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ cluster_name }}', self.name)
        self.log("Fetch for kubeconfig from the cluster.")
        try:
            response = self.mgmt_client.query(self.url,
                                              'POST',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.body())
        except Exception as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')
        return self.format_item(results)

    def format_item(self, item):
        d = {
            'kubeconfig': item.get('kubeconfig'),
        }
        return d

    def path_is_valid(self):
        if not os.path.basename(self.path):
            if os.path.isdir(self.path):
                self.log("Path is dir. Appending file name.")
                self.path += "kubeconfig"
            else:
                try:
                    self.log('Attempting to makedirs {0}'.format(self.path))
                    os.makedirs(self.path)
                except IOError as exc:
                    self.fail("Failed to create directory {0} - {1}".format(self.path, str(exc)))
                self.path += "kubeconfig"
        else:
            file_name = os.path.basename(self.path)
            path = self.path.replace(file_name, '')
            self.log('Checking path {0}'. format(path))
            # If the "path" is not defined, it's cwd.
            if path and not os.path.isdir(path):
                try:
                    self.log('Attempting to makedirs {0}'. format(path))
                    os.makedirs(path)
                except IOError as exc:
                    self.fail("Failed to create directory {0} - {1}".format(path, str(exc)))
        self.log("Validated path - {0}". format(self.path))
        return True

    def write_kubeconfig_to_file(self):
        decoded_bytes = base64.b64decode(self.results['kubeconfig'])
        decoded_string = decoded_bytes.decode("utf-8")

        if os.path.exists(self.path):
            self.log('Existing kubeconfig file found. Compare, to decide if needs to override')
            # If kubeconfig file already exists, compare it with the new file
            # If equal, do nothing, otherwise, override.
            tmp_kubeconfig = tempfile.TemporaryFile(mode='w')
            tmp_kubeconfig.write(decoded_string)
            tmp_kubeconfig.seek(0)

            # No need to close the temp file as it's closed by filecmp.cmp.
            if filecmp.cmp(tmp_kubeconfig.name, self.path):
                self.log("Files are identical. No need to override.")
                self.results['changed'] = False
                return

        self.log("Create {0} kubeconfig file.".format(self.path))
        try:
            with open(self.path, "w") as file:
                file.write(decoded_string)
        except Exception as exc:
            self.fail("Failed to write kubeconfig output to file - {0} to {1} - {2}".format(self.results['kubeconfig'],
                                                                                            self.path, exc))
        self.log("The {0} kubeconfig file has been created.")
        self.results['changed'] = True
        return


def main():
    AzureRMOpenShiftManagedClustersKubeconfigInfo()


if __name__ == '__main__':
    main()

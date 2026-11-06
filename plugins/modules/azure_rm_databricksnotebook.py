#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_databricksnotebook
version_added: "4.3.0"
short_description: Import, export, or remove Databricks notebooks
description:
    - Transfer notebook source between the Ansible controller and an Azure Databricks workspace.
    - Supports SOURCE, HTML, JUPYTER, and DBC formats.
options:
    resource_group:
        description: Resource group containing the workspace.
        required: true
        type: str
    workspace_name:
        description: Azure Databricks workspace name.
        required: true
        type: str
    path:
        description: Absolute path of the notebook in the workspace.
        required: true
        type: str
    state:
        description: Import a local notebook, export it to the controller, or remove it.
        type: str
        choices: [present, exported, absent]
        default: present
    source:
        description: Local source file to import. Required when I(state=present).
        type: path
    dest:
        description: Local destination file to write. Required when I(state=exported).
        type: path
    format:
        description: Notebook format.
        type: str
        choices: [SOURCE, HTML, JUPYTER, DBC]
        default: SOURCE
    language:
        description: Notebook language. Required by the workspace for SOURCE format.
        type: str
        choices: [SCALA, PYTHON, SQL, R]
    overwrite:
        description: Replace a different existing notebook on import.
        type: bool
        default: true
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Import a Python notebook
  azure.azcollection.azure_rm_databricksnotebook:
    resource_group: analytics
    workspace_name: analytics-workspace
    path: /Shared/etl
    source: files/etl.py
    language: PYTHON

- name: Export a notebook to the controller
  azure.azcollection.azure_rm_databricksnotebook:
    resource_group: analytics
    workspace_name: analytics-workspace
    path: /Shared/etl
    state: exported
    dest: /tmp/etl.py
    language: PYTHON
'''

RETURN = '''
notebook:
    description: Workspace notebook metadata, when available.
    returned: when I(state=present) or I(state=exported)
    type: dict
    sample: {"path": "/Shared/etl", "object_type": "NOTEBOOK", "language": "PYTHON"}
'''

import base64
import hashlib
import os
from urllib.parse import urlencode

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks import databricks_request


class AzureRMDatabricksNotebook(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            workspace_name=dict(type='str', required=True),
            path=dict(type='str', required=True),
            state=dict(type='str', choices=['present', 'exported', 'absent'], default='present'),
            source=dict(type='path'),
            dest=dict(type='path'),
            format=dict(type='str', choices=['SOURCE', 'HTML', 'JUPYTER', 'DBC'], default='SOURCE'),
            language=dict(type='str', choices=['SCALA', 'PYTHON', 'SQL', 'R']),
            overwrite=dict(type='bool', default=True),
        )
        super(AzureRMDatabricksNotebook, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        if not self.path.startswith('/'):
            self.fail('path must be an absolute workspace path')
        if self.state == 'present' and not self.source:
            self.fail('source is required when state is present')
        if self.state == 'exported' and not self.dest:
            self.fail('dest is required when state is exported')
        if self.format == 'SOURCE' and not self.language and self.state != 'absent':
            self.fail('language is required when format is SOURCE')

        try:
            workspace = self.databricks_client.workspaces.get(self.resource_group, self.workspace_name)
        except ResourceNotFoundError:
            self.fail('Databricks workspace {0} was not found'.format(self.workspace_name))
        except Exception as exc:
            self.fail('Error retrieving Databricks workspace {0}: {1}'.format(self.workspace_name, exc))
        workspace_url = getattr(workspace, 'workspace_url', None)
        if not workspace_url:
            self.fail('Databricks workspace {0} did not return a workspace URL'.format(self.workspace_name))
        host = 'https://' + workspace_url
        query = urlencode(dict(path=self.path, format=self.format))

        if self.state == 'exported':
            exported = databricks_request(self, host, '/api/2.0/workspace/export?' + query)
            content = base64.b64decode(exported['content'])
            current = None
            if os.path.exists(self.dest):
                with open(self.dest, 'rb') as stream:
                    current = stream.read()
            changed = current != content
            if changed and not self.check_mode:
                parent = os.path.dirname(self.dest)
                if parent and not os.path.isdir(parent):
                    os.makedirs(parent)
                with open(self.dest, 'wb') as stream:
                    stream.write(content)
            return dict(changed=changed, notebook=dict(path=self.path, dest=self.dest,
                                                       sha256=hashlib.sha256(content).hexdigest()))

        status = databricks_request(self, host, '/api/2.0/workspace/get-status?' + urlencode({'path': self.path}),
                                    allow_not_found=True)
        if self.state == 'absent':
            if status and not self.check_mode:
                databricks_request(self, host, '/api/2.0/workspace/delete?' + urlencode({'path': self.path}), 'POST')
            return dict(changed=status is not None)

        with open(self.source, 'rb') as stream:
            content = stream.read()
        encoded = base64.b64encode(content).decode('ascii')
        if status:
            current = databricks_request(self, host, '/api/2.0/workspace/export?' + query)
            current_content = base64.b64decode(current['content'])
            changed = current_content != content
            if not changed:
                return dict(changed=False, notebook=status)
            if not self.overwrite:
                self.fail('Notebook {0} exists and overwrite is false'.format(self.path))
        else:
            changed = True
        if changed and not self.check_mode:
            body = dict(path=self.path, format=self.format, content=encoded, overwrite=self.overwrite)
            if self.language:
                body['language'] = self.language
            result = databricks_request(self, host, '/api/2.0/workspace/import', 'POST', body)
        else:
            result = dict(path=self.path)
        return dict(changed=changed, notebook=result)


def main():
    AzureRMDatabricksNotebook()


if __name__ == '__main__':
    main()

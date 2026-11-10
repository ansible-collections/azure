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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks import (
    databricks_request,
    databricks_workspace_host,
)

NOTEBOOK_SOURCE_HEADER = b'# Databricks notebook source'


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

        self.resource_group = None
        self.workspace_name = None
        self.path = None
        self.state = None
        self.source = None
        self.dest = None
        self.format = None
        self.language = None
        self.overwrite = None

        self.results = dict(changed=False)
        self.host = None

        super(AzureRMDatabricksNotebook, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            required_if=[
                ('state', 'present', ('source',)),
                ('state', 'exported', ('dest',)),
            ],
            supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        # The language check cannot be expressed with required_if because it
        # only applies to imports and exports, not to state=absent.
        if not self.path.startswith('/'):
            self.fail('path must be an absolute workspace path')
        if self.format == 'SOURCE' and not self.language and self.state != 'absent':
            self.fail('language is required when format is SOURCE')

        self.host = databricks_workspace_host(self, self.resource_group, self.workspace_name)

        if self.state == 'exported':
            return self.export_notebook()

        status = self._status()
        if self.state == 'absent':
            return self.delete_notebook(status)

        return self.import_notebook(status)

    def export_notebook(self):
        exported = databricks_request(self, self.host, '/api/2.0/workspace/export?' + self._query())
        content = base64.b64decode(exported['content'])
        current = None
        if os.path.exists(self.dest):
            with open(self.dest, 'rb') as stream:
                current = stream.read()
        self.results['changed'] = current != content
        if self.results['changed'] and not self.check_mode:
            parent = os.path.dirname(self.dest)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent)
            with open(self.dest, 'wb') as stream:
                stream.write(content)
        self.results['notebook'] = dict(path=self.path, dest=self.dest,
                                        sha256=hashlib.sha256(content).hexdigest())
        return self.results

    def delete_notebook(self, status):
        if status is not None:
            self.results['changed'] = True
            if not self.check_mode:
                databricks_request(self, self.host,
                                   '/api/2.0/workspace/delete?' + urlencode({'path': self.path}), 'POST')
        return self.results

    def import_notebook(self, status):
        with open(self.source, 'rb') as stream:
            content = stream.read()
        if status is not None:
            current = databricks_request(self, self.host, '/api/2.0/workspace/export?' + self._query())
            self.results['changed'] = self._content_changed(base64.b64decode(current['content']), content)
            if not self.results['changed']:
                self.results['notebook'] = status
                return self.results
            if not self.overwrite:
                self.fail('Notebook {0} exists and overwrite is false'.format(self.path))
        else:
            self.results['changed'] = True
        if self.check_mode:
            self.results['notebook'] = dict(path=self.path)
            return self.results
        body = dict(path=self.path, format=self.format,
                    content=base64.b64encode(content).decode('ascii'), overwrite=self.overwrite)
        if self.language:
            body['language'] = self.language
        self.results['notebook'] = databricks_request(self, self.host, '/api/2.0/workspace/import', 'POST', body)
        return self.results

    def _status(self):
        return databricks_request(self, self.host,
                                  '/api/2.0/workspace/get-status?' + urlencode({'path': self.path}),
                                  allow_not_found=True)

    def _content_changed(self, current, content):
        """Compare notebook content, ignoring the SOURCE-format notebook header.

        Databricks adds the header to every SOURCE-format export even when
        the imported file did not have one, so comparing raw bytes would
        report a change on every run.
        """
        if self.format != 'SOURCE':
            return current != content
        return self._without_source_header(current) != self._without_source_header(content)

    def _without_source_header(self, content):
        if not content.startswith(NOTEBOOK_SOURCE_HEADER):
            return content
        content = content[len(NOTEBOOK_SOURCE_HEADER):]
        if content[:2] == b'\r\n':
            return content[2:]
        if content[:1] == b'\n':
            return content[1:]
        return content

    def _query(self):
        return urlencode(dict(path=self.path, format=self.format))


def main():
    AzureRMDatabricksNotebook()


if __name__ == '__main__':
    main()

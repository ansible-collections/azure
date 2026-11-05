# Copyright (c) 2026
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Helpers for Azure Databricks workspace data-plane APIs."""

import json
from urllib.error import HTTPError

from ansible.module_utils.urls import open_url


ADB_RESOURCE_ID = '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d'


def databricks_request(module, workspace_url, path, method='GET', body=None, allow_not_found=False):
    """Call the Databricks REST API using the module's Azure identity."""
    token = module.azure_auth.azure_credential_track2.get_token(
        ADB_RESOURCE_ID + '/.default').token
    url = workspace_url.rstrip('/') + path
    data = json.dumps(body).encode('utf-8') if body is not None else None
    try:
        response = open_url(
            url,
            data=data,
            headers={
                'Authorization': 'Bearer {0}'.format(token),
                'Content-Type': 'application/json',
            },
            method=method,
            validate_certs=module.validate_certs,
            timeout=module.module.params.get('polling_timeout', 60) or 60,
        )
        status = response.code
        content = response.read()
    except HTTPError as exc:
        status = exc.code
        content = exc.read()
        if status == 404 and allow_not_found:
            return None
    except Exception as exc:
        module.fail('Error calling Databricks API {0}: {1}'.format(path, exc))
    if status < 200 or status >= 300:
        message = content.decode('utf-8', errors='replace') if content else 'HTTP {0}'.format(status)
        module.fail('Databricks API {0} {1} failed: {2}'.format(method, path, message))
    if not content:
        return {}
    return json.loads(content.decode('utf-8'))

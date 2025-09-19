# Copyright (c) 2018 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


try:
    from ansible.module_utils.ansible_release import __version__ as ANSIBLE_VERSION
except Exception:
    ANSIBLE_VERSION = 'unknown'

try:
    from azure.core._pipeline_client import PipelineClient
    from azure.core.polling import LROPoller
    from azure.core.pipeline import PipelineResponse
    from azure.core.pipeline.policies import BearerTokenCredentialPolicy, UserAgentPolicy
    from azure.mgmt.core.polling.arm_polling import ARMPolling
    import uuid
    from azure.core.configuration import Configuration
except ImportError:
    # This is handled in azure_rm_common
    Configuration = object

ANSIBLE_USER_AGENT = 'Ansible/{0}'.format(ANSIBLE_VERSION)


class GenericRestClientConfiguration(Configuration):

    def __init__(self, credential, subscription_id, credential_scopes=None, base_url=None):

        if credential is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        if subscription_id is None:
            raise ValueError("Parameter 'subscription_id' must not be None.")
        if not base_url:
            base_url = 'https://management.azure.com'
        if not credential_scopes:
            credential_scopes = 'https://management.azure.com/.default'

        super(GenericRestClientConfiguration, self).__init__()

        self.user_agent_policy = UserAgentPolicy(ANSIBLE_USER_AGENT)
        self.credentials = credential
        self.subscription_id = subscription_id
        self.authentication_policy = BearerTokenCredentialPolicy(credential, credential_scopes)


class GenericRestClient(object):

    def __init__(self, credential, subscription_id, base_url=None, credential_scopes=None):
        self._config = GenericRestClientConfiguration(credential, subscription_id, credential_scopes[0])
        self._client = PipelineClient(base_url, config=self._config)
        self.models = None

        # Support http errors by status code
        self.error_map = {}

    def query(self, url, method, query_parameters, header_parameters, body, expected_status_codes, polling_timeout, polling_interval):
        # Construct and send request
        operation_config = {}

        request = None

        if header_parameters is None:
            header_parameters = {}

        header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())

        if method == 'GET':
            request = self._client.get(url, query_parameters, header_parameters, body)
        elif method == 'PUT':
            request = self._client.put(url, query_parameters, header_parameters, body)
        elif method == 'POST':
            request = self._client.post(url, query_parameters, header_parameters, body)
        elif method == 'HEAD':
            request = self._client.head(url, query_parameters, header_parameters, body)
        elif method == 'PATCH':
            request = self._client.patch(url, query_parameters, header_parameters, body)
        elif method == 'DELETE':
            request = self._client.delete(url, query_parameters, header_parameters, body)
        elif method == 'MERGE':
            request = self._client.merge(url, query_parameters, header_parameters, body)

        response = self._client.send_request(request, **operation_config)

        if response.status_code not in expected_status_codes:
            return self.on_error(response)

        elif response.status_code == 202 and polling_timeout > 0:
            def get_long_running_output(response):
                return response
            poller = LROPoller(self._client,
                               PipelineResponse(None, response, None),
                               get_long_running_output,
                               ARMPolling(polling_interval, **operation_config))
            response = self.get_poller_result(poller, polling_timeout)

        return response

    def get_poller_result(self, poller, timeout):
        try:
            poller.wait(timeout=timeout)
            return poller.result()
        except Exception as exc:
            raise

    def on_error(self, response):
        """ handle errors in response
        """
        # raise common http errors
        error_type = self.error_map.get(response.status_code)
        if error_type:
            raise error_type(response=response)
        raise SendRequestException(response.text(), response.status_code)


class SendRequestException(Exception):
    def __init__(self, response, status_code):
        self.response = response
        self.status_code = status_code

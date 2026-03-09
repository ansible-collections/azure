# -*- coding: utf-8 -*-

# Copyright: (c) 2016 Matt Davis, <mdavis@ansible.com>
# Copyright: (c) 2016 Chris Houseknecht, <house@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    # Azure doc fragment
    DOCUMENTATION = r'''
options:
    subscription_id:
        description:
            - Your Azure subscription Id.
        type: str
        env:
          - name: AZURE_SUBSCRIPTION_ID
    client_id:
        description:
            - Azure client ID. Use when authenticating with a Service Principal or Managed Identity (msi).
            - Can also be set via the C(AZURE_CLIENT_ID) environment variable.
        type: str
        env:
          - name: AZURE_CLIENT_ID
    secret:
        description:
            - Azure client secret. Use when authenticating with a Service Principal.
        type: str
        env:
          - name: AZURE_SECRET
    tenant:
        description:
            - Azure tenant ID. Use when authenticating with a Service Principal.
        type: str
        env:
          - name: AZURE_TENANT
    cloud_environment:
        description:
            - For cloud environments other than the US public cloud, the environment name (as defined by Azure Python SDK, eg, C(AzureChinaCloud),
              C(AzureUSGovernment)), or a resource manager URL (required for Azure Stack). Can also be set via credential file profile or
              the C(AZURE_CLOUD_ENVIRONMENT) environment variable. If setting to a URL, you must also set the ARM_CLOUD_METADATA_URL if the cloud
              is not registered with azcli.
        type: str
        default: AzureCloud
        version_added: '0.0.1'
        env:
          - name: AZURE_CLOUD_ENVIRONMENT
    auth_source:
        description:
            - Controls the source of the credentials to use for authentication.
            - Can also be set via the C(ANSIBLE_AZURE_AUTH_SOURCE) environment variable.
            - When set to C(auto) (the default) the precedence is module parameters, then C(env), then C(credential_file), then C(cli).
            - When set to C(env), the credentials will be read from the environment variables
            - When set to C(credential_file), it will read the profile from C(~/.azure/credentials).
            - When set to C(cli), the credentials will be sources from the Azure CLI profile. C(subscription_id) or the environment variable
              C(AZURE_SUBSCRIPTION_ID) can be used to identify the subscription ID if more than one is present otherwise the default
              az cli subscription is used.
            - When set to C(msi), the host machine must be an azure resource with an enabled MSI extension. C(subscription_id) or the
              environment variable C(AZURE_SUBSCRIPTION_ID) can be used to identify the subscription ID if the resource is granted
              access to more than one subscription, otherwise the first subscription is chosen.
            - The C(msi) was added in Ansible 2.6.
            - When set to C(workload_identity), authentication uses a federated OIDC token file, typically provided by Azure DevOps Workload Identity
              or AKS.
            - When set to C(oidc), authentication uses OIDC request URL and request token, typically provided by GitHub Actions.
        type: str
        default: auto
        choices:
        - auto
        - cli
        - env
        - msi
        - workload_identity
        - oidc
        env:
          - name: ANSIBLE_AZURE_AUTH_SOURCE
requirements:
    - python >= 2.7
    - The host that executes this module must have the azure.azcollection collection installed via galaxy
    - All python packages listed in collection's requirements.txt must be installed via pip on the host that executes modules from azure.azcollection
    - Full installation instructions may be found https://galaxy.ansible.com/azure/azcollection

notes:
    - For authentication with Azure you can pass parameters, set environment variables, use a profile stored
      in C(~/.azure/credentials), or log in before you run your tasks or playbook with C(az login).
    - Authentication is also possible using a service principal or Active Directory user.
    - To authenticate via service principal, pass subscription_id, client_id, secret and tenant or set environment
      variables AZURE_SUBSCRIPTION_ID, AZURE_CLIENT_ID, AZURE_SECRET and AZURE_TENANT.
    - To authenticate via Active Directory user, pass ad_user and password, or set AZURE_AD_USER and
      AZURE_PASSWORD in the environment.
    - "Alternatively, credentials can be stored in ~/.azure/credentials. This is an ini file containing
      a [default] section and the following keys: subscription_id, client_id, secret and tenant or
      subscription_id, ad_user and password. It is also possible to add additional profiles. Specify the profile
      by passing profile or setting AZURE_PROFILE in the environment."
    - Authentication using workload identity federation is supported without client secrets.
    - To authenticate using Azure DevOps Workload Identity Federation or AKS, set C(auth_source=workload_identity) and ensure the C(AZURE_CLIENT_ID),
      C(AZURE_TENANT), C(AZURE_SUBSCRIPTION_ID), and C(AZURE_FEDERATED_TOKEN_FILE) are present.
    - To authenticate using GitHub Actions OIDC, set C(auth_source=oidc) and ensure the C(ACTIONS_ID_TOKEN_REQUEST_URL)
      and C(ACTIONS_ID_TOKEN_REQUEST_TOKEN), along with C(AZURE_CLIENT_ID), C(AZURE_TENANT), and C(AZURE_SUBSCRIPTION_ID) are present.
    - The OIDC token is exchanged for an Azure access token at runtime and is not persisted.

seealso:
    - name: Sign in with Azure CLI
      link: https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest
      description: How to authenticate using the C(az login) command.
    '''

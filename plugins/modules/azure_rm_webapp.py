#!/usr/bin/python
#
# Copyright (c) 2018 Yunge Zhu, <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_webapp
version_added: "0.1.2"
short_description: Manage Web App instances
description:
    - Create, update and delete instance of Web App.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Unique name of the app to create or update. To create or update a deployment slot, use the {slot} parameter.
        required: True

    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.

    plan:
        description:
            - App service plan. Required for creation.
            - Can be name of existing app service plan in same resource group as web app.
            - Can be the resource ID of an existing app service plan. For example
              /subscriptions/<subs_id>/resourceGroups/<resource_group>/providers/Microsoft.Web/serverFarms/<plan_name>.
            - Can be a dict containing five parameters, defined below.
            - C(name), name of app service plan.
            - C(resource_group), resource group of the app service plan.
            - C(sku), SKU of app service plan, allowed values listed on U(https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).
            - C(is_linux), whether or not the app service plan is Linux. defaults to C(False).
            - C(number_of_workers), number of workers for app service plan.

    frameworks:
        description:
            - Set of run time framework settings. Each setting is a dictionary.
            - See U(https://docs.microsoft.com/en-us/azure/app-service/app-service-web-overview) for more info.
        suboptions:
            name:
                description:
                    - Name of the framework.
                    - Supported framework list for Windows web app and Linux web app is different.
                    - Windows web apps support C(java), C(net_framework), C(php), C(python), and C(node) from June 2018.
                    - Windows web apps support multiple framework at the same time.
                    - Linux web apps support C(java), C(ruby), C(php), C(dotnetcore), and C(node) from June 2018.
                    - Linux web apps support only one framework.
                    - Java framework is mutually exclusive with others.
                choices:
                    - java
                    - net_framework
                    - php
                    - python
                    - ruby
                    - dotnetcore
                    - node
            version:
                description:
                    - Version of the framework. For Linux web app supported value, see U(https://aka.ms/linux-stacks) for more info.
                    - C(net_framework) supported value sample, C(v4.0) for .NET 4.6 and C(v3.0) for .NET 3.5.
                    - C(php) supported value sample, C(5.5), C(5.6), C(7.0).
                    - C(python) supported value sample, C(5.5), C(5.6), C(7.0).
                    - C(node) supported value sample, C(6.6), C(6.9).
                    - C(dotnetcore) supported value sample, C(1.0), C(1.1), C(1.2).
                    - C(ruby) supported value sample, C(2.3).
                    - C(java) supported value sample, C(1.9) for Windows web app. C(1.8) for Linux web app.
            settings:
                description:
                    - List of settings of the framework.
                suboptions:
                    java_container:
                        description:
                            - Name of Java container.
                            - Supported only when I(frameworks=java). Sample values C(Tomcat), C(Jetty).
                    java_container_version:
                        description:
                            - Version of Java container.
                            - Supported only when I(frameworks=java).
                            - Sample values for C(Tomcat), C(8.0), C(8.5), C(9.0). For C(Jetty,), C(9.1), C(9.3).

    container_settings:
        description:
            - Web app container settings.
        suboptions:
            name:
                description:
                    - Name of the container, for example C(imagename:tag).
                    - To create a multi-container app, the name should be 'COMPOSE|' or 'KUBE|' followed by base64 encoded configuration.
            registry_server_url:
                description:
                    - Container registry server URL, for example C(mydockerregistry.io).
            registry_server_user:
                description:
                    - The container registry server user name.
            registry_server_password:
                description:
                    - The container registry server password.

    scm_type:
        description:
            - Repository type of deployment source, for example C(LocalGit), C(GitHub).
            - List of supported values maintained at U(https://docs.microsoft.com/en-us/rest/api/appservice/webapps/createorupdate#scmtype).

    deployment_source:
        description:
            - Deployment source for git.
        suboptions:
            url:
                description:
                    - Repository url of deployment source.

            branch:
                description:
                    - The branch name of the repository.
    startup_file:
        description:
            - The web's startup file.
            - Used only for Linux web apps.

    client_affinity_enabled:
        description:
            - Whether or not to send session affinity cookies, which route client requests in the same session to the same instance.
        type: bool
        default: True

    https_only:
        description:
            - Configures web site to accept only https requests.
        type: bool

    dns_registration:
        description:
            - Whether or not the web app hostname is registered with DNS on creation. Set to C(false) to register.
        type: bool

    skip_custom_domain_verification:
        description:
            - Whether or not to skip verification of custom (non *.azurewebsites.net) domains associated with web app. Set to C(true) to skip.
        type: bool

    ttl_in_seconds:
        description:
            - Time to live in seconds for web app default domain name.

    app_settings:
        description:
            - Configure web app application settings. Suboptions are in key value pair format.

    purge_app_settings:
        description:
            - Purge any existing application settings. Replace web app application settings with app_settings.
        type: bool
        default: False

    app_state:
        description:
            - Start/Stop/Restart the web app.
        type: str
        choices:
            - started
            - stopped
            - restarted
        default: started

    state:
        description:
            - State of the Web App.
            - Use C(present) to create or update a Web App and C(absent) to delete it.
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Yunge Zhu (@yungezz)

'''

EXAMPLES = '''
    - name: Create a windows web app with non-exist app service plan
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myWinWebapp
        plan:
          resource_group: myAppServicePlan_rg
          name: myAppServicePlan
          is_linux: false
          sku: S1

    - name: Create a docker web app with some app settings, with docker image
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myDockerWebapp
        plan:
          resource_group: myAppServicePlan_rg
          name: myAppServicePlan
          is_linux: true
          sku: S1
          number_of_workers: 2
        app_settings:
          testkey: testvalue
          testkey2: testvalue2
        container_settings:
          name: ansible/ansible:ubuntu1404

    - name: Create a docker web app with private acr registry
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myDockerWebapp
        plan: myAppServicePlan
        app_settings:
          testkey: testvalue
        container_settings:
          name: ansible/ubuntu1404
          registry_server_url: myregistry.io
          registry_server_user: user
          registry_server_password: pass

    - name: Create a multi-container web app
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myMultiContainerWebapp
        plan: myAppServicePlan
        app_settings:
          testkey: testvalue
        container_settings:
          name: "COMPOSE|{{ lookup('file', 'docker-compose.yml') | b64encode }}"

    - name: Create a linux web app with Node 6.6 framework
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myLinuxWebapp
        plan:
          resource_group: myAppServicePlan_rg
          name: myAppServicePlan
        app_settings:
          testkey: testvalue
        frameworks:
          - name: "node"
            version: "6.6"

    - name: Create a windows web app with node, php
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myWinWebapp
        plan:
          resource_group: myAppServicePlan_rg
          name: myAppServicePlan
        app_settings:
          testkey: testvalue
        frameworks:
          - name: "node"
            version: 6.6
          - name: "php"
            version: "7.0"

    - name: Create a stage deployment slot for an existing web app
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myWebapp/slots/stage
        plan:
          resource_group: myAppServicePlan_rg
          name: myAppServicePlan
        app_settings:
          testkey:testvalue

    - name: Create a linux web app with java framework
      azure_rm_webapp:
        resource_group: myResourceGroup
        name: myLinuxWebapp
        plan:
          resource_group: myAppServicePlan_rg
          name: myAppServicePlan
        app_settings:
          testkey: testvalue
        frameworks:
          - name: "java"
            version: "8"
            settings:
              java_container: "Tomcat"
              java_container_version: "8.5"
'''

RETURN = '''
azure_webapp:
    description:
        - ID of current web app.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Web/sites/myWebApp"
'''

import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrest.serialization import Model
    from azure.mgmt.web.models import (
        site_config, app_service_plan, Site,
        AppServicePlan, SkuDescription, NameValuePair
    )
except ImportError:
    # This is handled in azure_rm_common
    pass

container_settings_spec = dict(
    name=dict(type='str', required=True),
    registry_server_url=dict(type='str'),
    registry_server_user=dict(type='str'),
    registry_server_password=dict(type='str', no_log=True)
)

deployment_source_spec = dict(
    url=dict(type='str'),
    branch=dict(type='str')
)


framework_settings_spec = dict(
    java_container=dict(type='str', required=True),
    java_container_version=dict(type='str', required=True)
)


framework_spec = dict(
    name=dict(
        type='str',
        required=True,
        choices=['net_framework', 'java', 'php', 'node', 'python', 'dotnetcore', 'ruby']),
    version=dict(type='str', required=True),
    settings=dict(type='dict', options=framework_settings_spec)
)


def _normalize_sku(sku):
    if sku is None:
        return sku

    sku = sku.upper()
    if sku == 'FREE':
        return 'F1'
    elif sku == 'SHARED':
        return 'D1'
    return sku


def get_sku_name(tier):
    tier = tier.upper()
    if tier == 'F1' or tier == "FREE":
        return 'FREE'
    elif tier == 'D1' or tier == "SHARED":
        return 'SHARED'
    elif tier in ['B1', 'B2', 'B3', 'BASIC']:
        return 'BASIC'
    elif tier in ['S1', 'S2', 'S3']:
        return 'STANDARD'
    elif tier in ['P1', 'P2', 'P3']:
        return 'PREMIUM'
    elif tier in ['P1V2', 'P2V2', 'P3V2']:
        return 'PREMIUMV2'
    else:
        return None


def appserviceplan_to_dict(plan):
    return dict(
        id=plan.id,
        name=plan.name,
        kind=plan.kind,
        location=plan.location,
        reserved=plan.reserved,
        is_linux=plan.reserved,
        provisioning_state=plan.provisioning_state,
        tags=plan.tags if plan.tags else None
    )


def webapp_to_dict(webapp):
    return dict(
        id=webapp.id,
        name=webapp.name,
        location=webapp.location,
        client_cert_enabled=webapp.client_cert_enabled,
        enabled=webapp.enabled,
        reserved=webapp.reserved,
        client_affinity_enabled=webapp.client_affinity_enabled,
        server_farm_id=webapp.server_farm_id,
        host_names_disabled=webapp.host_names_disabled,
        https_only=webapp.https_only if hasattr(webapp, 'https_only') else None,
        skip_custom_domain_verification=webapp.skip_custom_domain_verification if hasattr(webapp, 'skip_custom_domain_verification') else None,
        ttl_in_seconds=webapp.ttl_in_seconds if hasattr(webapp, 'ttl_in_seconds') else None,
        state=webapp.state,
        tags=webapp.tags if webapp.tags else None
    )


class Actions:
    CreateOrUpdate, UpdateAppSettings, Delete = range(3)


class AzureRMWebApps(AzureRMModuleBase):
    """Configuration class for an Azure RM Web App resource"""

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
            plan=dict(
                type='raw'
            ),
            frameworks=dict(
                type='list',
                elements='dict',
                options=framework_spec
            ),
            container_settings=dict(
                type='dict',
                options=container_settings_spec
            ),
            scm_type=dict(
                type='str',
            ),
            deployment_source=dict(
                type='dict',
                options=deployment_source_spec
            ),
            startup_file=dict(
                type='str'
            ),
            client_affinity_enabled=dict(
                type='bool',
                default=True
            ),
            dns_registration=dict(
                type='bool'
            ),
            https_only=dict(
                type='bool'
            ),
            skip_custom_domain_verification=dict(
                type='bool'
            ),
            ttl_in_seconds=dict(
                type='int'
            ),
            app_settings=dict(
                type='dict'
            ),
            purge_app_settings=dict(
                type='bool',
                default=False
            ),
            app_state=dict(
                type='str',
                choices=['started', 'stopped', 'restarted'],
                default='started'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        mutually_exclusive = [['container_settings', 'frameworks']]

        self.resource_group = None
        self.name = None
        self.location = None

        # update in create_or_update as parameters
        self.client_affinity_enabled = True
        self.dns_registration = None
        self.skip_custom_domain_verification = None
        self.ttl_in_seconds = None
        self.https_only = None

        self.tags = None

        # site config, e.g app settings, ssl
        self.site_config = dict()
        self.app_settings = dict()
        self.app_settings_strDic = None

        # app service plan
        self.plan = None

        # siteSourceControl
        self.deployment_source = dict()

        # site, used at level creation, or update. e.g windows/linux, client_affinity etc first level args
        self.site = None

        # property for internal usage, not used for sdk
        self.container_settings = None

        self.purge_app_settings = False
        self.app_state = 'started'

        self.results = dict(
            changed=False,
            id=None,
        )
        self.state = None
        self.to_do = []

        self.frameworks = None

        # set site_config value from kwargs
        self.site_config_updatable_properties = ["net_framework_version",
                                                 "java_version",
                                                 "php_version",
                                                 "python_version",
                                                 "scm_type"]

        # updatable_properties
        self.updatable_properties = ["client_affinity_enabled",
                                     "force_dns_registration",
                                     "https_only",
                                     "skip_custom_domain_verification",
                                     "ttl_in_seconds"]

        self.supported_linux_frameworks = ['ruby', 'php', 'dotnetcore', 'node', 'java']
        self.supported_windows_frameworks = ['net_framework', 'php', 'python', 'node', 'java']

        super(AzureRMWebApps, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             mutually_exclusive=mutually_exclusive,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "scm_type":
                    self.site_config[key] = kwargs[key]

        old_response = None
        response = None
        to_be_updated = False

        # set location
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        # get existing web app
        old_response = self.get_webapp()

        if old_response:
            self.results['id'] = old_response['id']

        if self.state == 'present':
            if not self.plan and not old_response:
                self.fail("Please specify plan for newly created web app.")

            if not self.plan:
                self.plan = old_response['server_farm_id']

            self.plan = self.parse_resource_to_dict(self.plan)

            # get app service plan
            is_linux = False
            old_plan = self.get_app_service_plan()
            if old_plan:
                is_linux = old_plan['reserved']
            else:
                is_linux = self.plan['is_linux'] if 'is_linux' in self.plan else False

            if self.frameworks:
                # java is mutually exclusive with other frameworks
                if len(self.frameworks) > 1 and any(f['name'] == 'java' for f in self.frameworks):
                    self.fail('Java is mutually exclusive with other frameworks.')

                if is_linux:
                    if len(self.frameworks) != 1:
                        self.fail('Can specify one framework only for Linux web app.')

                    if self.frameworks[0]['name'] not in self.supported_linux_frameworks:
                        self.fail('Unsupported framework {0} for Linux web app.'.format(self.frameworks[0]['name']))

                    self.site_config['linux_fx_version'] = (self.frameworks[0]['name'] + '|' + self.frameworks[0]['version']).upper()

                    if self.frameworks[0]['name'] == 'java':
                        if self.frameworks[0]['version'] != '8':
                            self.fail("Linux web app only supports java 8.")
                        if self.frameworks[0]['settings'] and self.frameworks[0]['settings']['java_container'].lower() != 'tomcat':
                            self.fail("Linux web app only supports tomcat container.")

                        if self.frameworks[0]['settings'] and self.frameworks[0]['settings']['java_container'].lower() == 'tomcat':
                            self.site_config['linux_fx_version'] = 'TOMCAT|' + self.frameworks[0]['settings']['java_container_version'] + '-jre8'
                        else:
                            self.site_config['linux_fx_version'] = 'JAVA|8-jre8'
                else:
                    for fx in self.frameworks:
                        if fx.get('name') not in self.supported_windows_frameworks:
                            self.fail('Unsupported framework {0} for Windows web app.'.format(fx.get('name')))
                        else:
                            self.site_config[fx.get('name') + '_version'] = fx.get('version')

                        if 'settings' in fx and fx['settings'] is not None:
                            for key, value in fx['settings'].items():
                                self.site_config[key] = value

            if not self.app_settings:
                self.app_settings = dict()

            if self.container_settings:
                linux_fx_version = 'DOCKER|'

                if self.container_settings.get('registry_server_url'):
                    self.app_settings['DOCKER_REGISTRY_SERVER_URL'] = 'https://' + self.container_settings['registry_server_url']

                    linux_fx_version += self.container_settings['registry_server_url'] + '/'

                linux_fx_version += self.container_settings['name']

                # Use given name as is if it starts with allowed values of multi-container application
                if self.container_settings['name'].startswith('COMPOSE|') or self.container_settings['name'].startswith('KUBE|'):
                    linux_fx_version = self.container_settings['name']

                self.site_config['linux_fx_version'] = linux_fx_version

                if self.container_settings.get('registry_server_user'):
                    self.app_settings['DOCKER_REGISTRY_SERVER_USERNAME'] = self.container_settings['registry_server_user']

                if self.container_settings.get('registry_server_password'):
                    self.app_settings['DOCKER_REGISTRY_SERVER_PASSWORD'] = self.container_settings['registry_server_password']

            # init site
            self.site = Site(location=self.location, site_config=self.site_config)

            if self.https_only is not None:
                self.site.https_only = self.https_only

            if self.client_affinity_enabled:
                self.site.client_affinity_enabled = self.client_affinity_enabled

            # check if the web app already present in the resource group
            if not old_response:
                self.log("Web App instance doesn't exist")

                to_be_updated = True
                self.to_do.append(Actions.CreateOrUpdate)
                self.site.tags = self.tags

                # service plan is required for creation
                if not self.plan:
                    self.fail("Please specify app service plan in plan parameter.")

                if not old_plan:
                    # no existing service plan, create one
                    if (not self.plan.get('name') or not self.plan.get('sku')):
                        self.fail('Please specify name, is_linux, sku in plan')

                    if 'location' not in self.plan:
                        plan_resource_group = self.get_resource_group(self.plan['resource_group'])
                        self.plan['location'] = plan_resource_group.location

                    old_plan = self.create_app_service_plan()

                self.site.server_farm_id = old_plan['id']

                # if linux, setup startup_file
                if old_plan['is_linux']:
                    if hasattr(self, 'startup_file'):
                        self.site_config['app_command_line'] = self.startup_file

                # set app setting
                if self.app_settings:
                    app_settings = []
                    for key in self.app_settings.keys():
                        app_settings.append(NameValuePair(name=key, value=self.app_settings[key]))

                    self.site_config['app_settings'] = app_settings
            else:
                # existing web app, do update
                self.log("Web App instance already exists")

                self.log('Result: {0}'.format(old_response))

                update_tags, self.site.tags = self.update_tags(old_response.get('tags', None))

                if update_tags:
                    to_be_updated = True

                # check if root level property changed
                if self.is_updatable_property_changed(old_response):
                    to_be_updated = True
                    self.to_do.append(Actions.CreateOrUpdate)

                # check if site_config changed
                old_config = self.get_webapp_configuration()

                if self.is_site_config_changed(old_config):
                    to_be_updated = True
                    self.to_do.append(Actions.CreateOrUpdate)

                # check if linux_fx_version changed
                if old_config.linux_fx_version != self.site_config.get('linux_fx_version', ''):
                    to_be_updated = True
                    self.to_do.append(Actions.CreateOrUpdate)

                self.app_settings_strDic = self.list_app_settings()

                # purge existing app_settings:
                if self.purge_app_settings:
                    to_be_updated = True
                    self.app_settings_strDic = dict()
                    self.to_do.append(Actions.UpdateAppSettings)

                # check if app settings changed
                if self.purge_app_settings or self.is_app_settings_changed():
                    to_be_updated = True
                    self.to_do.append(Actions.UpdateAppSettings)

                    if self.app_settings:
                        for key in self.app_settings.keys():
                            self.app_settings_strDic[key] = self.app_settings[key]

        elif self.state == 'absent':
            if old_response:
                self.log("Delete Web App instance")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_webapp()

                self.log('Web App instance deleted')

            else:
                self.fail("Web app {0} not exists.".format(self.name))

        if to_be_updated:
            self.log('Need to Create/Update web app')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            if Actions.CreateOrUpdate in self.to_do:
                response = self.create_update_webapp()

                self.results['id'] = response['id']

            if Actions.UpdateAppSettings in self.to_do:
                update_response = self.update_app_settings()
                self.results['id'] = update_response.id

        webapp = None
        if old_response:
            webapp = old_response
        if response:
            webapp = response

        if webapp:
            if (webapp['state'] != 'Stopped' and self.app_state == 'stopped') or \
               (webapp['state'] != 'Running' and self.app_state == 'started') or \
               self.app_state == 'restarted':

                self.results['changed'] = True
                if self.check_mode:
                    return self.results

                self.set_webapp_state(self.app_state)

        return self.results

    # compare existing web app with input, determine weather it's update operation
    def is_updatable_property_changed(self, existing_webapp):
        for property_name in self.updatable_properties:
            if hasattr(self, property_name) and getattr(self, property_name) is not None and \
                    getattr(self, property_name) != existing_webapp.get(property_name, None):
                return True

        return False

    # compare xxx_version
    def is_site_config_changed(self, existing_config):
        for fx_version in self.site_config_updatable_properties:
            if self.site_config.get(fx_version):
                if not getattr(existing_config, fx_version) or \
                        getattr(existing_config, fx_version).upper() != self.site_config.get(fx_version).upper():
                    return True

        return False

    # comparing existing app setting with input, determine whether it's changed
    def is_app_settings_changed(self):
        if self.app_settings:
            if self.app_settings_strDic:
                for key in self.app_settings.keys():
                    if self.app_settings[key] != self.app_settings_strDic.get(key, None):
                        return True
            else:
                return True
        return False

    # comparing deployment source with input, determine wheather it's changed
    def is_deployment_source_changed(self, existing_webapp):
        if self.deployment_source:
            if self.deployment_source.get('url') \
                    and self.deployment_source['url'] != existing_webapp.get('site_source_control')['url']:
                return True

            if self.deployment_source.get('branch') \
                    and self.deployment_source['branch'] != existing_webapp.get('site_source_control')['branch']:
                return True

        return False

    def create_update_webapp(self):
        '''
        Creates or updates Web App with the specified configuration.

        :return: deserialized Web App instance state dictionary
        '''
        self.log(
            "Creating / Updating the Web App instance {0}".format(self.name))

        try:
            skip_dns_registration = self.dns_registration
            force_dns_registration = None if self.dns_registration is None else not self.dns_registration

            response = self.web_client.web_apps.create_or_update(resource_group_name=self.resource_group,
                                                                 name=self.name,
                                                                 site_envelope=self.site,
                                                                 skip_dns_registration=skip_dns_registration,
                                                                 skip_custom_domain_verification=self.skip_custom_domain_verification,
                                                                 force_dns_registration=force_dns_registration,
                                                                 ttl_in_seconds=self.ttl_in_seconds)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Web App instance.')
            self.fail(
                "Error creating the Web App instance: {0}".format(str(exc)))
        return webapp_to_dict(response)

    def delete_webapp(self):
        '''
        Deletes specified Web App instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Web App instance {0}".format(self.name))
        try:
            response = self.web_client.web_apps.delete(resource_group_name=self.resource_group,
                                                       name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Web App instance.')
            self.fail(
                "Error deleting the Web App instance: {0}".format(str(e)))

        return True

    def get_webapp(self):
        '''
        Gets the properties of the specified Web App.

        :return: deserialized Web App instance state dictionary
        '''
        self.log(
            "Checking if the Web App instance {0} is present".format(self.name))

        response = None

        try:
            response = self.web_client.web_apps.get(resource_group_name=self.resource_group,
                                                    name=self.name)

            # Newer SDK versions (0.40.0+) seem to return None if it doesn't exist instead of raising CloudError
            if response is not None:
                self.log("Response : {0}".format(response))
                self.log("Web App instance : {0} found".format(response.name))
                return webapp_to_dict(response)

        except CloudError as ex:
            pass

        self.log("Didn't find web app {0} in resource group {1}".format(
            self.name, self.resource_group))

        return False

    def get_app_service_plan(self):
        '''
        Gets app service plan
        :return: deserialized app service plan dictionary
        '''
        self.log("Get App Service Plan {0}".format(self.plan['name']))

        try:
            response = self.web_client.app_service_plans.get(
                resource_group_name=self.plan['resource_group'],
                name=self.plan['name'])

            # Newer SDK versions (0.40.0+) seem to return None if it doesn't exist instead of raising CloudError
            if response is not None:
                self.log("Response : {0}".format(response))
                self.log("App Service Plan : {0} found".format(response.name))

                return appserviceplan_to_dict(response)
        except CloudError as ex:
            pass

        self.log("Didn't find app service plan {0} in resource group {1}".format(
            self.plan['name'], self.plan['resource_group']))

        return False

    def create_app_service_plan(self):
        '''
        Creates app service plan
        :return: deserialized app service plan dictionary
        '''
        self.log("Create App Service Plan {0}".format(self.plan['name']))

        try:
            # normalize sku
            sku = _normalize_sku(self.plan['sku'])

            sku_def = SkuDescription(tier=get_sku_name(
                sku), name=sku, capacity=(self.plan.get('number_of_workers', None)))
            plan_def = AppServicePlan(
                location=self.plan['location'], app_service_plan_name=self.plan['name'], sku=sku_def, reserved=(self.plan.get('is_linux', None)))

            poller = self.web_client.app_service_plans.create_or_update(
                self.plan['resource_group'], self.plan['name'], plan_def)

            if isinstance(poller, LROPoller):
                response = self.get_poller_result(poller)

            self.log("Response : {0}".format(response))

            return appserviceplan_to_dict(response)
        except CloudError as ex:
            self.fail("Failed to create app service plan {0} in resource group {1}: {2}".format(
                self.plan['name'], self.plan['resource_group'], str(ex)))

    def list_app_settings(self):
        '''
        List application settings
        :return: deserialized list response
        '''
        self.log("List application setting")

        try:

            response = self.web_client.web_apps.list_application_settings(
                resource_group_name=self.resource_group, name=self.name)
            self.log("Response : {0}".format(response))

            return response.properties
        except CloudError as ex:
            self.fail("Failed to list application settings for web app {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))

    def update_app_settings(self):
        '''
        Update application settings
        :return: deserialized updating response
        '''
        self.log("Update application setting")

        try:
            response = self.web_client.web_apps.update_application_settings(
                resource_group_name=self.resource_group, name=self.name, properties=self.app_settings_strDic)
            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            self.fail("Failed to update application settings for web app {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))

    def create_or_update_source_control(self):
        '''
        Update site source control
        :return: deserialized updating response
        '''
        self.log("Update site source control")

        if self.deployment_source is None:
            return False

        self.deployment_source['is_manual_integration'] = False
        self.deployment_source['is_mercurial'] = False

        try:
            response = self.web_client.web_client.create_or_update_source_control(
                self.resource_group, self.name, self.deployment_source)
            self.log("Response : {0}".format(response))

            return response.as_dict()
        except CloudError as ex:
            self.fail("Failed to update site source control for web app {0} in resource group {1}".format(
                self.name, self.resource_group))

    def get_webapp_configuration(self):
        '''
        Get  web app configuration
        :return: deserialized  web app configuration response
        '''
        self.log("Get web app configuration")

        try:

            response = self.web_client.web_apps.get_configuration(
                resource_group_name=self.resource_group, name=self.name)
            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            self.log("Failed to get configuration for web app {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))

            return False

    def set_webapp_state(self, appstate):
        '''
        Start/stop/restart web app
        :return: deserialized updating response
        '''
        try:
            if appstate == 'started':
                response = self.web_client.web_apps.start(resource_group_name=self.resource_group, name=self.name)
            elif appstate == 'stopped':
                response = self.web_client.web_apps.stop(resource_group_name=self.resource_group, name=self.name)
            elif appstate == 'restarted':
                response = self.web_client.web_apps.restart(resource_group_name=self.resource_group, name=self.name)
            else:
                self.fail("Invalid web app state {0}".format(appstate))

            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            request_id = ex.request_id if ex.request_id else ''
            self.log("Failed to {0} web app {1} in resource group {2}, request_id {3} - {4}".format(
                appstate, self.name, self.resource_group, request_id, str(ex)))


def main():
    """Main execution"""
    AzureRMWebApps()


if __name__ == '__main__':
    main()

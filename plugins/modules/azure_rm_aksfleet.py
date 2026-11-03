#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_aksfleet
version_added: "4.3.0"
short_description: Manage a Fleet Manager and its cluster memberships
description:
    - Create, update and delete a Fleet Manager resource and manage the
      clusters that belong to it.
    - A fleet orchestrates updates of multiple Kubernetes clusters; use the
      clusters in I(members) as rollout stages or update strategies through
      Fleet update runs.
    - A fleet without I(hub) does not deploy a hub cluster and only provides
      multi-cluster update orchestration.
options:
    resource_group:
        description:
            - Name of the resource group for the fleet.
        required: true
        type: str
    name:
        description:
            - Name of the fleet. Must be unique in the resource group.
        required: true
        type: str
    location:
        description:
            - Azure Region for the fleet. Defaults to the location of the
              resource group.
            - Immutable once the fleet is created.
        type: str
    hub:
        description:
            - Configuration of the managed hub cluster of the fleet.
            - A fleet without I(hub) has no hub cluster; the hub cluster is
              created when I(hub) is first set.
            - Additional hub options such as the auto-scaling profile are
              planned for later releases.
        type: dict
        suboptions:
            dns_prefix:
                description:
                    - DNS prefix of the hub API server.
                required: true
                type: str
    members:
        description:
            - Azure resource IDs of the clusters that belong to the fleet.
              Azure Kubernetes Service managed clusters are supported.
            - When set, the module reconciles the fleet's memberships to
              exactly this list; members not listed are removed from the
              fleet (the clusters themselves are untouched).
            - The member name of each cluster is derived from the last
              segment of its resource ID, so a cluster can change from I(hub)
              to I(member) and vice versa between playbooks and stay
              reconciled.
            - Leave unset to keep the existing memberships.
        type: list
        elements: str
    state:
        description:
            - Assert the state of the fleet. Use C(present) to create or
              update, C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent
notes:
    - On update, fields that are omitted are carried forward from the
      existing fleet.
    - Deleting a fleet also removes its memberships and local update runs.
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a fleet and register two clusters
  azure.azcollection.azure_rm_aksfleet:
    resource_group: myResourceGroup
    name: myFleet
    location: eastus
    tags:
      env: prod
    members:
      - /subscriptions/xxx/resourceGroups/rg1/providers/Microsoft.ContainerService/managedClusters/aks1
      - /subscriptions/xxx/resourceGroups/rg2/providers/Microsoft.ContainerService/managedClusters/aks2

- name: Update the membership of the fleet
  azure.azcollection.azure_rm_aksfleet:
    resource_group: myResourceGroup
    name: myFleet
    members:
      - /subscriptions/xxx/resourceGroups/rg1/providers/Microsoft.ContainerService/managedClusters/aks1

- name: Add a fleet to a resource group without a hub cluster
  azure.azcollection.azure_rm_aksfleet:
    resource_group: myResourceGroup
    name: updateFleet

- name: Delete a fleet
  azure.azcollection.azure_rm_aksfleet:
    resource_group: myResourceGroup
    name: myFleet
    state: absent
'''

RETURN = '''
fleet:
    description:
        - The fleet definition, including its member clusters in I(members).
    returned: when I(state=present)
    type: dict
    sample: {
        "name": "myFleet",
        "location": "eastus",
        "tags": {"env": "prod"},
        "provisioning_state": "Succeeded",
        "members": [
            {
                "name": "aks1",
                "cluster_resource_id":
                  "/subscriptions/xxx/resourceGroups/rg1/providers/Microsoft.ContainerService/managedClusters/aks1",
                "provisioning_state": "Succeeded"
            }
        ]
    }
'''

import re

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.containerservicefleet import models as fleet_models
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

# Fields which are read-only or create-only and must not be replayed on update.
HUB_RO_FIELDS = ('fqdn', 'portal_fqdn', 'kubernetes_version', 'agent_profile', 'api_server_access_profile')
# Identity fields Azure fills on its own on read.
IDENTITY_RO_FIELDS = ('principal_id', 'tenant_id')
READ_ONLY_FIELDS = ('id', 'name', 'type', 'system_data', 'provisioning_state', 'status')
FLEET_MEMBER_NAME_PATTERN = re.compile(r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?$')
FLEET_MEMBER_NAME_MAX_LENGTH = 50


class AzureRMAksFleet(AzureRMModuleBaseExt):
    """Manage a Fleet Manager and its cluster memberships."""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            tags=dict(type='dict'),
            hub=dict(
                type='dict',
                options=dict(
                    dns_prefix=dict(type='str', required=True),
                ),
            ),
            members=dict(type='list', elements='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.tags = None
        self.hub = None
        self.members = None
        self.state = None

        self.results = dict(changed=False)
        self.fleet_client = None

        super(AzureRMAksFleet, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.fleet_client = self.containerservicefleet_client

        existing = self.get_resource()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_resource()
            return self.results

        if existing is not None:
            tags_changed, self.tags = self.update_tags(existing.get('tags'))
            if tags_changed:
                self.results['changed'] = True

        if existing is None:
            if self.location is None:
                self.location = self.get_resource_group(self.resource_group).location
            self.results['changed'] = True
            if not self.check_mode:
                body = self._merge(self._body(), existing)
                self.results['fleet'] = self.create_update_resource(body)
            else:
                self.results['fleet'] = self._for_check_mode(existing)
        else:
            if self.location is not None and self.location != existing['location']:
                self.fail("The location of fleet '{0}' is immutable: '{1}' cannot be applied on "
                          "'{2}'".format(self.name, self.location, existing['location']))
            body = self._merge(self._body(), existing)
            if not self._is_current(body, existing):
                self.results['changed'] = True
                if not self.check_mode:
                    self.results['fleet'] = self.create_update_resource(body)
                else:
                    self.results['fleet'] = self._for_check_mode(existing)
            else:
                self.results['fleet'] = existing

        # Reconcile the fleet's memberships when members is supplied.
        if self.members is not None:
            if self.check_mode:
                changed = self._members_need_update()
            else:
                changed = self._reconcile_members()
            if changed:
                self.results['changed'] = True

        if not self.check_mode and self.state == 'present':
            self.results['fleet']['members'] = self._member_list()

        return self.results

    def get_resource(self):
        """Read the fleet with its writable properties flattened."""
        try:
            response = self.fleet_client.fleets.get(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
            )
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving fleet {0}: {1}".format(self.name, str(exc)))
        normalized = as_attribute_dict(response, exclude_readonly=False)
        if normalized.get('properties'):
            normalized.update(normalized.pop('properties'))
        normalized['resource_group'] = self.resource_group
        return normalized

    def create_update_resource(self, body):
        self.log("Creating / updating fleet {0}".format(self.name))
        fleet = fleet_models.Fleet(location=body['location'], tags=body.get('tags'))
        if body.get('identity'):
            fleet.identity = self._identity_model(body['identity'])
        if body.get('hub_profile'):
            fleet.properties = fleet_models.FleetProperties(
                hub_profile=fleet_models.FleetHubProfile(**body['hub_profile']))
        try:
            response = self.fleet_client.fleets.begin_create_or_update(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
                resource=fleet,
            ).result()
        except Exception as exc:
            self.fail("Error creating / updating fleet {0}: {1}".format(self.name, str(exc)))
        return self._flatten(response)

    def delete_resource(self):
        self.log("Deleting fleet {0}".format(self.name))
        try:
            self.fleet_client.fleets.begin_delete(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
            ).result()
        except Exception as exc:
            self.fail("Error deleting fleet {0}: {1}".format(self.name, str(exc)))
        return True

    def _body(self):
        """Wire body holding the user-supplied (non C(None)) options.

        Valid both for creation and for the overlay of an update.
        """
        body = dict()
        if self.location is not None:
            body['location'] = self.location
        if self.tags is not None:
            body['tags'] = self.tags
        if self.hub is not None:
            body['hub_profile'] = {k: v for k, v in self.hub.items() if v is not None}
        return body

    def _merge(self, body, existing):
        """Carry forward writable fields the user omitted on update; return
        the payload for the full-replace PUT."""
        if existing is None:
            return body
        merged = dict(body)
        if self.location is None and merged.get('location') is None:
            merged['location'] = existing['location']
        if self.tags is None and existing.get('tags'):
            merged['tags'] = existing['tags']
        if self.hub is None and existing.get('hub_profile'):
            merged['hub_profile'] = {k: v for k, v in existing['hub_profile'].items()
                                     if k not in HUB_RO_FIELDS}
        if existing.get('identity'):
            merged['identity'] = {k: v for k, v in (existing['identity'] or {}).items()
                                  if k not in IDENTITY_RO_FIELDS}
        return merged

    def _is_current(self, body, existing):
        if self.tags is not None and (body.get('tags') or {}) != (existing.get('tags') or {}):
            return False
        if self.hub is not None:
            wanted = body.get('hub_profile') or dict()
            current = existing.get('hub_profile') or dict()
            for key, value in wanted.items():
                if value != current.get(key):
                    return False
        return True

    def _reconcile_members(self):
        """Align the fleet's memberships with self.members. Returns changed."""
        clusters = self._member_names(self.members)

        current = self._member_list()
        desired_ids = {resource_id.lower() for resource_id in self.members}
        current_ids = {member['cluster_resource_id'].lower() for member in current}

        changed = False
        # Remove stale memberships first. This also frees a child name if a
        # different cluster with the same name is being substituted.
        for member in current:
            if member['cluster_resource_id'].lower() not in desired_ids:
                self._delete_member(member['name'])
                changed = True

        for cluster_resource_id, member_name in zip(self.members, clusters):
            if cluster_resource_id.lower() in current_ids:
                continue
            self._add_member(member_name, cluster_resource_id)
            changed = True
        return changed

    def _members_need_update(self):
        """Diff for check mode. Returns True when a change is needed."""
        current_ids = {member['cluster_resource_id'].lower() for member in self._member_list()}
        self._member_names(self.members)
        desired_ids = {resource_id.lower() for resource_id in self.members}
        return current_ids != desired_ids

    def _member_name(self, cluster_resource_id):
        """Validate a supported cluster ARM resource ID and derive its name."""
        parts = cluster_resource_id.strip('/').split('/')
        if (len(parts) == 8 and
                parts[0].lower() == 'subscriptions' and parts[1] and
                parts[2].lower() == 'resourcegroups' and parts[3] and
                parts[4].lower() == 'providers' and
                parts[5].lower() == 'microsoft.containerservice' and
                parts[6].lower() == 'managedclusters' and parts[7]):
            name = parts[7].lower()
            if (len(name) <= FLEET_MEMBER_NAME_MAX_LENGTH and
                    FLEET_MEMBER_NAME_PATTERN.match(name)):
                return name
            self.fail("cluster name '{0}' is not a valid Fleet member name; names must match "
                      "{1} and be at most {2} characters".format(
                          parts[7], FLEET_MEMBER_NAME_PATTERN.pattern,
                          FLEET_MEMBER_NAME_MAX_LENGTH))
        self.fail("members must hold Azure resource IDs of AKS managed clusters, got '{0}'".format(cluster_resource_id))
        return None

    def _member_names(self, cluster_resource_ids):
        """Return Fleet member names, rejecting IDs that collide on name."""
        names = [self._member_name(resource_id) for resource_id in cluster_resource_ids]
        if len(set(names)) != len(names):
            self.fail("members contains clusters with the same name; Fleet member names must be unique")
        return names

    def _add_member(self, member_name, cluster_resource_id):
        self.log("Adding member {0} to fleet {1}".format(member_name, self.name))
        try:
            self.fleet_client.fleet_members.begin_create(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
                fleet_member_name=member_name,
                resource=fleet_models.FleetMember(
                    properties=fleet_models.FleetMemberProperties(cluster_resource_id=cluster_resource_id)),
            ).result()
        except Exception as exc:
            self.fail("Error adding member {0} to fleet {1}: {2}".format(member_name, self.name, str(exc)))
        return True

    def _delete_member(self, member_name):
        self.log("Removing member {0} from fleet {1}".format(member_name, self.name))
        try:
            self.fleet_client.fleet_members.begin_delete(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
                fleet_member_name=member_name,
            ).result()
        except Exception as exc:
            self.fail("Error removing member {0} from fleet {1}: {2}".format(member_name, self.name, str(exc)))
        return True

    def _member_list(self):
        try:
            members = list(self.fleet_client.fleet_members.list_by_fleet(
                resource_group_name=self.resource_group,
                fleet_name=self.name,
            ))
        except ResourceNotFoundError:
            # The fleet does not exist (yet), e.g. in check mode on create.
            return []
        except Exception as exc:
            self.fail("Error listing members of fleet {0}: {1}".format(self.name, str(exc)))
        result = []
        for member in members:
            normalized = as_attribute_dict(member, exclude_readonly=False)
            properties = normalized.pop('properties', None) or {}
            normalized.update(properties)
            normalized.pop('system_data', None)
            result.append(normalized)
        return result

    def _identity_model(self, identity):
        user_identities = identity.get('user_assigned_identities')
        properties = dict(type=identity.get('type'))
        if user_identities:
            properties['user_assigned_identities'] = {
                rid: fleet_models.UserAssignedIdentity() for rid in user_identities}
        return fleet_models.ManagedServiceIdentity(**properties)

    def _for_check_mode(self, existing):
        """Report the state the module would produce without API calls."""
        item = existing or dict()
        result = dict(item)
        result['name'] = self.name
        result['location'] = self.location or \
            (existing.get('location') if existing else self.get_resource_group(self.resource_group).location)
        if self.tags is not None:
            result['tags'] = dict(self.tags)
        if self.hub is not None:
            result['hub_profile'] = dict(
                (existing.get('hub_profile') or {}), **{k: v for k, v in self.hub.items() if v is not None})
            result['hub_profile'].pop('fqdn', None)
            result['hub_profile'].pop('portal_fqdn', None)
        result['members'] = sorted(self._member_names_for_check(existing))
        result['resource_group'] = self.resource_group
        return result

    def _member_names_for_check(self, existing):
        if self.members is None:
            return [member['name'] for member in self._member_list()]
        return self._member_names(self.members)

    def _flatten(self, fleet):
        if fleet is None:
            return None
        normalized = as_attribute_dict(fleet, exclude_readonly=False)
        if normalized.get('properties'):
            normalized.update(normalized.pop('properties'))
        normalized['resource_group'] = self.resource_group
        return normalized


def main():
    AzureRMAksFleet()


if __name__ == '__main__':
    main()

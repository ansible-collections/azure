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
    plugin:
        description: marks this as an instance of the 'azure_rm' plugin
        required: true
        choices: ['azure_rm', 'azure.azcollection.azure_rm']
    include_vm_resource_groups:
        description: A list of resource group names to search for virtual machines. '\*' will include all resource
            groups in the subscription. Can also be set comma separated resource group names via the
            C(ANSIBLE_AZURE_VM_RESOURCE_GROUPS) environment variable.
        default: ['*']
    include_vmss_resource_groups:
        description: A list of resource group names to search for virtual machine scale sets (VMSSs). '\*' will
            include all resource groups in the subscription.
        default: []
    fail_on_template_errors:
        description: When false, template failures during group and filter processing are silently ignored (eg,
            if a filter or group expression refers to an undefined host variable)
        choices: [True, False]
        default: True
    keyed_groups:
        description: Creates groups based on the value of a host variable. Requires a list of dictionaries,
            defining C(key) (the source dictionary-typed variable), C(prefix) (the prefix to use for the new group
            name), and optionally C(separator) (which defaults to C(_))
    conditional_groups:
        description: A mapping of group names to Jinja2 expressions. When the mapped expression is true, the host
            is added to the named group.
    hostvar_expressions:
        description: A mapping of hostvar names to Jinja2 expressions. The value for each host is the result of the
            Jinja2 expression (which may refer to any of the host's existing variables at the time this inventory
            plugin runs).
    exclude_host_filters:
        description: Excludes hosts from the inventory with a list of Jinja2 conditional expressions. Each
            expression in the list is evaluated for each host; when the expression is true, the host is excluded
            from the inventory.
        default: []
    batch_fetch:
        description: To improve performance, results are fetched using an unsupported batch API. Disabling
            C(batch_fetch) uses a much slower serial fetch, resulting in many more round-trips. Generally only
            useful for troubleshooting.
        default: true
    default_host_filters:
        description: A default set of filters that is applied in addition to the conditions in
            C(exclude_host_filters) to exclude powered-off and not-fully-provisioned hosts. Set this to a different
            value or empty list if you need to include hosts in these states.
        default: ['powerstate != "running"', 'provisioning_state != "succeeded"']
    use_contrib_script_compatible_sanitization:
        description:
        - By default this plugin is using a general group name sanitization to create safe and usable group names for use in Ansible.
            This option allows you to override that, in efforts to allow migration from the old inventory script and
            matches the sanitization of groups when the script's ``replace_dash_in_groups`` option is set to ``False``.
            To replicate behavior of ``replace_dash_in_groups = True`` with constructed groups,
            you will need to replace hyphens with underscores via the regex_replace filter for those entries.
        - For this to work you should also turn off the TRANSFORM_INVALID_GROUP_CHARS setting,
            otherwise the core engine will just use the standard sanitization on top.
        - This is not the default as such names break certain functionality as not all characters are valid Python identifiers
            which group names end up being used as.
        type: bool
        default: False
        version_added: '0.0.1'
    plain_host_names:
        description:
        - By default this plugin will use globally unique host names.
            This option allows you to override that, and use the name that matches the old inventory script naming.
        - This is not the default, as these names are not truly unique, and can conflict with other hosts.
            The default behavior will add extra hashing to the end of the hostname to prevent such conflicts.
        type: bool
        default: False
        version_added: '0.0.1'
    hostnames:
        description:
        - A list of Jinja2 expressions in order of precedence to compose inventory_hostname.
        - Ignores expression if result is an empty string or None value.
        - By default, inventory_hostname is generated to be globally unique based on the VM host name.
            See C(plain_host_names) for more details on the default.
        - An expression of 'default' will force using the default hostname generator if no previous hostname expression
            resulted in a valid hostname.
        - Use ``default_inventory_hostname`` to access the default hostname generator's value in any of the Jinja2 expressions.
        type: list
        elements: str
        default: [default]
'''

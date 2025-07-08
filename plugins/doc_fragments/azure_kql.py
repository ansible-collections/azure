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
        choices: ['azure_kql', 'azure.azcollection.azure_kql']
    graph_query:
        description: A graph query which will retrieve the inventory of hosts you are interested in.
            You must return inventory_hostname as a field from your query.
    fail_on_template_errors:
        description: When false, template failures during group and filter processing are silently ignored (eg,
            if a filter or group expression refers to an undefined host variable)
        choices: [True, False]
        default: True
    keyed_groups:
        description: Creates groups based on the value of a host variable. Requires a list of dictionaries,
            defining C(key) (the source dictionary-typed variable), C(prefix) (the prefix to use for the new group
            name), and optionally C(separator) (which defaults to C(_))
    groups:
        description: A mapping of group names to Jinja2 expressions. When the mapped expression is true, the host
            is added to the named group.
    compose:
        description: A mapping of hostvar names to Jinja2 expressions. The value for each host is the result of the
            Jinja2 expression (which may refer to any of the host's existing variables at the time this inventory
            plugin runs).
    hostnames:
        description:
        - A list of Jinja2 expressions in order of precedence to compose inventory_hostname.
        - Ignores expression if result is an empty string or None value.
        - An expression of C(default) will force using the default hostname generator if no previous hostname expression
            resulted in a valid hostname.
        - Use C(default_inventory_hostname) to access the default hostname generator's value in any of the Jinja2 expressions.
        type: list
        elements: str
        default: [default]
'''

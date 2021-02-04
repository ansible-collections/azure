# -*- coding: utf-8 -*-

# Copyright: (c) 2016, Matt Davis, <mdavis@ansible.com>
# Copyright: (c) 2016, Chris Houseknecht, <house@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    # Azure doc fragment
    DOCUMENTATION = r'''
options:
    tags:
        description:
            - Dictionary of string:string pairs to assign as metadata to the object.
            - Metadata tags on the object will be updated with any provided values.
            - To remove tags set append_tags option to false.
            - Currently, Azure DNS zones and Traffic Manager services also don't allow the use of spaces in the tag.
            - Azure Front Door doesn't support the use of # in the tag name.
            - Azure Automation and Azure CDN only support 15 tags on resources.
        type: dict
    append_tags:
        description:
            - Use to control if tags field is canonical or just appends to existing tags.
            - When canonical, any tags not found in the tags parameter will be removed from the object's metadata.
        type: bool
        default: yes
    '''

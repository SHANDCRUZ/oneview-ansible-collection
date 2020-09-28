#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
# ----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_storage_system_facts
short_description: Retrieve facts about the OneView Storage Systems
description:
    - Retrieve facts about the Storage Systems from OneView.
version_added: "2.5.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.0.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    storage_hostname:
      description:
        - Storage System IP or hostname.
    name:
      description:
        - Storage System name.
    options:
      description:
        - "List with options to gather additional facts about a Storage System and related resources.
          Options allowed:
          C(hostTypes) gets the list of supported host types.
          C(storagePools) gets a list of storage pools belonging to the specified storage system.
          C(reachablePorts) gets a list of storage system reachable ports. Accepts C(params).
            An additional C(networks) list param can be used to restrict the search for only these ones.
          C(templates) gets a list of storage templates belonging to the storage system."
        - "To gather facts about C(storagePools), C(reachablePorts), and C(templates) it is required to inform
            either the argument C(name), C(ip_hostname), or C(hostname). Otherwise, this option will be ignored."
    api_version:
        description:
            - List with the api_version.
        required: false
        type: int
    hostname:
        description:
            - List with the hostname.
        required: false
        type: str
    image_streamer_hostname:
        description:
            - List with the image_streamer_hostname.
        required: false
        type: str
    password:
        description:
            - List with the password.
        required: false
        type: str
    auth_login_domain:
        description:
            - List with the auth_login_domain.
        required: false
        type: str
    username:
        description:
            - List with the username.
        required: false
        type: str

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Systems
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather paginated, filtered and sorted facts about Storage Systems
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: managedDomain=TestDomain

- debug: var=storage_systems

- name: Gather facts about a Storage System by IP (ip_hostname)
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather facts about a Storage System by IP (hostname)
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather facts about a Storage System by name
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather facts about a Storage System and all options
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "ThreePAR7200-4555"
    options:
        - hostTypes
        - storagePools
  delegate_to: localhost

- debug: var=storage_systems
- debug: var=storage_system_host_types
- debug: var=storage_system_pools

- name: Gather queried facts about Storage System reachable ports (API500 onwards)
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    options:
        - reachablePorts
    params:
      networks:
        - /rest/fc-networks/01FC123456
        - /rest/fc-networks/02FC123456
      sort: 'name:descending'

- debug: var=storage_system_reachable_ports

- name: Gather facts about Storage System storage templates (API500 onwards)
  oneview_storage_system_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    options:
      - templates
    params:
      sort: 'name:descending'

- debug: var=storage_system_templates
'''

RETURN = '''
storage_systems:
    description: Has all the OneView facts about the Storage Systems.
    returned: Always, but can be null.
    type: dict

storage_system_host_types:
    description: Has all the OneView facts about the supported host types.
    returned: When requested, but can be null.
    type: dict

storage_system_pools:
    description: Has all the OneView facts about the Storage Systems - Storage Pools.
    returned: When requested, but can be null.
    type: dict

storage_system_reachable_ports:
    description: Has all the OneView facts about the Storage Systems reachable ports.
    returned: When requested, but can be null.
    type: dict

storage_system_templates:
    description: Has all the OneView facts about the Storage Systems - Storage Templates.
    returned: When requested, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class StorageSystemFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(type='str'),
            options=dict(type='list'),
            params=dict(type='dict'),
            storage_hostname=dict(type='str')
        )

        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.storage_systems)

    def execute_module(self):
        facts = {}
        is_specific_storage_system = True

        # This allows using both "ip_hostname" and "hostname" regardless api_version
        if self.oneview_client.api_version >= 500:
            get_method = self.resource_client.get_by_hostname
        else:
            get_method = self.resource_client.get_by_ip_hostname

        if self.module.params.get('storage_hostname'):
            self.current_resource = get_method(self.module.params['storage_hostname'])

        if self.current_resource:
            storage_systems = [self.current_resource.data]
        else:
            storage_systems = self.resource_client.get_all(**self.facts_params)
            is_specific_storage_system = False

        self.__get_options(facts, is_specific_storage_system)

        facts['storage_systems'] = storage_systems

        return dict(changed=False, ansible_facts=facts)

    def __get_options(self, facts, is_specific_storage_system):

        if self.options:
            if self.options.get('hostTypes'):
                facts['storage_system_host_types'] = self.oneview_client.storage_systems.get_host_types()

            if self.current_resource and is_specific_storage_system:
                query_params = self.module.params.get('params', {})
                if self.options.get('storagePools'):
                    facts['storage_system_pools'] = self.current_resource.get_storage_pools()
                if self.options.get('reachablePorts'):
                    facts['storage_system_reachable_ports'] = \
                        self.current_resource.get_reachable_ports(**query_params)
                if self.options.get('templates'):
                    facts['storage_system_templates'] = \
                        self.current_resource.get_templates(**query_params)


def main():
    StorageSystemFactsModule().run()


if __name__ == '__main__':
    main()

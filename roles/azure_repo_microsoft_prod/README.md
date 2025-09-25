azure_repo_microsoft_prod
==================

A role to Configure a repo for Microsoft production software.

Requirements
------------

* A supported **ansible_os_family**.  Currently only RedHat is supported but you can provide the package url yourself. See the role variables below.

Role Variables
--------------

* **azure_repo_microsoft_prod_package_url**: You can set this url to the full path to the Microsoft production repo.  By default this will be set automatically for RedHat.
* **proxy**: Object used to provide details for proxy setup if needed.  Contains the following:
  - * **hostname**: The hostname of the proxy server.
  - * **port**: The port that the proxy server is listening on.

Limitations
------------

- NA

Dependencies
------------

- NA

Example Playbook
----------------

    - name: Configure Microsoft production repository
      hosts: all
      tasks:
        - name: Configure Microsoft production repository
          ansible.builtin.include_role:
            name: azure.azure_repo_microsoft_prod
          vars:
            proxy:
              hostname: proxy.example.com
              port: 8080

License
-------

GNU General Public License v3.0 or later

See [LICENCE](https://github.com/ansible-collections/azure/blob/dev/LICENSE) to see the full text.

Author Information
------------------

- Klaas Demter
- Ansible Cloud Content Team

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': '@joelwking'
}
DOCUMENTATION = '''
---
module: cucm.admin

short_description: Administration of Cisco Unified Communications Manager using AXL
version_added: "2.13.7"

description:
    - "Ansible module to administration of the Call Manager via the AXL library"

options:
    arguments:
      description:
        - The arguments passed to the method
      required: false
      type: dict

    hostname:
      description:
        - The hostname or IP address of the CUCM
      required: true
      type: str

    username: 
      description:
        - The username used to logon the CUCM
      default: administrator
      required: false
      type: str

    password:
      description:
        - The password associated with the username
      required: true
      type: str

  
author:
    - Joel W. King (@joelwking)
'''
EXAMPLES = '''

---
- name: Manage Users
  hosts: localhost

  vars:
    cucm_anchor: &cucm_opts
      hostname: '10.10.20.1'
      username: administrator
      password: 'ciscopsdt'
      version: '12.5'

  tasks:
    - name: Add User
      netcraftsmen.cucm.admin:
        <<: *cucm_opts
        method: add_user
        arguments:
          userid: 'jking@netcraftsmen.com' 
          lastName: 'King' 
          firstName: 'Joel'

'''
from ansible.module_utils.basic import AnsibleModule

try:
    from PhantomIngest import ingest
    HAS_INGEST = True
except ImportError:
    HAS_INGEST = False

def container():
    """
    """
    return

def artifact(_object, container_id, cef, meta_data, art_i_fact):
    """
    """
    artifact_id = _object.add_artifact(container_id, cef, meta_data, **art_i_fact)
    return (dict(artifact_id=artifact_id, status_code=p.status_code)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            authtoken=dict(required=True, no_log=True),
            container_id=dict(required=True),
            container=dict(required=False, type=dict, default=dict())
            artifact=dict(required=False, type=dict, default=dict()),
            cef=dict(required=False, type='dict', default=dict()),
            metadata=dict(required=False, type='dict', default=dict()),
        ),
        supports_check_mode=False
    )

    if not HAS_INGEST:
        module.fail_json(msg="The python SDK, PhantomIngest, is required")

    server = module.params.get('server')
    authtoken = module.params.get('authtoken')
    container_id = module.params.get('container_id')
    container = module.params.get('container')

    try:
        p = ingest.PhantomIngest(f"https://{server}", f"{authtoken}")
    except Exception as e:
        module.fail_json(msg=f'Exception: {e}')

    container_id = module.params.get('container_id')  # TODO for now, required
    if container:
        container_id = container(container)  # TODO Create container if not specified.
    
    cef = module.params.get('cef')
    metadata = module.params.get('metadata')
    artifact = module.params.get('artifact')

    result = artifact()
    result['changed'] = False
    if result.get('status_code') in (200,):  # TODO is string or integer?
        result['changed'] = True

    module.exit_json(**result)

if __name__ == "__main__":
    main()

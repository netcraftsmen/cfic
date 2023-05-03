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

short_description: Create Splunk SOAR events
version_added: "2.14.5"

description:
    - "Ansible module to create Splunk SOAR events (containers and artifacts)"

options:
    authtoken:
      description:
        - The API Bearer Token, "ph-auth-token" for the 'automation' user
      required: true
      type: str

    server:
      description:
        - The host IP or FQDN of the Splunk SOAR instance
      required: true
      type: str

    TODO

author:
    - Joel W. King (@joelwking)
'''
EXAMPLES = '''

    - name: Add artifact to new container
      netcraftsmen.kafka.soar_event:
        server: ec2-54-164-159-148.compute-1.amazonaws.com
        authtoken: "1GvdkA220zFlbJMjISredactedm9QANjCg0k="
        # container_id: 3
        container:
          name: "Voltaire" 
          description: "French Enlightenment writer, historian, and philosopher."
        artifact:
          name: "cfic"
          source_data_identifier: "IR_3458575"
        cef:
          sourceAddress: 192.0.2.1
          sourcePort: 6553 
          sourceUserId: 'voltaire@example.net'
        metadata:
          Influenced_by: "John Locke, William Shakespeare, Isaac Newton"
          Born: "November 21, 1694"
          quote: "Judge of a man by his questions rather than by his answers."

    - name: Add artifact to new container
      netcraftsmen.kafka.soar_event:
        server: ec2-54-164-159-148.compute-1.amazonaws.com
        authtoken: "1GvdkA220zFlbJMjISredactedm9QANjCg0k="
        container_id: 3
        artifact:
          name: "cfic"
          source_data_identifier: "IR_3458575"
        cef:
          sourceMacAddress: “00:0D:60:AF:1B:61”
          msg: "An arbitrary message giving more details about the event."
          

'''
from ansible.module_utils.basic import AnsibleModule

try:
    from PhantomIngest import ingest
    HAS_INGEST = True
except ImportError:
    HAS_INGEST = False

def container():
    """
      TODO, for now, assume we have an existing container.
    """
    return

def artifact(_object, container_id, cef, metadata, artifact):
    """
      Add the artifact to the container (event)
    """
    try:
        artifact_id = _object.add_artifact(container_id, cef, metadata, **artifact)
    except:
        return dict(status_code=500)
    
    return dict(artifact_id=artifact_id, status_code=_object.status_code)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            authtoken=dict(required=True, no_log=True),
            container_id=dict(required=False),
            container=dict(required=False, type=dict, default=dict())
            artifact=dict(required=False, type=dict, default=dict(name='default')),
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

    if container and container_id:
       module.fail_json(msg="Specify either container ID or container, not both.")

    try:
        p = ingest.PhantomIngest(f"https://{server}", f"{authtoken}")
    except Exception as e:
        module.fail_json(msg=f'Exception: {e}')

    if container:
        container_id = container(container)  # TODO Create container if not specified.
    
    cef = module.params.get('cef')
    metadata = module.params.get('metadata')
    artifact = module.params.get('artifact')

    result = artifact(artifact(p, container_id, cef, metadata, artifact))
    result['changed'] = False
    if result.get('status_code') in (200,):  # TODO is string or integer?
        result['changed'] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()

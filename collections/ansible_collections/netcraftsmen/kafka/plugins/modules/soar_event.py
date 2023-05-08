#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': '@joelwking'
}
DOCUMENTATION = '''
---
module: kafka.soar_event.py

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

    container_id:
      description:
        - An existing container to add the artifact.
      required: false
      type: int
  
    container:
      description:
        - Key, Value pairs describing fields used to describe the container, see the
        - examples for suggested keys and sample values
      required: false
      type: dict
    
    artifact:
      description:
        - Key, Value pairs describing the files used to describe the artifact, see the
        - examples for suggested keys and sample values
      required: false
      type: dict

    cef:
      description:
        - The Common Event Format (CEF) is a standardized logging format developed by ArcSight
        - Search for 'ArcSight Common Event Format (CEF)' to locate the Key, Value schema.
      required: false
      type: dict

    metadata:
       description:
         - Additional meta data to add to the artifact, it is free form Key, Value pairs
       required: false
       type: dict

author:
    - Joel W. King (@joelwking)
'''
EXAMPLES = '''

    - name: Add artifact to new container
      netcraftsmen.kafka.soar_event:
        server: ec2-54-164-159-148.compute-1.amazonaws.com
        authtoken: "1GvdkA220zFlbJMjISredactedm9QANjCg0k="
        container:
          name: "A short friendly name for the container" 
          description: "A brief useful description of the behavior tracked by this container"
          label: events
          sensitivity: red
          severity: high
          tags: ['danger']
        artifact:
          name: "cfic"
          source_data_identifier: "IR_3458575"
          tags: ['atomic_counters']
          type: "network"
          label: "event"
        cef:
          sourceAddress: 192.0.2.1
          sourcePort: 6553 
          sourceUserId: 'voltaire@example.net'
        metadata:
          Influenced_by: "John Locke, William Shakespeare, Isaac Newton"
          Born: "November 21, 1694"
          quote: "Judge of a man by his questions rather than by his answers."

    - name: Add artifact to an existing container
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
    from ansible_collections.netcraftsmen.kafka.plugins.module_utils import PhantomIngest as ingest
    HAS_INGEST = True
except ImportError:
    HAS_INGEST = False

def create_container(_object, container):
    """
        Input is a dictionary that defines the name, description, etc.
        Returns a tuple of the container_id (int) and status_code (int) 
        or a text (str) indicating the error
    """
    try:
        container_id = _object.add_container(**container)
    except AssertionError as e:
        return f"Any HTTP return code other than OK {e} input: {container}"
    except Exception as e:
        return f"Typically the host did not respond, a connection error {e}"

    return dict(container_id=container_id, status_code=_object.status_code)

def add_artifact(_object, container_id, cef, metadata, _artifact):
    """
      Add the artifact to the container (event)
    """
    try:
        artifact_id = _object.add_artifact(container_id, cef, metadata, **_artifact)
    except:
        return dict(status_code=500, msg=f'input: {_artifact}')
    
    return dict(artifact_id=artifact_id, status_code=_object.status_code)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            authtoken=dict(required=True, no_log=True),
            container_id=dict(required=False, type='int'),
            container=dict(required=False, type='dict', default=dict()),
            artifact=dict(required=False, type='dict', default=dict(name='default')),
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

    result = dict(changed=False)   # Create a variable to store output

    if container and container_id:
       module.fail_json(msg="Specify either container ID or container, not both.")

    try:
        p = ingest.PhantomIngest(f"{server}", f"{authtoken}")
    except Exception as e:
        module.fail_json(msg=f'Exception: {e}')

    if container:
        container_result = create_container(p, container)
        if not isinstance(container_result, dict):
            module.fail_json(msg=f'{container_result}')
        container_id = container_result.get('container_id')
        result.update(container_result)
    else:
        result.update(dict(container_id=container_id))

    cef = module.params.get('cef')
    metadata = module.params.get('metadata')
    artifact = module.params.get('artifact')

    artifact_result = add_artifact(p, container_id, cef, metadata, artifact)
    
    if artifact_result.get('status_code') in (200,):
        result['changed'] = True
    else:
        module.fail_json(msg=f'{artifact_result}')

    result.update(artifact_result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()

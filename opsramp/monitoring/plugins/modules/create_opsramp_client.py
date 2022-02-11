#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import requests

DOCUMENTATION = \
    r'''
---
module: create_opsramp_client

short_description: This module automates creation of  opsramp client 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is longer description explaining create_opsramp_client.

options:
    api_endpoint:
        description: the api endpoint url.
        required: true
        type: str
    json_path:
        description: the absolute path of json file which is the input to create client.
        required: true
        type: str
    auth_header:
        description: bearer token to invoke API.
        required: true
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - opsramp.monitoring.my_doc_fragment_name

author:
    - BalaSubramanian Vetrivel
'''

EXAMPLES = \
    r'''
# Pass in a message
- name: Test with a message
  opsramp.monitoring.create_opsramp_client:
    api_endpoint: https://content-development.api.opsramp.net/api/v2/tenants/msp_795257/clients
    json_path: /home/subramanian/namasivaya/doc/opsramp/ansible/createClient.json
    auth_header bearer xxxxxx

# fail the module
- name: Test failure of the module
  opsramp.monitoring.create_opsramp_client:
    json_path: fail me
'''

RETURN = \
    r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original json_path param that was passed in.
    type: str
    returned: always
    sample: '/home/subramanian/namasivaya/doc/opsramp/ansible/createClient.json'
message:
    description: The output message that the create_opsramp_client module generates.
    type: str
    returned: always
    sample: 'client created successfully'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():

    # define available arguments/parameters a user can pass to the module

    module_args = dict(api_endpoint=dict(type='str', required=True),
                       json_path=dict(type='str', required=True),
                       auth_header=dict(type='str', required=True))

    result = dict(changed=False, original_message='', message='')

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=True)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications

    if module.check_mode:
        module.exit_json(**result)

    # #############
    # create client
    # #############

    url = module.params['api_endpoint']
    json_path = module.params['json_path']
    auth_header = module.params['auth_header']

    # auth_header='bearer 9f891b59-dcaa-49ca-aa3a-f3aa333d9838'

    data_json = open(json_path, 'rb').read()
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               'Authorization': '{}'.format(auth_header)}

    print('headers ', headers)

    # url = "https://content-development.api.opsramp.net/api/v2/tenants/msp_795257/clients"

    try:
        response = requests.post(url, data=data_json, headers=headers)
    except Exception, e:

        print('error at post call {}', e)
        raise SystemExit(e)

    result['original_message'] = (module.params['api_endpoint'],
                                  module.params['json_path'],
                                  module.params['auth_header'])

    if response.ok:
        result['message'] = \
            ('client created successfully output json is:',
             response.content)
        result['changed'] = True
    else:
        result['message'] = ('client was not created error is:',
                             response.content)
        result['changed'] = False

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result

    if module.params['json_path'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

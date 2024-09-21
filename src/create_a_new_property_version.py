import json
from credentials import *


def create_new_version(ASK, propertyId, propertyVersion, contractId, groupId, etag):
    payload = {
        "createFromVersion": propertyVersion,
        "createFromVersionEtag": etag
    }

    qs = {'accountSwitchKey': ASK,
          'contractId': contractId,
          'groupId': groupId,
          }

    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }

    response = session.post(urljoin(baseurl, f'/papi/v1/properties/{propertyId}/versions'),
                            headers=headers, json=payload, params=qs)
    print(response.json())
    return response


if __name__ == '__main__':
    # ASK  = generate_switch_key()
    # Akamai Tech
    # ASK = '1-599K:1-8BYUX'
    # TC East
    ASK = '1-5BYUG1:1-8BYUX'
    contractId = '1-5C13O2'
    groupId = '18543'
    propertyId = '1101399'
    propertyVersion = '1'
    etag = '5766855d8879dab1fa85ebf276c53169f38abf4a'
    response = create_new_version(ASK, propertyId, propertyVersion, contractId, groupId, etag)
    print(response.status_code)

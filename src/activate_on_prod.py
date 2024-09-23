import json
from credentials import *

def get_latest_version(ASK, propertyId, contractId, groupId):

    qs = {'accountSwitchKey': ASK,
          'contractId': contractId,
          'groupId': groupId,
          }

    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }

    response = session.get(urljoin(baseurl, f'/papi/v1/properties/{propertyId}/versions/latest'),
                            headers=headers, params=qs)
    # print(response.json())
    return response.json()

def activate_on_stage(ASK, propertyId, propertyVersion, contractId, groupId):
    payload = {
        "propertyVersion": propertyVersion,
        "network": "PRODUCTION",
        "note": "Sample activation",
        "useFastFallback": 'false',
        "notifyEmails": [
            "gamittal@akamai.com",
        ],
        "acknowledgeAllWarnings": True

        # "acknowledgeWarnings": [
        #     "7a2aa72bca3f894607c126436861cb73fb82d677"
        # ]
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

    response = session.post(urljoin(baseurl, f'/papi/v1/properties/{propertyId}/activations'),
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
    propertyVersion_response = get_latest_version(ASK, propertyId, contractId, groupId)
    propertyVersion = propertyVersion_response['versions']['items'][0]['propertyVersion']

    etag = '5766855d8879dab1fa85ebf276c53169f38abf4a'

    response = activate_on_stage(ASK,propertyId, propertyVersion, contractId, groupId)
    print(response.status_code)

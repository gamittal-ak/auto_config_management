import json
from credentials import *


def update_rule_tree(ASK, propertyId, propertyVersion, contractId, groupId):

    with open('auto_deploy/gamittal-compute.json', 'r') as file:
        payload = json.load(file)

    qs = {'accountSwitchKey': ASK,
          'contractId': contractId,
          'groupId': groupId,
          "validateMode": "full",
          "validateRules": "false",
          "dryRun": "false"

          }

    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }
    response = session.put(urljoin(baseurl,
                                    f"/papi/v1/properties/{propertyId}/versions/{propertyVersion}/rules"),
                           headers=headers, params=qs, json=payload)

    return response


if __name__ == '__main__':
    # ASK  = generate_switch_key()
    # Akamai Tech
    # ASK = '1-599K:1-8BYUX'
    # TC East
    ASK = '1-5BYUG1:1-8BYUX'
    contractId='1-5C13O2'
    groupId = '232339'
    propertyId = '988273'
    propertyVersion = '5'
    etag = 'b3d8183cd56cff2ac7558851ae909050315e80ef'
    response = update_rule_tree(ASK,propertyId, propertyVersion, contractId, groupId)
    print(response.status_code)


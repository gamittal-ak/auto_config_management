import json
from pprint import pprint
from credentials import *


def get_property(active_item, ASK):
    qs = {'accountSwitchKey': ASK,
          'contractId': active_item['contractId'],
          'groupId' : active_item['groupId']
            }

    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }


    response = session.get(urljoin(baseurl,
                                    f"/papi/v1/properties/{active_item['propertyId']}/versions/{active_item['propertyVersion']}/rules"), headers=headers, params=qs)

    return response.json()


def property_search(property_name, ASK):
    qs = {'accountSwitchKey': ASK }
    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }

    payload = {
        "propertyName": property_name
    }
    response = session.post(urljoin(baseurl, "/papi/v1/search/find-by-value"), headers=headers, params=qs, json=payload)
    return response


if __name__ == '__main__':
    # ASK  = generate_switch_key()
    # Akamai Tech
    # ASK = '1-599K:1-8BYUX'
    # TC East
    ASK = '1-5BYUG1:1-8BYUX'

    # property_name = input('Enter Property name to search: ')
    # property_name='cyberabstract_property'
    property_name='gamittal-compute'


    res = property_search(property_name, ASK)
    pprint(res.json())

    # Extract the item where productionStatus is 'ACTIVE'
    active_item = next(item for item in res.json()['versions']['items'] if item['productionStatus'] == 'ACTIVE')
    # print(active_item)
    rule_tree = get_property(active_item, ASK)
    pprint(rule_tree)
    with open(f'{rule_tree['propertyName']}.json', 'w') as outfile:
        json.dump(rule_tree, outfile, indent=4)
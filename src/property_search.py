import os
import json
import pickle
from pprint import pprint
from urllib.parse import urljoin
from credentials import get_or_generate_switch_key, session, baseurl

def get_property(active_item, ASK):
    qs = {'accountSwitchKey': ASK,
          'contractId': active_item['contractId'],
          'groupId': active_item['groupId']
          }

    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }

    response = session.get(
        urljoin(baseurl, f"/papi/v1/properties/{active_item['propertyId']}/versions/{active_item['propertyVersion']}/rules"),
        headers=headers, params=qs)

    if response.status_code != 200:
        print(f"Failed to fetch property rules. Status code: {response.status_code}")
        exit(1)

    return response.json()


def property_search(property_name, ASK):
    qs = {'accountSwitchKey': ASK}
    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }

    payload = {
        "propertyName": property_name
    }
    response = session.post(urljoin(baseurl, "/papi/v1/search/find-by-value"), headers=headers, params=qs, json=payload)

    if response.status_code != 200:
        print(f"Property search failed. Status code: {response.status_code}")
        exit(1)

    return response


if __name__ == '__main__':
    # Get or generate the account switch key (ASK) from the credentials
    switch_key_data = get_or_generate_switch_key()
    ASK = switch_key_data['switch_key']

    # Get the property name from the user
    property_name = input('Enter Property name to search: ')

    # Perform property search
    res = property_search(property_name, ASK)

    # Extract the item where productionStatus is 'ACTIVE'
    active_item = next(item for item in res.json()['versions']['items'] if item['productionStatus'] == 'ACTIVE')

    # Fetch the property rule tree for the active item
    rule_tree = get_property(active_item, ASK)

    # Save the rule tree to a JSON file
    with open(f"{rule_tree['propertyName']}.json", 'w') as outfile:
        json.dump(rule_tree, outfile, indent=4)

    # Create a dictionary with relevant fields from the rule tree
    relevant_data = {
        'accountId': rule_tree['accountId'],
        'contractId': rule_tree['contractId'],
        'groupId': rule_tree['groupId'],
        'propertyId': rule_tree['propertyId'],
        'propertyName': rule_tree['propertyName'],
        'propertyVersion': rule_tree['propertyVersion'],
        'etag': rule_tree['etag']
    }

    # Save the relevant fields to a pickle file
    with open("property_fields.pkl", 'wb') as pklfile:
        pickle.dump(relevant_data, pklfile)

    # Print confirmation and the relevant fields
    print(f"Relevant fields from the rule tree have been saved to {rule_tree['propertyName']}_fields.pkl")
    pprint(relevant_data)

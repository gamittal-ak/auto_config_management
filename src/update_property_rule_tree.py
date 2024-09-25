import json
import pickle
import os
from credentials import load_switch_key, session, baseurl
from urllib.parse import urljoin


def get_property_pkl_file():
    """Get the file path of the property pickle file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'property_fields.pkl')


def load_relevant_data_from_pkl():
    """Load the relevant data for the property from the pickle file."""
    pkl_file_path = get_property_pkl_file()

    if not os.path.exists(pkl_file_path):
        raise FileNotFoundError(f"Pickle file '{pkl_file_path}' not found for the property.")

    try:
        with open(pkl_file_path, 'rb') as pklfile:
            relevant_data = pickle.load(pklfile)
        return relevant_data
    except pickle.UnpicklingError as e:
        raise Exception(f"Error while unpickling the file: {e}")


def update_rule_tree(ASK, propertyId, propertyVersion, contractId, groupId, property_name):
    """Update the rule tree for a specific property version."""
    # Dynamically load the rule tree payload using propertyName from relevant data
    json_file_path = os.path.join('src', f'{property_name}.json')

    try:
        with open(json_file_path, 'r') as file:
            payload = json.load(file)
    except FileNotFoundError:
        print(f"JSON file for property '{property_name}' not found at {json_file_path}. Exiting.")
        exit(1)

    qs = {
        'accountSwitchKey': ASK,
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

    # Send the PUT request to update the rule tree
    response = session.put(urljoin(baseurl, f"/papi/v1/properties/{propertyId}/versions/{propertyVersion}/rules"),
                           headers=headers, params=qs, json=payload)

    return response


if __name__ == '__main__':
    try:
        # Step 1: Load the existing account switch key (ASK)
        switch_key_data = load_switch_key()
        if switch_key_data is None:
            raise Exception("No switch key found. Exiting.")
        ASK = switch_key_data['switch_key']

        # Step 2: Load relevant data from the pickle file for the property
        relevant_data = load_relevant_data_from_pkl()

        # Extract relevant fields from the pickle file
        contractId = relevant_data['contractId']
        groupId = relevant_data['groupId']
        propertyId = relevant_data['propertyId']
        propertyVersion = relevant_data['propertyVersion']
        property_name = relevant_data['propertyName']  # Dynamically load property name

        # Step 3: Update the rule tree for the specific property version using the loaded data
        response = update_rule_tree(ASK, propertyId, propertyVersion, contractId, groupId, property_name)

        # Step 4: Print the status of the API response
        print(f"Response status code: {response.status_code}")
        print(response.json())  # Optionally, print the full response for debugging

    except Exception as e:
        print(f"An error occurred: {e}")

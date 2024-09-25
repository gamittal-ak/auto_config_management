import json
import pickle
from credentials import load_switch_key, session, baseurl
from urllib.parse import urljoin

def load_relevant_data_from_pkl():
    """Load the relevant data for the property from the pkl file."""
    try:
        with open("property_fields.pkl", 'rb') as pklfile:
            relevant_data = pickle.load(pklfile)
        return relevant_data
    except FileNotFoundError:
        print(f"No pickle file found for property.")
        exit(1)

def activate_on_stage(ASK, propertyId, propertyVersion, contractId, groupId):
    """Activate the specified property version on the staging network."""
    payload = {
        "propertyVersion": propertyVersion,
        "network": "STAGING",
        "note": "Sample activation",
        "useFastFallback": False,
        "notifyEmails": [
            "gamittal@akamai.com",
        ],
        "acknowledgeAllWarnings": True
    }

    qs = {
        'accountSwitchKey': ASK,
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
    # Step 1: Load the existing account switch key (ASK)
    switch_key_data = load_switch_key()
    if switch_key_data is None:
        print("No switch key found. Exiting.")
        exit(1)
    ASK = switch_key_data['switch_key']

    # Step 2: Load relevant data (including new property version) from the pickle file
    relevant_data = load_relevant_data_from_pkl()

    # Extract relevant fields from the pickle file
    contractId = relevant_data['contractId']
    groupId = relevant_data['groupId']
    propertyId = relevant_data['propertyId']
    propertyVersion = relevant_data.get('new_property_version')  # Load new property version

    if not propertyVersion:
        print("No new property version found in the pickle file. Exiting.")
        exit(1)

    # Step 3: Activate the new property version on staging
    response = activate_on_stage(ASK, propertyId, propertyVersion, contractId, groupId)

    # Step 4: Print the status of the activation
    print(f"Response status code: {response.status_code}")

import json
import pickle
import sys
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

def activate_on_akamai(ASK, propertyId, propertyVersion, contractId, groupId, network):
    """Activate the specified property version on the given network (STAGING or PRODUCTION)."""
    payload = {
        "propertyVersion": propertyVersion,
        "network": network.upper(),  # Network can be STAGING or PRODUCTION
        "note": f"Activating version {propertyVersion} on {network}",
        "useFastFallback": False,
        "notifyEmails": [
            "gamittal@akamai.com",
        ],
        "acknowledgeAllWarnings": True,
    }

    # Add compliance record only for PRODUCTION
    if network.upper() == "PRODUCTION":
        payload["complianceRecord"] = {
            "unitTested": "false",
            "peerReviewedBy": "",
            "customerEmail": "",
            "nonComplianceReason": "NO_PRODUCTION_TRAFFIC",
            "otherNoncomplianceReason": "",
            "siebelCase": ""
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
    if len(sys.argv) < 2:
        print("Usage: python3 activate_on_akamai.py <network>")
        print("Example: python3 activate_on_akamai.py staging")
        print("Example: python3 activate_on_akamai.py production")
        exit(1)

    network = sys.argv[1].lower()  # Get the environment (staging or production) from command-line arguments

    if network not in ['staging', 'production']:
        print(f"Invalid network: {network}. Use 'staging' or 'production'.")
        exit(1)

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

    # Step 3: Activate the new property version on the specified network (STAGING or PRODUCTION)
    response = activate_on_akamai(ASK, propertyId, propertyVersion, contractId, groupId, network)

    # Step 4: Print the status of the activation
    print(f"Response status code: {response.status_code}")

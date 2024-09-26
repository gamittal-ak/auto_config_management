import pickle
import sys
import os
import time
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
        print(f"Loaded relevant data from pkl: {relevant_data}")  # Add this for debugging
        return relevant_data
    except pickle.UnpicklingError as e:
        raise Exception(f"Error while unpickling the file: {e}")


def check_activation_status(activation_link):
    """Check the status of the property activation on Akamai."""
    url = urljoin(baseurl, activation_link)
    response = session.get(url)

    if response.status_code == 200:
        status_data = response.json()
        return status_data['activation']['status']  # Polling the activation status
    else:
        print(f"Error while checking activation status: {response.status_code}. Response: {response.json()}")
        return None


def activate_on_akamai(ASK, propertyId, propertyVersion, contractId, groupId, network):
    """Activate the specified property version on the given network (STAGING or PRODUCTION)."""
    payload = {
        "propertyVersion": propertyVersion,
        "network": network.upper(),  # Network can be STAGING or PRODUCTION
        "note": f"DevOps Push Activating version {propertyVersion} on {network.upper()}",
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

    if response.status_code == 201:
        print(f"Successfully activated property on {network.upper()} network.")
        print(f"Activation response: {response.json()}")  # Add this for debugging
        return response
    else:
        print(f"Failed to activate property on {network.upper()} network. Status code: {response.status_code}")
        print(f"Response content: {response.json()}")  # Add this for debugging
        return None


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

    try:
        # Step 1: Load the existing account switch key (ASK)
        switch_key_data = load_switch_key()
        if switch_key_data is None:
            raise Exception("No switch key found. Exiting.")
        ASK = switch_key_data['switch_key']

        # Step 2: Load relevant data (including new property version) from the pickle file
        relevant_data = load_relevant_data_from_pkl()

        # Extract relevant fields from the pickle file
        contractId = relevant_data['contractId']
        groupId = relevant_data['groupId']
        propertyId = relevant_data['propertyId']
        propertyVersion = relevant_data['propertyVersion']  # Load new property version

        if not propertyVersion:
            raise Exception("No property version found in the pickle file. Exiting.")

        # Step 3: Activate the new property version on the specified network (STAGING or PRODUCTION)
        print(f"Activating version {propertyVersion} on {network.upper()} network.")  # Debugging
        response = activate_on_akamai(ASK, propertyId, propertyVersion, contractId, groupId, network)

        if response is not None:
            # Step 4: Extract activation link and poll for status
            activation_link = response.json().get('activationLink')

            print("Polling for activation status...")
            while True:
                status = check_activation_status(activation_link)
                if status == "ACTIVE":
                    print(f"Activation on {network.upper()} network completed successfully!")
                    exit(0)  # Success, continue with next steps in GitHub Actions
                elif status == "FAILED":
                    print(f"Activation on {network.upper()} network failed.")
                    exit(1)  # Failure, stop workflow
                else:
                    print(f"Current status: {status}. Waiting to complete...")
                    time.sleep(60)  # Wait 60 seconds before polling again
        else:
            print("Activation failed, skipping polling.")
            exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

import os
import pickle
from credentials import load_switch_key, session, baseurl
from urllib.parse import urljoin
import re

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


def save_relevant_data_to_pkl(new_data):
    """Save the updated relevant data to the pickle file."""

    print('inside save_relevant.....', new_data)
    try:
        existing_data = load_relevant_data_from_pkl()
        print(f"Existing data before update: {existing_data}")

        # Update the existing data with the new data
        existing_data.update(new_data)

        # Save the updated data back to the pickle file
        with open(get_property_pkl_file(), 'wb') as pklfile:
            pickle.dump(existing_data, pklfile)

        print(f"New data: {new_data} saved to {get_property_pkl_file()}")
    except Exception as e:
        print(f"Failed to save data to the pickle file: {e}")


def create_new_version(ASK, propertyId, propertyVersion, contractId, groupId, etag):
    """Create a new property version using the Akamai PAPI API."""
    payload = {
        "createFromVersion": propertyVersion,
        "createFromVersionEtag": etag
    }

    qs = {
        'accountSwitchKey': ASK,
        'contractId': contractId,
        'groupId': groupId
    }

    headers = {
        "accept": "application/json",
        "PAPI-Use-Prefixes": "false",
        "content-type": "application/json"
    }

    url = urljoin(baseurl, f'/papi/v1/properties/{propertyId}/versions')
    response = session.post(url, headers=headers, json=payload, params=qs)

    if response.status_code == 201:
        # Extract the new property version from the response
        new_property_version = int(re.search(r'versions/(\d+)', response.json()['versionLink']).group(1))
        print(f"New property version created: {new_property_version}")
        return new_property_version
    else:
        raise Exception(
            f"Failed to create a new property version. Status code: {response.status_code}. Response: {response.json()}")


if __name__ == '__main__':
    try:
        # Step 1: Load the existing account switch key (ASK)
        switch_key_data = load_switch_key()
        if switch_key_data is None:
            raise Exception("No switch key found.")

        ASK = switch_key_data['switch_key']

        # Step 2: Load relevant data from the pickle file for the property
        relevant_data = load_relevant_data_from_pkl()

        # Extract relevant fields from the pickle file
        contractId = relevant_data['contractId']
        groupId = relevant_data['groupId']
        propertyId = relevant_data['propertyId']
        propertyVersion = relevant_data['propertyVersion']
        etag = relevant_data['etag']
        property_name = relevant_data['propertyName']  # Load property name dynamically

        # Print the property name being processed
        print(f"Creating a new version for property: {property_name}")

        # Step 3: Create a new property version using the loaded data
        new_property_version = create_new_version(ASK, propertyId, propertyVersion, contractId, groupId, etag)

        # Step 4: Save the new property version to the pickle file
        save_relevant_data_to_pkl({'propertyVersion': new_property_version})

        # Step 5: Print the final status
        print(f"New property version {new_property_version} has been successfully created and saved.")

    except Exception as e:
        print(f"An error occurred: {e}")

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

def save_relevant_data_to_pkl(new_data):
    """Load existing data from the pickle file, update it with new data, and save it back."""
    try:
        # Load the existing data from the pickle file
        with open("property_fields.pkl", 'rb') as pklfile:
            existing_data = pickle.load(pklfile)
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty dictionary
        existing_data = {}

    # Update the existing data with the new data
    existing_data.update(new_data)

    # Save the updated data back to the pickle file
    with open("property_fields.pkl", 'wb') as pklfile:
        pickle.dump(existing_data, pklfile)

    print(f"Updated relevant data saved to property_fields.pkl")

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

    response = session.post(urljoin(baseurl, f'/papi/v1/properties/{propertyId}/versions'),
                            headers=headers, json=payload, params=qs)

    if response.status_code == 201:
        # Extract the new property version from the response
        new_property_version = response.json().get('propertyVersion')
        print(f"New property version created: {new_property_version}")
        return new_property_version
    else:
        print(f"Failed to create a new property version. Status code: {response.status_code}")
        print(response.json())
        exit(1)


if __name__ == '__main__':
    # Step 1: Load the existing account switch key (ASK)
    switch_key_data = load_switch_key()
    if switch_key_data is None:
        print("No switch key found. Exiting.")
        exit(1)
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
    print(f"Creating new version for property: {property_name}")

    # Step 3: Create a new property version using the loaded data
    new_property_version = create_new_version(ASK, propertyId, propertyVersion, contractId, groupId, etag)

    # Step 4: Save the new property version to the pickle file
    save_relevant_data_to_pkl({'new_property_version': new_property_version})

    # Step 5: Print the final status
    print(f"New property version {new_property_version} has been successfully created and saved to the pickle file.")

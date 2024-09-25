import os
import pickle
import tempfile  # To get the temp directory in a cross-platform way
from pathlib import Path
from urllib.parse import urljoin
from akamai.edgegrid import EdgeRc, EdgeGridAuth
from requests import Session

# Get the path to the .edgerc file from the environment variable or fallback to the default location
edgerc_path = os.getenv('AKAMAI_EDGERC_PATH', str(Path.home().joinpath('.edgerc')))
EDGERC = EdgeRc(edgerc_path)
SECTION = 'default'
baseurl = f'https://{EDGERC.get(SECTION, "host")}'
session = Session()
session.auth = EdgeGridAuth.from_edgerc(EDGERC, SECTION)

def _get_all_switch_keys(my_account):
    qparam = {'search': my_account}
    resp = session.get(urljoin(baseurl,
                               'identity-management/v3/api-clients/self/account-switch-keys'),
                       params=qparam).json()
    return resp


def generate_switch_key():
    """Generate a new switch key for a different account."""
    my_account = input('Enter account name: ')
    accounts = _get_all_switch_keys(my_account)
    for i, account in enumerate(accounts, start=1):
        print(f'{i}: {account["accountName"]}')
    key_number = int(input('Enter key number: '))
    switch_key = accounts[key_number - 1]['accountSwitchKey']
    account_name = accounts[key_number - 1]['accountName']

    # Store the switch key and account name using pickle
    switch_key_data = {'switch_key': switch_key, 'account_name': account_name}
    with open('switch_key.pkl', 'wb') as local_cache:
        pickle.dump(switch_key_data, local_cache)

    print(f"New switch key stored in file switch_key.pkl for account '{account_name}': {switch_key}")
    return switch_key_data


import os
import pickle


def load_switch_key():
    """
    Load the switch key from the pickle file located in the 'src' folder.

    Returns:
        dict: The switch key data if successfully loaded, None otherwise.
    """
    # Get the current directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the pickle file located in the 'src' folder
    pkl_file_path = os.path.join(current_dir, 'switch_key.pkl')

    # Check if the file exists before trying to open it
    if not os.path.exists(pkl_file_path):
        print(f"Error: Pickle file {pkl_file_path} not found.")
        return None

    try:
        # Load the switch key from the pickle file
        with open(pkl_file_path, 'rb') as f:
            switch_key_data = pickle.load(f)

        # Log and return the switch key data
        print(
            f"Reusing account switch key from file: {switch_key_data['switch_key']} for account '{switch_key_data['account_name']}'")
        return switch_key_data

    except pickle.UnpicklingError:
        print("Error: Failed to unpickle the file. The pickle file may be corrupted.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_or_generate_switch_key():
    """
    Check if a switch key exists, and if so, give the user an option to reuse it.
    If the switch key does not exist or the user chooses not to reuse it, generate a new one.
    This function can be reused by other scripts.
    """
    # Check if a switch key already exists
    switch_key_data = load_switch_key()

    if switch_key_data:
        # Show the user their current switch key and account
        current_switch_key = switch_key_data['switch_key']
        current_account_name = switch_key_data['account_name']
        print(f"You already have a switch key for the account: {current_account_name} (Key: {current_switch_key})")

        # Ask the user if they want to reuse the switch key or generate a new one
        reuse_choice = input(
            f"Do you want to reuse this switch key for account '{current_account_name}'? (y/n): ").strip().lower()

        if reuse_choice == 'y':
            print(f"Reusing switch key for account '{current_account_name}'.")
            return switch_key_data
        else:
            print("Generating a new switch key for a different account...")
            return generate_switch_key()
    else:
        # No existing switch key, generate a new one
        print("No switch key found. Generating a new one...")
        return generate_switch_key()


# Optional: main function for standalone execution
def main():
    get_or_generate_switch_key()


# This ensures the script can still be executed directly but the main logic is reusable by other scripts
if __name__ == '__main__':
    main()

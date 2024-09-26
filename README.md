# Akamai Pipeline Automation

This project provides Python-based automation tools to manage Akamai properties using the Akamai PAPI (Property Manager API). It includes scripts for creating new property versions, activating properties, and updating rule trees on the Akamai platform.

## Project Structure

```plaintext
.
├── .github/
│   └── workflows/
│       └── update_akamai_config.yml  # GitHub Actions for automatic deployment
├── .venv/                             # Virtual environment
├── src/                               # Source code for managing Akamai properties
│   ├── __init__.py                    # Empty initializer for src package
│   ├── activate_on_akamai.py          # Script to activate properties on Akamai networks
│   ├── create_a_new_property_version.py # Script to create a new version of a property
│   ├── credentials.py                 # Script to load or generate credentials for Akamai access
│   ├── property_fields.pkl            # Pickle file storing relevant property fields
│   ├── property_search.py             # Script to search for properties by name
│   ├── switch_key.pkl                 # Pickle file storing account switch key information
│   ├── update_property_rule_tree.py   # Script to update the rule tree of a property version
│   ├── www.cyberabstract.com.json     # JSON file containing rule tree data for a specific property
├── tests/
│   └── test_response.py               # Unit test for response validation
├── .gitignore                         # Git ignore file
├── README.md                          # This file
├── requirements.txt                   # Dependencies
└── scratch.txt                        # Scratch file for notes
## Setup Instructions

### 1. Python Environment Setup

Ensure Python 3.x is installed on your system. Then, install the necessary dependencies by running:

`python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt` 

### 2. Configuring Akamai Credentials

Your Akamai credentials should be stored in the `.edgerc` file, located either in your home directory or in a custom path set via the environment variable `AKAMAI_EDGERC_PATH`.

Example `.edgerc` file:

`[default]
client_secret = <client_secret>
host = <host>
access_token = <access_token>
client_token = <client_token>` 

### 3. Available Scripts

#### Activate on Akamai (`activate_on_akamai.py`)

This script activates a specified property version on either the staging or production network.

`python src/activate_on_akamai.py <network>` 

Where `<network>` is either `staging` or `production`.

The script will:

-   Load credentials and switch key.
-   Fetch the latest property version.
-   Activate the property on the selected network.

#### Create a New Property Version (`create_a_new_property_version.py`)

Creates a new version of an Akamai property based on the latest available version.

`python src/create_a_new_property_version.py` 

#### Update Property Rule Tree (`update_property_rule_tree.py`)

This script updates the rule tree of a property version using the JSON rule tree stored in the `src` directory.

`python src/update_property_rule_tree.py` 

#### Property Search (`property_search.py`)

This script allows searching for a property by its name and fetching its rule tree.

`python src/property_search.py` 

#### Credentials Management (`credentials.py`)

Handles loading and generating Akamai account switch keys (ASK).

-   `load_switch_key()`: Load the stored switch key from `switch_key.pkl`.
-   `generate_switch_key()`: Generate a new account switch key.

### 4. GitHub Actions

A GitHub Actions workflow (`update_akamai_config.yml`) is included for automatic deployment to Akamai staging and production environments. This is triggered upon merging changes into the main branch.
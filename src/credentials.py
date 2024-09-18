from akamai.edgegrid import EdgeRc, EdgeGridAuth
from requests import Session
from urllib.parse import urljoin
from pathlib import Path

EDGERC = EdgeRc(str(Path.home().joinpath('.edgerc')))
SECTION = 'default'
baseurl = f'https://{EDGERC.get(SECTION, "host")}'
session = Session()
session.auth = EdgeGridAuth.from_edgerc(EDGERC, SECTION)

def _get_all_switch_keys(my_account):
    qparam = {
        'search': my_account
    }

    resp = session.get(urljoin(baseurl, 'identity-management/v3/api-clients/self/account-switch-keys'), params=qparam).json()
    return resp

def generate_switch_key():
    my_account = input('Enter account name: ')
    accounts = _get_all_switch_keys(my_account)
    # print(accounts)
    for i, account in enumerate(accounts, start=1):
        print(f'{i}: {account["accountName"]}')
    key_number = int(input('Enter key number: '))
    switch_key =accounts[key_number -1]['accountSwitchKey']
    return switch_key



if __name__ == '__main__':
    print(generate_switch_key())

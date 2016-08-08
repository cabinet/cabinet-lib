#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cabinet import Cabinet


def main():
    # TODO: get this from config?
    account_id = 'my-name@my-company.com'
    password = b'asdfasdf'
    # password = getpass.getpass("Password: ")

    temp_config_path = os.path.join(os.getcwd(), 'test.data', 'secrets')
    test_vault_path = os.path.join(os.getcwd(), 'test.data', 'vaults')
    name = 'test-vault'

    cab = Cabinet(account_id, password, temp_config_path)
    cab.open(name, test_vault_path)
    import pprint
    pprint.pprint(cab.get_all())

    # # uncomment to insert some test data
    # content = {
    #     'username': 'testuser',
    #     'password': 'not so supersecretpassword',
    #     'site-url': 'https://example.com/2',
    #     'notes': '',
    # }
    # item = {
    #     'name': 'test-item #2',
    #     'tags': ['test', 'something', 'blah'],
    #     'content': content,
    # }
    # cab.add(item)

    print('-'*10)
    name = 'test-item #2'
    print(name)
    pprint.pprint(cab.get(name))


if __name__ == "__main__":
    main()

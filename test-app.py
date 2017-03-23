#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random

from cabinet import Cabinet


def get_item(number=None):
    if number is None:
        n = random.randrange(1, 500)
    else:
        n = number

    content = {
        'username': 'testuser #' + str(n),
        'password': 'not so supersecretpassword',
        'site-url': 'https://example.com/login/' + str(n),
        'notes': '',
    }
    item = {
        'name': 'test-item #' + str(n),
        'tags': ['test', 'something', 'blah'],
        'content': content,
    }

    return item


def main():
    account_id = 'my-name@my-company.com'
    password = b'asdfasdf'

    temp_config_path = os.path.join(os.getcwd(), 'test.data', 'secrets')
    test_vault_path = os.path.join(os.getcwd(), 'test.data', 'vaults')
    name = 'test-vault'

    cab = Cabinet(account_id, password, temp_config_path)
    cab.open(name, test_vault_path)

    item = get_item()
    cab.add(item)

    item = get_item(42)
    cab.add(item)

    print('-'*10)
    print("Result for cabinet.get_all():")
    import pprint
    pprint.pprint(cab.get_all())

    print('-'*10)
    name = 'test-item #42'
    print("Result for cabinet.get(name):")
    print(name)
    pprint.pprint(cab.get(name))


if __name__ == "__main__":
    main()

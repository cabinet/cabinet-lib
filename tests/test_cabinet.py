#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import os
import random
import shutil
import unittest

from cabinet import Cabinet


class TestCabinet(unittest.TestCase):

    def setUp(self):
        account_id = 'my-name@my-company.com'
        password = b'asdfasdf'

        self._base_dir = base_dir = os.path.join(os.getcwd(), 'tmp.tests')
        temp_config_path = os.path.join(base_dir, 'secrets')
        test_vault_path = os.path.join(base_dir, 'vaults')
        name = 'test-vault'

        cab = Cabinet(account_id, password, temp_config_path)
        cab.open(name, test_vault_path)

        self.cab = cab

    def _get_item(self, number=None):
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

    def tearDown(self):
        shutil.rmtree(self._base_dir)

    def test_created(self):
        self.assertTrue(os.path.isdir(self._base_dir))

    def test_add_get(self):
        item = self._get_item(42)
        name = item['name']
        self.cab.add(item)
        item_got = self.cab.get(name)

        self.assertEqual(item, item_got)

    def test_add_get_all(self):
        items = {}

        item = self._get_item(42)
        self.cab.add(item)
        del item['content']  # get_all won't return content
        items[item['name']] = item

        item = self._get_item(99)
        self.cab.add(item)
        del item['content']  # get_all won't return content
        items[item['name']] = item

        all_items = self.cab.get_all()

        self.assertEqual(items, all_items)

    def test_add_does_not_modify_item(self):
        item = self._get_item(42)
        item_copy = copy.deepcopy(item)
        self.cab.add(item)
        self.assertEqual(item, item_copy)


if __name__ == '__main__':
    unittest.main()

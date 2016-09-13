#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from cabinet.person import Person


class TestPerson(unittest.TestCase):

    def setUp(self):
        self._base_dir = base_dir = os.path.join(os.getcwd(), 'tmp.tests')
        self._test_path = os.path.join(base_dir, 'test-persons-data')

    def tearDown(self):
        shutil.rmtree(self._base_dir)

    def get_person(self, name='bob', generate_keys=True):
        p = Person(name, self._test_path)
        if generate_keys:
            p.generate_keys()

        return p

    def test_has_secret_key(self):
        bob = self.get_person()

        self.assertTrue(bob.has_secret_key())

    def test_encrypt_decrypt(self):
        alice = self.get_person('alice')
        bob = self.get_person('bob')

        message = b"Hello bob, how are you doing?"
        encrypted = alice.encrypt(message, bob.public_key)
        decrypted = bob.decrypt(encrypted, alice.public_key)

        self.assertEqual(message, decrypted)

    def test_save_load_pk(self):
        bob = self.get_person()
        bob_pk = bob._get_private_key()

        password = b"super secret passphrase"
        bob.save_key(password)
        bob.load_key(password)

        bob_pk2 = bob._get_private_key()
        self.assertEqual(bob_pk, bob_pk2)

    def test_fail_regenerate_keys(self):
        bob = self.get_person()

        # TODO: use a more precise error
        with self.assertRaises(Exception):
            bob.generate_keys()

    def test_fail_load_no_keys(self):
        bob = self.get_person(generate_keys=False)

        # TODO: use a more precise error
        with self.assertRaises(Exception):
            bob.load_key('')


if __name__ == '__main__':
    unittest.main()

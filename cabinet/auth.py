#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import os

from nacl.exceptions import CryptoError

from cabinet.person import Person

VAULTS_PATH = os.path.join(os.getcwd(), 'vaults')


def mkdir_p(path):
    """
    Creates the path and all the intermediate directories that don't
    exist

    Might raise OSError

    :param path: path to create
    :type path: str
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Auth:
    def __init__(self, vault_path):
        self._me = None
        self._vault_path = vault_path
        mkdir_p(os.path.join(vault_path, 'auth'))

    def set_me(self, person):
        self._me = person

    def _decrypt(self, data):
        return self._me.decrypt(data, self._me.public_key)

    def _encrypt(self, data):
        return self._me.encrypt(data, self._me.public_key)

    def get_vault_key(self):
        key_path = os.path.join(self._vault_path, 'auth', 'key.dat')
        return self._get_vault_key(key_path)

    def create_vault_key(self):
        import nacl.secret
        import nacl.utils

        # This must be kept secret, this is the combination to your safe
        key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        key_path = os.path.join(self._vault_path, 'auth', 'key.dat')
        self._add_vault_key(key_path, key)

    def initialized(self):
        key_file = os.path.join(self._vault_path, 'auth', 'key.dat')
        return os.path.isfile(key_file)

    def setup_me(self, name, password):
        me = Person(name)
        me.generate_keys()
        me.save_key(password)
        self._me = me

    def _add_vault_key(self, filename, data):
        b_encrypted_data = self._encrypt(data)
        encrypted_data = b_encrypted_data.decode('utf-8')

        with open(filename, 'a') as f:
            f.write(encrypted_data)
            f.write('\n')

    def _get_vault_key(self, filename):
        # Cycle each line on the file until one can be decrypted with the given
        # decryptor
        b_decrypted_data = None
        with open(filename, 'r') as f:
            for encrypted_line in f:
                try:
                    b_decrypted_data = self._decrypt(encrypted_line)
                except CryptoError:
                    continue  # couldn't decrypt this line
                break

        if b_decrypted_data is None:
            return None

        # print(type(b_decrypted_data))
        # print(repr(b_decrypted_data))
        # import ipdb
        # ipdb.set_trace()
        # decrypted_data = b_decrypted_data.decode('utf-8')
        decrypted_data = b_decrypted_data
        return decrypted_data

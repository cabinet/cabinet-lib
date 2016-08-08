#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import os

import nacl.utils

from nacl.public import PrivateKey, Box

from .utils import CryptoHelper


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


class Person:
    def __init__(self, account_id, config_path):
        self._account_id = account_id
        self._config = os.path.join(config_path, account_id)
        mkdir_p(self._config)

    def has_secret_key(self):
        key_file = os.path.join(self._config, 'secret.key')
        return os.path.isfile(key_file)

    def load_secret_key(self, key):
        pk = PrivateKey(key, encoder=nacl.encoding.Base64Encoder)
        self.public_key = pk.public_key
        self._private_key = pk

    def generate_keys(self):
        self._private_key = PrivateKey.generate()
        self.public_key = self._private_key.public_key

    # def encrypt_to(self, message, public_key):
    def encrypt(self, message, public_key, base64=True):
        box = Box(self._private_key, public_key)
        nonce = nacl.utils.random(Box.NONCE_SIZE)
        # encrypted = box.encrypt(message, nonce)
        if base64:
            encrypted = box.encrypt(message, nonce,
                                    encoder=nacl.encoding.Base64Encoder)
        else:
            encrypted = box.encrypt(message, nonce)
        return encrypted

    # def decrypt_from(self, data, public_key):
    def decrypt(self, data, public_key, base64=True):
        box = Box(self._private_key, public_key)
        # decrypted = box.decrypt(data)
        if base64:
            decrypted = box.decrypt(data, encoder=nacl.encoding.Base64Encoder)
        else:
            decrypted = box.decrypt(data)

        return decrypted

    def get_public_key(self):
        return self.public_key.encode(encoder=nacl.encoding.Base64Encoder)

    def _get_private_key(self, encoded=False):
        if encoded:
            return self._private_key.encode(
                encoder=nacl.encoding.Base64Encoder)
        else:
            return self._private_key.encode()

    def save_key(self, password):
        key_file = os.path.join(self._config, 'secret.key')

        data = self._private_key.encode(encoder=nacl.encoding.Base64Encoder)
        ch = CryptoHelper()
        encrypted_secret = ch.encrypt(data, password, self._account_id)

        with open(key_file, 'wb') as f:
            f.write(bytes(encrypted_secret))

    def load_key(self, password):
        key_file = os.path.join(self._config, 'secret.key')

        data = None
        with open(key_file, 'r') as f:
            data = f.readline()

        ch = CryptoHelper()
        secret_key = ch.decrypt(data, password, self._account_id)
        self.load_secret_key(secret_key)

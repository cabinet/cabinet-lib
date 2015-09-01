#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gnupg


DEFAULT_PARAMS = {
    'name_comment': None,
    # 'expire_date': None,  # FIXME: one year?
    'key_type': 'RSA',
    'key_usage': 'encrypt,sign,auth',
    'key_length': 1024,  # FIXME: rise for production
    # 'subkey_type': None,
    'subkey_length': None,
    # 'keyserver': None,
    'preferences': None,
}


class GPGHelper(object):
    def __init__(self, homedir):
        self._gpg = gnupg.GPG(homedir=homedir)

    def _generate_batch(self, name, email, password):
        params = DEFAULT_PARAMS
        params.update({
            'name_real': name,
            'name_email': email,
            'passphrase': password,
        })
        batch = self._gpg.gen_key_input(**params)

        return batch

    def get_key(self, fingerprint):
        # Using '--fingerprint' twice will display subkey fingerprints too:
        # gpg.options = ['--fingerprint', '--fingerprint']
        keylist = self._gpg.list_keys(secret=True)

        for key in keylist:
            if key['fingerprint'] == fingerprint:
                return key

    def display_keys(self):
        # Using '--fingerprint' twice will display subkey fingerprints too:
        self._gpg.options = ['--fingerprint', '--fingerprint']
        keylist = self._gpg.list_keys(secret=True)

        # `result` is a `gnupg._parsers.ListKeys`, which is list-like, so
        # iterate over all the keys and display their info:
        for gpgkey in keylist:
            for k, v in gpgkey.items():
                print("%s: %s" % (k.capitalize(), v))

        print '-'*20
        print keylist

    def create_key(self, name, email, password):
        batch = self._generate_batch(name, email, password)
        key = self._gpg.gen_key(batch)
        print dir(key)

        if not key.fingerprint:
            print("Key creation seems to have failed: %s" % key.status)
            print key.stderr
            raise Exception

        return key.fingerprint

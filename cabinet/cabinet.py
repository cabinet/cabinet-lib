#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cabinet.auth import Auth
from cabinet.vault import Vault
from cabinet.person import Person

BASE_PATH = os.path.join(os.path.expanduser('~'), '.config', 'cabinet')
CONFIG_PATH = os.path.join(BASE_PATH, 'secrets')
VAULTS_PATH = os.path.join(BASE_PATH, 'vaults')


class Cabinet:
    def __init__(self, account_id, password, config_path=CONFIG_PATH):
        self._config_path = config_path
        self._account_id = account_id
        self._password = password
        self._vault = None

    def _load_me(self):
        me = Person(self._account_id, config_path=self._config_path)
        if me.has_secret_key():
            me.load_key(self._password)
        else:
            me.generate_keys()
            me.save_key(self._password)

        return me

    def _open_vault(self):
        me = self._load_me()

        auth = Auth(self._vault_path)
        auth.set_me(me)
        if not auth.initialized():
            auth.create_vault_key()

        vault_key = auth.get_vault_key()
        vault = Vault(self._vault_path)
        vault.open(vault_key)

        self._vault = vault

    def open(self, name, path=BASE_PATH):
        self._vault_path = os.path.join(path, name)
        self._open_vault()

    def get_all(self):
        return self._vault.get_all()

    def get(self, name):
        return self._vault.get(name)

    def add(self, item):
        self._vault.add(item)

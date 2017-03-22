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
        if isinstance(password, str):
            # password must be bytes
            password = password.encode('utf-8')

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

    def get_tags(self):
        return self._vault.get_tags()

    def get_by_tags(self, tags=None):
        """
        Recover all the items that contains the given tags.

        :param tags: A list of tags
        :ptype tags: List

        :returns: The list of items filtered by tags.
        :type: List of Dictionaries
        """
        if tags is None:
            tags = []

        item_list = self.get_all().values()
        return [item for item in item_list
                if set(tags).issubset(item['tags'])]

    def add(self, item):
        """Add an item.

        :param item: the item is a dict of the form:
        :ptype item: Dictionary

        {
          'name': 'the name of this item',
          'tags': ['test', 'something', 'blah'],
          'content': content_of_any_kind,
        }

        name and content are mandatory, tags can be None.

        """

        name = item['name']
        content = item['content']
        tags = item.get('tags')

        self.add_new(name, content, tags)

    def add_new(self, name, content, tags=None):
        """Add a new item to the Vault.

        :param name: the name of the new item
        :type name: str

        :param content: the content of the new item
        :type content: any

        :param tags: the tags for the new content
        :type tags: list

        Note: eventually, this should be just `add` but is named `add_new` to
        avoid breaking existing code.
        """
        if tags is None:
            tags = []

        item = {
            'name': name,
            'tags': tags,
            'content': content,
        }
        self._vault.add(item)

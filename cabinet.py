#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This is the first cli prototype for the cabinet core.
#
# References;
#   argparse : https://docs.python.org/3/library/argparse.html
#   cement   : http://builtoncement.com/2.10/index.html
#
# TODO:
#   - Move the cli to it's own repo (inside a new 'Cabinet' organization).
#   - Refactor the code to move each class, utils to its own module.

import os
import argparse

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from cabinet import Cabinet

VERSION = '0.0.1'
BANNER = """
Cabinet command line v{0}
GNU GENERAL PUBLIC LICENSE
""".format(VERSION)


class CabinetWrapper:
    """
    A wrapper to easely use the cabinet library.

    TODO: In the future we should try moving this all to the library.
    """

    def __init__(self):
        current_path = os.getcwd()
        join = os.path.join
        self.config_path = join(current_path, 'test.data', 'secrets')
        self.default_vault_path = join(current_path, 'test.data', 'vaults')
        self.load_credentials()

    def load_credentials(self):
        """
        TODO: Implement reading credentials from stdin.
        TODO: Implement reading credentials from config file.
        """
        self.account_id = 'my-name@my-company.com'
        self.password = 'asdfasdf'
        self.vault_name = 'test-vault'
        return self.open_vault(self.account_id, self.password, self.vault_name)

    def open_vault(self, account_id, password, vault_name, vault_path=None):
        """
        Open the vault identified by the vault_name, vault_path.

        Params:
        :param account_id:
        :type: String
        :param password:
        :type: String
        :param vault_name: The name of the vault
        :type: String
        :param vault_path: The location of the vault.
        :type: String

        TODO: Implement account_id/password/vault validation and opening
        """

        if vault_path is None:
            vault_path = self.default_vault_path

        self.cab = Cabinet(account_id, password, self.config_path)
        self.cab.open(vault_name, vault_path)

        # TODO: Add open check. For this, the vault should verify keys
        return True

    def get_all(self):
        """
        Get all the items from the vault without the 'content' (i.e: only name
        and tags).

        :returns: The list of items
        :type: List of Dictionaries.
        """
        return self.cab.get_all()

    def get_item(self, name):
        """
        Get an item from the vault.

        :param name: The name of the item to recover.
        :type: String

        :returns: The item with the specified name.
        :type: Dictionary
        """
        return self.cab.get(name)

    def add_item(self, item):
        """
        Add an item to the vault.

        :param item: The item to be added.
        :type: Dictionary
        """
        self.cab.add(item)


# TODO: Move the types out of this file, to a type folder/file. ###############
def tags_type(value):
    """
    Parse the value to recover a list of tags.

    :param value: The value to parse
    :type: String

    :returns: A list of strings composed by spliting the value by ','.
    :type: List
    """
    try:
        return value.split(',')
    except:
        raise argparse.argumenttypeerror("Multiple tags should be separated by\
                                          comma")


def tuple_type(value):
    """
    Parse the value to recover a tuple

    :param value: The value to parse
    :type: String

    :returns: A tuple of two values composed by spliting the value by ','.
    :type: Tuple
    """
    try:
        key, value = value.split(',')
        return key, value
    except:
        raise argparse.argumenttypeerror("coordinates must be x,y,z")

###############################################################################


class CabinetController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Cabinet's cli client for managing vaults."
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER))
        ]

    @expose(hide=True)
    def default(self):
        """Without any parameter, the command will print the help"""
        app.args.print_help()


class ItemController(CementBaseController):
    class Meta:
        label = 'item'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['name'],
             dict(help='The item name.', action='store')),
            (['-t', '--tag'],
             dict(help='Add a tag to the item', action='append')),
            (['--tags'],
             dict(help='Add multiple separated comma tags',
                  type=tags_type, action='store')),
            (['--content'],
             dict(help='Add content to the item',
                  type=tuple_type, action='append'))
        ]

    @expose(help='Get an item from the vault.')
    def get(self):
        """Get an item from the vault"""
        name = self.app.pargs.name
        if name:
            self.app.log.debug('Looking for item with name "{0}"'.format(name))
            cab = CabinetWrapper()
            if cab.load_credentials():
                item = cab.get_item(name)
                if item:
                    print(item)
                else:
                    print('Item with name "{0}" not found!'.format(name))

    @expose(help="Add an item to the vault.")
    def add(self):
        """Add an item to the vault"""
        name = self.app.pargs.name
        tags = self.app.pargs.tags
        if not tags:
            tags = [] if not self.app.pargs.tag else self.app.pargs.tag
        content = [] if not self.app.pargs.content else self.app.pargs.content

        content_obj = {}
        for key, value in content:
            content_obj[key] = value

        if name:
            cab = CabinetWrapper()
            if cab.load_credentials():
                cab.add_item({
                    'name': name,
                    'tags': tags,
                    'content': content_obj
                })
        else:
            print('Insufficient arguments!')


class SearchController(CementBaseController):
    """The command controller for searching within the vault values"""

    class Meta:
        label = 'search'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['-s', '--show-tags'],
             dict(help='Show items with tags.', action='store_true')),
            (['-t', '--tag'],
             dict(help='Filter by tag', action='append')),
            (['--tags'],
             dict(help='Filter by multiple tags',
                  type=tags_type, action='store')),
            (['extra_arguments'],
             dict(action='store', nargs='*')),
        ]

    # TODO: Think where should go the item filter (In the cabinet or here?)
    @expose(help='Get all the items in the vault.')
    def default(self):
        """Print all the item names (and tags if apply) to stdout."""
        tags = self.app.pargs.tags
        if not tags:
            tags = [] if not self.app.pargs.tag else self.app.pargs.tag
        tag_tpl = " tagged with {1}" if self.app.pargs.show_tags else ''
        cab = CabinetWrapper()
        if cab.load_credentials():
            item_list = cab.get_all().values()
            item_list = [item for item in item_list
                         if set(tags).issubset(item['tags'])]
            print("The following items was found:")
            for item in item_list:
                print(('\t-"{0}"' + tag_tpl).format(item['name'],
                                                    item['tags']))


class MyApp(CementApp):
    class Meta:
        label = 'cabinet'
        base_controller = 'base'
        handlers = [CabinetController, ItemController, SearchController]


with MyApp() as app:
    app.run()

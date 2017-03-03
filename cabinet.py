#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# References;
#   argparse : https://docs.python.org/3/library/argparse.html
#   cement   : http://builtoncement.com/2.10/index.html
import os
import argparse

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from cabinet import Cabinet

VERSION = '0.9.1'
BANNER = """
Cabinet command line v{0}
GNU GENERAL PUBLIC LICENSE
""".format(VERSION)

config_path = os.path.join(os.getcwd(), 'test.data', 'secrets')
vault_path = os.path.join(os.getcwd(), 'test.data', 'vaults')

# GLOBAL config object
vault_config = {
    'config_path': config_path,
    'vault_path': vault_path,
    'vault_name': None,
    'account_id': None,
    'password': None,
    'cabinet': None,
}


def open_vault(username, password, vault_name, vault_path=None):
    """
    Open the vault identified by the vault_name, vault_path.

    Params:
    :param username:
    :ptype: String
    :param password:
    :ptype: String
    :param vault_name: The name of the vault
    :ptype: String
    :param vault_path: The location of the vault.
    :ptype: String

    TODO: Implement username/password/vault validation and opening
    """

    global vault_config
    config_path = vault_config.get('config_path')
    if vault_path is None:
        vault_path = vault_config.get('vault_path')

    cab = Cabinet(username, password, config_path)
    cab.open(vault_name, vault_path)
    vault_config['cabinet'] = cab

    return True  # TODO: Add open check. For this, the vault should verify keys


def get_all():
    """
    Get all the items from the vault without the 'content' (i.e: only name and
    tags).

    :returns: The list of items
    :ptype: List of Dictionaries.
    """
    global vault_config
    cab = vault_config.get('cabinet')
    return cab.get_all()


def get_item(name):
    """
    Get an item from the vault.

    :param name: The name of the item to recover.
    :ptype: String

    :returns: The item with the specified name.
    :ptype: Dictionary
    """
    global vault_config
    cab = vault_config.get('cabinet')
    return cab.get(name)


def add_item(item):
    """
    Add an item to the vault.

    :param item: The item to be added.
    :ptype: Dictionary
    """
    global vault_config
    cab = vault_config.get('cabinet')
    cab.add(item)


def tags(value):
    """
    Parse the value to recover a list of tags.

    :param value: The value to parse
    :ptype: String

    :returns: A list of strings composed by spliting the value by ','.
    :rtype: List
    """
    try:
        return value.split(',')
    except:
        raise argparse.argumenttypeerror("Multiple tags should be separated by\
                                          comma")


def tuple(value):
    """
    Parse the value to recover a tuple

    :param value: The value to parse
    :ptype: String

    :returns: A tuple of two values composed by spliting the value by ','.
    :rtype: Tuple
    """
    try:
        key, value = value.split(',')
        return key, value
    except:
        raise argparse.argumenttypeerror("coordinates must be x,y,z")


class CabinetController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Cabinet's cli client for managing valuts."
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
                  type=tags, action='store')),
            (['--content'],
             dict(help='Add content to the item',
                  type=tuple, action='append'))
        ]

    @expose(help='Get an item from the vault.')
    def get(self):
        """Get an item from the vault"""
        name = self.app.pargs.name
        if name:
            self.app.log.debug('Looking for item with name "{0}"'.format(name))
            account_id = 'my-name@my-company.com'
            password = 'asdfasdf'
            vault_name = 'test-vault'
            if open_vault(account_id, password, vault_name):
                item = get_item(name)
                if item:
                    print(item)
                else:
                    print('Item with name "{0}" not found!'.format(name))

    @expose(help="Add an item to the vault.")
    def add(self):
        """Add an item to the vault"""
        account_id = 'my-name@my-company.com'
        password = 'asdfasdf'
        vault_name = 'test-vault'
        name = self.app.pargs.name
        tags = self.app.pargs.tags
        if not tags:
            tags = [] if not self.app.pargs.tag else self.app.pargs.tag
        content = [] if not self.app.pargs.content else self.app.pargs.content

        content_obj = {}
        for key, value in content:
            content_obj[key] = value

        if name:
            if open_vault(account_id, password, vault_name):
                add_item({
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
                  type=tags, action='store')),
            (['extra_arguments'],
             dict(action='store', nargs='*')),
        ]

    # TODO: Think where should go the item filter (In the cabinet or here?)
    @expose(help='Get all the items in the vault.')
    def default(self):
        """Print all the item names (and tags if apply) to stdout."""
        account_id = 'my-name@my-company.com'
        password = 'asdfasdf'
        vault_name = 'test-vault'
        tags = self.app.pargs.tags
        if not tags:
            tags = [] if not self.app.pargs.tag else self.app.pargs.tag
        tag_tpl = " tagged with {1}" if self.app.pargs.show_tags else ''
        if open_vault(account_id, password, vault_name):
            all = get_all().values()
            all = [item for item in all if set(tags).issubset(item['tags'])]
            print("The following items was found:")
            for item in all:
                print(('\t-"{0}"' + tag_tpl).format(item['name'],
                                                    item['tags']))


class MyApp(CementApp):
    class Meta:
        label = 'cabinet'
        base_controller = 'base'
        handlers = [CabinetController, ItemController, SearchController]


with MyApp() as app:
    app.run()

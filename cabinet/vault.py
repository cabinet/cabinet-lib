#!/usr/bin/env python
# encoding: utf-8
import copy
import json
import os

from uuid import uuid4

from cabinet.utils import CryptoHelper, mkdir_p


class Vault(object):
    """
    Safe data vault representation.

    An item has this structure:

    example_item = {
        'name': 'the name of this item',
        'tags': ['test', 'something', 'blah'],
        'content': content_of_any_kind,
    }

    Each item is stored in 2 parts/files: data and metadata.
    The data file contains the 'content'.

    The metadata file contains the 'name', 'tags', and 'hashname'.
    The 'hashname' stored on the metadata file is the name of the file on which
    is stored its corresponding 'data'.
    """

    def __init__(self, path):
        self._base_path = path
        self._tags = {}
        self._names = {}
        self._metadata_paths = {}

        metadata_path = os.path.join(self._base_path, 'metadata')
        data_path = os.path.join(self._base_path, 'data')
        mkdir_p(metadata_path)
        mkdir_p(data_path)

    def add(self, item):
        """Add a new item to the vault.

        :param item: the item to add
        :type item: dict
        """
        if self.get(item['name']) is not None:
            raise Exception("An item with that name already exists")

        metadata = copy.deepcopy(item)

        name = metadata['name']
        content = metadata['content']
        del metadata['content']  # no content along with metadata

        self._names[name] = metadata
        self._tags[name] = metadata['tags']

        # get random name for the contents file
        fname = uuid4().hex
        metadata['hashname'] = fname

        # get random name for the metadata file
        fname = uuid4().hex
        metadata_path = os.path.join(self._base_path, 'metadata')
        fname = os.path.join(metadata_path, fname)
        self._file_write(fname, metadata)

        fname = metadata['hashname']
        data_path = os.path.join(self._base_path, 'data')
        fname = os.path.join(data_path, fname)
        self._file_write(fname, content)

    def update(self, name, new_item):
        """Update the item named as `name` with the item `new_item`.

        :param name: the name of the item to update
        :type name: str
        :param new_item: the new item's contents
        :type new_item: dict
        """
        item = self.get(name, full=True)

        if item is None:
            raise Exception("The specified item does not exist.")

        self._tags[name] = new_item['tags']
        new_item['hashname'] = item['hashname']

        content = new_item['content']
        del new_item['content']  # no content on the metadata
        self._names[name] = new_item

        metadata_file, content_file = self._get_item_paths(name)

        self._file_write(metadata_file, new_item)
        self._file_write(content_file, content)

    def _get_item_paths(self, name):
        metadata_file = os.path.join(self._base_path, 'metadata',
                                     self._metadata_paths[name])

        content_file = os.path.join(self._base_path, 'data',
                                    self._names[name]['hashname'])

        return metadata_file, content_file

    def rename(self, name, new_name):
        """Rename the item named `name` as `new_name`.

        :param name: the name of the item to rename
        :type name: str
        :param new_name: the new item's name
        :type new_name: str
        """
        item = self.get(name, True)

        if item is None:
            raise Exception("The specified item does not exist.")

        item['name'] = new_name
        self._names[new_name] = item

        metadata_file, _ = self._get_item_paths(name)
        self._file_write(metadata_file, item)
        del self._names[name]

    def get(self, name, full=False):
        """Return the item with the given `name`.

        :param name: the name of the item to return
        :type name: str
        :param full: whether we want to include all the available information
                     on the item or not. Right now it only adds the `hashname`.
        :type full: bool
        """
        metadata = copy.deepcopy(self._names.get(name))

        if metadata is None:
            return

        fname = metadata['hashname']
        data_path = os.path.join(self._base_path, 'data')
        fname = os.path.join(data_path, fname)
        content = self._file_read(fname)
        metadata['content'] = content

        if not full:
            # hashname is not returned to the user, its goal is just to find
            # information on the disk
            del metadata['hashname']

        return metadata

    def get_tags(self):
        """Return the list of all available tags."""
        return list(self._tags.keys())

    def get_all(self):
        all_items = copy.deepcopy(self._names)

        # remove randomly generated hashes
        for k in all_items:
            del all_items[k]['hashname']

        return all_items

    def remove(self, name):
        # TODO:
        # remove from names
        # remove from tags
        # remove metadata file
        # remove data file
        # add test for this
        pass

    def _load_metadata(self):
        metadata_path = os.path.join(self._base_path, 'metadata')
        tags = {}
        names = {}
        metadata_paths = {}

        for fname in os.listdir(metadata_path):
            file_path = os.path.join(metadata_path, fname)
            obj = self._file_read(file_path)
            name = obj['name']
            names[name] = obj
            metadata_paths[name] = fname

            for tag in obj['tags']:
                if tags.get(tag):
                    tags[tag].append(fname)
                else:
                    tags[tag] = [fname]

        self._tags = tags
        self._names = names
        self._metadata_paths = metadata_paths

    def open(self, key):
        self._key = key
        # TODO: test key
        self._load_metadata()

    def _encrypt(self, data):
        # maybe base this on a random string created along the vault
        salt = 'this must be rethinked!'
        ch = CryptoHelper()
        return ch.encrypt(data, self._key, salt)

    def _decrypt(self, data):
        salt = 'this must be rethinked!'
        ch = CryptoHelper()
        return ch.decrypt(data, self._key, salt)

    def _file_read(self, filename):
        encrypted_data = None
        with open(filename, 'r') as f:
            encrypted_data = f.read()

        b_decrypted_data = self._decrypt(encrypted_data)
        decrypted_data = b_decrypted_data.decode('utf-8')
        json_data = decrypted_data
        data = json.loads(json_data)

        return data

    def _file_write(self, filename, obj):
        json_data = json.dumps(obj)
        b_json_data = json_data.encode('utf-8')
        encrypted_data = self._encrypt(b_json_data)
        encrypted_data = encrypted_data.decode()
        with open(filename, 'w') as f:
            f.write(encrypted_data)

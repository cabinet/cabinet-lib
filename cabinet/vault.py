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

        metadata_path = os.path.join(self._base_path, 'metadata')
        data_path = os.path.join(self._base_path, 'data')
        mkdir_p(metadata_path)
        mkdir_p(data_path)

    def add(self, item):
        metadata = copy.deepcopy(item)

        name = metadata['name']
        content = metadata['content']
        del metadata['content']  # no content along with metadata

        self._names[name] = metadata
        self._tags[name] = metadata['tags']

        fname = uuid4().hex
        metadata['hashname'] = fname

        fname = uuid4().hex
        metadata_path = os.path.join(self._base_path, 'metadata')
        fname = os.path.join(metadata_path, fname)
        self._file_write(fname, metadata)

        fname = metadata['hashname']
        data_path = os.path.join(self._base_path, 'data')
        fname = os.path.join(data_path, fname)
        self._file_write(fname, content)

    def get(self, name):
        metadata = copy.deepcopy(self._names.get(name))

        if metadata is None:
            return

        fname = metadata['hashname']
        data_path = os.path.join(self._base_path, 'data')
        fname = os.path.join(data_path, fname)
        content = self._file_read(fname)
        metadata['content'] = content

        # hashname is not returned to the user, its goal is just to find
        # information on the disk
        del metadata['hashname']

        return metadata

    def get_tags(self):
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

        for fname in os.listdir(metadata_path):
            file_path = os.path.join(metadata_path, fname)
            obj = self._file_read(file_path)
            names[obj['name']] = obj

            for tag in obj['tags']:
                if tags.get(tag):
                    tags[tag].append(fname)
                else:
                    tags[tag] = [fname]

        self._tags = tags
        self._names = names

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

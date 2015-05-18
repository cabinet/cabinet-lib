#!/usr/bin/env python
# encoding: utf-8

"""
This class is meant to be a helper to store files/folders and don't use the
actual name in the filesystem.
The idea is to save a mapping of the actual filename and the random generated
filename and then encrypt it.
"""

import base64
import os


class RandomTree(object):
    def __init__(self):
        self._map = {}
        # TODO: decrypt, load

    def _get_random_name(self):
        r = os.urandom(32)
        return base64.urlsafe_b64encode(r)

    def _save(self, name, value):
        self._map[name] = value
        # TODO: persist, encrypt

    def add_node(self, name):
        rnd_name = self._get_random_name()
        self._save(name, rnd_name)

    def get_node(self, name):
        return self._map[name]

    def list_nodes(self):
        return self._map.keys()


def main():
    t = RandomTree()

    t.add_node('secret-note')
    t.add_node('ivan/test')
    t.add_node('ivan/gmail-account')
    t.add_node('unx/bank-passwords')
    t.add_node('unx/admin-mail')
    t.add_node('unx/ISPConfig')

    from pprint import pprint
    pprint(t._map)
    # print self._map

    print
    key = 'unx/admin-mail'
    print key, '->', t.get_node(key)
    print t.list_nodes()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# encoding: utf-8

"""
This class is meant to be a helper to store files/folders and don't use the
actual name in the filesystem.
The idea is to save a mapping of the actual filename and the random generated
filename and then encrypt it.
"""

import base64
import json
import os


class RandomTree(object):
    def __init__(self, storage_path):
        self._json_path = storage_path
        self._map = {}
        # TODO: decrypt, load
        self._load_map()

    def _get_random_string(self):
        # r = os.urandom(32)
        # return base64.urlsafe_b64encode(r)
        # shorter, easier to read on tests
        r = os.urandom(16)
        return base64.b16encode(r)

    def _save_map(self):
        with open(self._json_path, 'w') as f:
            f.write(json.dumps(self._map))

    def _load_map(self):
        jdata = None
        try:
            with open(self._json_path, 'r') as f:
                jdata = json.load(f)
        except IOError:
            pass

        if jdata is not None:
            self._map = jdata

    def _get_random_name(self, name):
        """
        Return a random name for the given name, reusing existing names and
        paths previously generated.

        partial names reuse example:
            some/ -> randomA
            some/thing/ -> randomA/randomB
            some/thing/test -> randomA/randomB/randomC

        :param name: the real node name
        :type name: str
        :return: the random node name
        :rtype: str
        """
        # print '-'*10
        # print "name:", name

        rnd_path = ''
        real_path = ''
        for d in name.split('/'):
            if real_path:
                real_path += '/'
            real_path += d

            # print 'd:', d
            if rnd_path:
                rnd_path += '/'
            if self._map.get(d):  # if this part already exists reuse it
                rnd_path += self._map[d]
            else:
                rnd_path += self._get_random_string()

            self._map[real_path] = rnd_path

        if not rnd_path:
            rnd_path = name

        # print "real_path -> rnd_path:", real_path, '->', rnd_path
        # from pprint import pprint
        # print "self._map:"
        # pprint(self._map)
        # print '-'*10

        return rnd_path

    def add_node(self, name):
        """
        Add a node to the Vault and return the generated random name.
        If the node already exists, return the existing name.
        """
        if self._map.get(name):
            # raise Exception("The node '{0}' already exist.".format(name))
            return self._map[name]

        random_name = self._get_random_name(name)
        self._map[name] = random_name

        # TODO: check if the name we want to save doesn't already exist
        # TODO: persist, encrypt
        self._save_map()
        return random_name

    def get_node(self, name):
        return self._map[name]

    def list_nodes(self):
        return self._map.keys()


def main():
    t = RandomTree('./tmp/random.tree/file_names.json')
    # t.add_node('ivan/test/demo-mail')
    # t.add_node('ivan/asdf')
    # t.add_node('ivan/asdf')
    # return

    try:
        t.add_node('secret-note')
        t.add_node('ivan/test-data')
        t.add_node('ivan/gmail-account')
        t.add_node('unx/bank-passwords')
        t.add_node('unx/admin-mail')
        t.add_node('unx/ISPConfig')
        t.add_node('ivan/test/demo-mail')
    except Exception as e:
        print repr(e)

    from pprint import pprint
    pprint(t._map)
    # print self._map

    print
    key = 'unx/admin-mail'
    print key, '->', t.get_node(key)
    print t.list_nodes()

if __name__ == '__main__':
    main()

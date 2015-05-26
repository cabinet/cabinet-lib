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
    BASE_PATH = './random.tree/'

    def __init__(self):
        self._map = {}
        # TODO: decrypt, load
        self._load_map()

    def _get_random_name(self):
        # r = os.urandom(32)
        # return base64.urlsafe_b64encode(r)
        # shorter, easier to read on tests
        r = os.urandom(16)
        return base64.b16encode(r)

    def _save_map(self):
        with open(self.BASE_PATH + 'file_names.json', 'w') as f:
            f.write(json.dumps(self._map))

    def _load_map(self):
        jdata = None
        try:
            with open(self.BASE_PATH + 'file_names.json', 'r') as f:
                jdata = json.load(f)
        except IOError:
            pass

        if jdata is not None:
            self._map = jdata

    def add_node(self, name):
        # partial names?
        # some/ -> randomA
        # some/thing/ -> randomA/randomB
        # some/thing/test -> randomA/randomB/randomC
        # if some of the random paths are already created we should use them
        # import ipdb; ipdb.set_trace()
        if self._map.get(name):
            raise Exception("The node already exist.")

        print '-'*10
        print "name:", name
        rnd_path = ''
        real_path = ''
        for d in name.split('/'):
            if real_path:
                real_path += '/'
            real_path += d

            print 'd:', d
            if rnd_path:
                rnd_path += '/'
            if self._map.get(d):
                rnd_path += self._map[d]
            else:
                rnd_path += self._get_random_name()
            self._map[real_path] = rnd_path

        if not rnd_path:
            rnd_path = name

        print "real_path -> rnd_path:", real_path, '->', rnd_path
        from pprint import pprint
        print "self._map:"
        pprint(self._map)
        self._map[name] = rnd_path
        # TODO: check if the name we want to save doesn't already exist
        # TODO: persist, encrypt
        # self._save_map()
        print '-'*10

    def get_node(self, name):
        return self._map[name]

    def list_nodes(self):
        return self._map.keys()


def main():
    t = RandomTree()
    t.add_node('ivan/test/demo-mail')
    t.add_node('ivan/asdf')
    return

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

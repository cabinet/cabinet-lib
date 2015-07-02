#!/usr/bin/env python
# encoding: utf-8

"""
This class is meant to be a helper to store files/folders and don't use the
actual name in the filesystem.
The idea is to save a mapping of the actual filename and the random generated
filename and then encrypt it.
"""

import base64
import errno
import os
import re
import subprocess

import gnupg


def mkdir_p(path):
    """
    Creates the path and all the intermediate directories that don't
    exist

    Might raise OSError

    :param path: path to create
    :type path: str
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class SimpleGPG(object):
    def test(self):
        filename = 'test2.asc'
        command = ["gpg", "-q", "--list-packets", "--no-use-agent",
                   "--passphrase", "asdf", filename]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        there = re.compile(r'name=".*"')
        print ''.join(there.findall(output))


class GPGTree(object):
    BASE_PATH = './tmp/gpg.tree/test-files-tree/'

    def __init__(self):
        self._gpg = gnupg.GPG()
        self._key = 'TestPassphrase'

    def _encrypt(self, data, key):
        encrypted = self._gpg.encrypt(data, encrypt=False,
                                      symmetric=True, passphrase=key)

        if not encrypted.ok:
            print encrypted.stderr
            return None

        return encrypted.data

    def _decrypt(self, data, key):
        decrypted = self._gpg.decrypt(data, passphrase=key)

        if not decrypted.ok:
            print decrypted.stderr
            return None

        return decrypted.data

    def _get_random_name(self):
        r = os.urandom(5)
        # return base64.urlsafe_b64encode(r)
        return base64.b16encode(r)

    def add_node(self, name, data):
        rnd_name = self._get_random_name()
        orig_name = os.path.join(self.BASE_PATH, name)
        orig_folder = os.path.dirname(orig_name)

        if '/' in name:
            base_name = '/'.join(name.split('/')[:-1])
        else:
            base_name = ''

        rnd_path = os.path.join(self.BASE_PATH, base_name, rnd_name)

        # XXX: this method does not store the filename in a packet
        # I think that there is a missing feature on python-gnupg
        # encrypted_data = self._encrypt(data, self._key)
        # with open(rnd_path, 'w') as f:
        #     f.write(encrypted_data)

        # alternative method:
        mkdir_p(orig_folder)
        with open(orig_name, 'w') as f:
            f.write(data)

        self._encrypt_file(orig_name)
        os.rename(orig_name, rnd_path)

    def _encrypt_file(self, filename):
        """ this is a temporary hack, we should use python-gnupg, the problem
        is that it does not provide an api to store strings filenames on
        packets"""
        command = ["gpg", "-c", "--batch", "--yes", "--no-use-agent",
                   "--passphrase", self._key, "-o", filename, filename]
        output = subprocess.check_output(command)
        print output

    def _read_tree(self):
        file_list = []
        for root, dirs, files in os.walk(self.BASE_PATH):
            for f in files:
                file_list.append(os.path.join(root, f))

        return file_list

    def _read_file_name(self, filename):
        command = ["gpg", "-q", "--list-packets", "--no-use-agent",
                   "--passphrase", self._key, filename]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        there = re.compile(r'name=".*"')
        name = ''.join(there.findall(output))
        return name.split('"')[1]

    def _read_packets(self):
        file_list = self._read_tree()
        real_list = {}
        for f in file_list:
            # here I need to contemplate the base path and the not randomized
            # prefix
            if '/' in f:
                base_name = '/'.join(f.split('/')[:-1])
            else:
                base_name = ''

            real_name = os.path.join(base_name, self._read_file_name(f))
            real_name = real_name.replace(self.BASE_PATH, '')

            real_list[real_name] = f

        self._map = real_list
        print real_list

    def get_node(self, name):
        self._read_packets()
        return self._map[name]

    def list_nodes(self):
        return self._map.keys()


def main2():
    g = SimpleGPG()
    g.test()


def main():
    t = GPGTree()

    data = "This is some test data for the placeholder files"
    t.add_node('secret-note', data)
    t.add_node('ivan/test', data)
    t.add_node('ivan/gmail-account', data)
    t.add_node('unx/bank-passwords', data)
    t.add_node('unx/admin-mail', data)
    t.add_node('unx/ISPConfig', data)

    # from pprint import pprint
    # pprint(t._map)
    # print self._map

    print
    key = 'unx/admin-mail'
    print key, '->', t.get_node(key)
    print t.list_nodes()

if __name__ == '__main__':
    main()

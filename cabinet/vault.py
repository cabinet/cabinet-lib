#!/usr/bin/env python
# encoding: utf-8
import errno
import os

import gnupg

from .gpg_helper import GPGHelper
from .random_tree import RandomTree
from .utils import TreeList


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


class Vault(object):
    """
    Password manager class prototype.
    """

    def __init__(self, private_key_password, root=None):
        """
        Initialize the password vault using the `root` base path to store the
        data and the `private_key_password` to unlock the private key.

        :param private_key_password: password to unlock the secret key
        :type private_key_password: str
        :param root: the path to store/read data
        :type root: str
        """
        if root is None:
            root = os.path.expanduser('~/.config/cabinet/')

        self._root_path = root

        self._base_path = os.path.join(root, 'vault')
        auth_path = os.path.join(self._base_path, '.auth')
        mkdir_p(auth_path)

        self._names_mapping = os.path.join(auth_path, 'mappings.json')
        self._recipients_file = os.path.join(auth_path, 'recipients')

        self._mapper = RandomTree(self._names_mapping)

        gpg_home = os.path.join(root, 'gnupg')
        self._gpg = gnupg.GPG(homedir=gpg_home)
        self._key = private_key_password

    def _get_recipients(self):
        """
        :return: a list of recipients to use to encrypt the data
        :rtype: list
        """
        try:
            with open(self._recipients_file) as f:
                recp = f.read()
        except:
            keylist = self._gpg.list_keys(secret=True)
            print keylist
            raise

        if recp is not None:
            recipients = recp.splitlines()

        return recipients

    def _cipher(self, data, recipients=None):
        """
        Encrypt the given data for the given recipients.

        :param data: the data to encrypt
        :type data: str
        :param recipients: a list of recipients to use to encrypt the data
        :type recipients: list

        :return: the encrypted data data
        :rtype: str
        """
        if recipients is None:
            recipients = self._get_recipients()

        result = self._gpg.encrypt(data, *recipients)

        if not result.ok:
            print "Error:", result.stderr
            # raise Exception

        return result.data

    def _decipher(self, data):
        """
        Decypher the given data using the private key of the current user.

        :param data: the data to decrypt
        :type data: str

        :return: the decrypted data
        :rtype: str
        """
        result = self._gpg.decrypt(data, passphrase=self._key)

        if not result.ok:
            print "Error:", result.stderr

        return result.data

    def init(self):
        """
        Initialize new password storage and use fingerprint for encryption.

        fingerprint -> admin's fp
        """
        # create path structure
        auth_path = os.path.join(self._root_path, 'vault', '.auth')
        gpg_home = os.path.join(self._root_path, 'gnupg')
        mkdir_p(auth_path)
        mkdir_p(gpg_home)

    def create_key(self, user, email, password):
        root = os.path.expanduser('~/.config/cabinet/')
        gpg_home = os.path.join(root, 'gnupg')

        g = GPGHelper(gpg_home)
        fingerprint = g.create_key(user, email, password)
        # g.display_keys()
        # g.get_key()
        return fingerprint

    def get_my_fingerprint(self):
        """
        Return the current user's fingerprint or None if there is no private
        key.

        :rtype: str or None
        """
        root = os.path.expanduser('~/.config/cabinet/')
        gpg_home = os.path.join(root, 'gnupg')
        g = GPGHelper(gpg_home)

        keylist = g.get_keys(secret=True)

        if not keylist:
            return None

        # it CAN be more but it SHOULD be just one private key
        if len(keylist) > 1:
            print keylist
            raise Exception("There is more than one private key.")

        return keylist[0]['fingerprint']

    def get_key(self, fingerprint):
        root = os.path.expanduser('~/.config/cabinet/')
        gpg_home = os.path.join(root, 'gnupg')
        g = GPGHelper(gpg_home)
        return g.get_key(fingerprint)

    def set_admin(self, fingerprint, overwrite=False):
        # create admin's key pair
        if os.path.isfile(self._recipients_file) and not overwrite:
            raise IOError("File already exists")

        with open(self._recipients_file, 'w') as r:
            r.write(fingerprint)

    def get_node_list(self):
        return self._mapper.list_nodes()

    def get_tree(self):
        nodes = self.get_node_list()
        nodes.sort()
        t = TreeList(nodes)
        return t.get_tree()

    def get(self, name):
        """
        Return the data contained in the key 'name'.

        :param name: the name of the data contents that you want to retrieve.
        :type name: str
        """
        random_name = self._mapper.get_node(name)

        path = os.path.join(self._base_path, random_name)
        with open(path, 'r') as f:
            e_data = f.read()

        data = self._decipher(e_data)
        return data

    def add(self, name, data, overwrite=False):
        """
        Add new data. It is stored encrypted.

        :param name: the name of the data contents that you want to retrieve.
        :type name: str
        :param data: the data to store
        :type data: str
        :param overwrite: whether we should overwrite or not the file if it
                          exists.
        :type overwrite: bool
        """
        random_name = self._mapper.add_node(name)

        e_data = self._cipher(data)
        path = os.path.join(self._base_path, random_name)

        if os.path.isfile(path) and not overwrite:
            raise IOError("File already exists")

        folder = os.path.dirname(path)
        mkdir_p(folder)

        with open(path, 'w') as f:
            f.write(e_data)

    def remove(self, name):
        """
        Remove existing password or directory, optionally forcefully.
        """
        pass

    def move(self, old_name, new_name):
        """
        Renames or moves old-path to new-path, optionally forcefully,
        selectively reencrypting.
        """
        pass

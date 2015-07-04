#!/usr/bin/env python
# encoding: utf-8
import errno
import os

from getpass import getpass

import gnupg

from random_tree import RandomTree


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

    def __init__(self, root, private_key_password):
        """
        Initialize the password vault using the `root` base path to store the
        data and the `private_key_password` to unlock the private key.

        :param root: the path to store/read data
        :type root: str
        :param private_key_password: password to unlock the secret key
        :type private_key_password: str
        """
        # TODO: default `root` to ~/.config/cabinet/vault/ ?
        self._base_path = root
        self._names_mapping = os.path.join(root, '.auth', 'mappings.json')
        self._recipients_file = os.path.join(root, '.auth', 'recipients')

        mkdir_p(self._base_path)

        self._mapper = RandomTree(self._names_mapping)

        # TODO: use special dir to keep password manager specific keys?
        # e.g. ~/.config/cabinet/keys/
        gpg_home = os.path.join(os.path.expanduser('~/.gnupg/'))
        self._gpg = gnupg.GPG(homedir=gpg_home)
        self._key = private_key_password

    def _get_recipients(self):
        """
        :return: a list of recipients to use to encrypt the data
        :rtype: list
        """
        with open(self._recipients_file) as f:
            recp = f.read()

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

    def init(self, subpath=None, new_gpg_id=None):
        """
        Initialize new password storage and use gpg-id for encryption.
        Selectively reencrypt existing passwords using new gpg-id.
        """
        pass

    def ls(self):
        """List passwords."""
        from pprint import pprint
        print "Nodes: ",
        pprint(self._mapper.list_nodes())

        print "Tree on disk:"
        import subprocess
        out = subprocess.check_output(['tree', self._base_path])
        print out

    def get_node_list(self):
        return self._mapper.list_nodes()

    def get(self, name):
        """
        Return the data contained in the key 'name'.

        :param name: the name of the data contents that you want to retrieve.
        :type name: str
        """
        random_name = self._mapper.get_node(name)

        path = self._base_path + random_name
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
        path = self._base_path + random_name

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


def main():
    pkey = getpass('Enter the password to unlock your private key: ')
    v = Vault(root='./tmp/password.vault/', private_key_password=pkey)

    v.add('test', "Hellooo worrrrlddd!!", overwrite=True)
    v.add('ivan/gmail', "my super secret password", overwrite=True)
    v.add('ivan/bank-password', "1234", overwrite=True)
    v.add('my-company/alarm', "123456", overwrite=True)
    v.add('my-company/contact-mail',
          "mail: contact@my-company.com - pass: hard to kill",
          overwrite=True)
    # this produces an error, handle it
    # v.add('test/asdf', "some sensitive information", overwrite=True)

    print '>> get("test"):', v.get('test')
    print '>> get("ivan/gmail"):', v.get('ivan/gmail')

    print ">> ls()"
    v.ls()

if __name__ == '__main__':
    main()

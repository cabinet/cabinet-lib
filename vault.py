#!/usr/bin/env python
# encoding: utf-8
import errno
import os

from getpass import getpass

import gnupg

PASSWORD_VAULT = './password.vault/'
GPG_RECIPIENTS = 'gpg-recipients'


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

    def __init__(self):
        mkdir_p(PASSWORD_VAULT)

        gpg_home = os.path.join(os.path.expanduser('~/.gnupg/'))
        self._gpg = gnupg.GPG(homedir=gpg_home)
        self._key = getpass('Enter the password to unlock your private key: ')

    def _get_recipients(self):
        """
        :return: a list of recipients to use to encrypt the data
        :rtype: list
        """
        recp_file = os.path.join(PASSWORD_VAULT, GPG_RECIPIENTS)
        with open(recp_file) as f:
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
        import subprocess
        out = subprocess.check_output(['tree', PASSWORD_VAULT])
        print out

    def get(self, name):
        """
        Return the data contained in the key 'name'.

        :param name: the name of the data contents that you want to retrieve.
        :type name: str
        """
        path = PASSWORD_VAULT + name
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
        e_data = self._cipher(data)
        path = PASSWORD_VAULT + name

        folder = os.path.dirname(path)
        mkdir_p(folder)

        if os.path.isfile(path) and not overwrite:
            raise IOError("File already exists")

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
    m = Vault()

    m.add('test', "Hellooo worrrrlddd!!", overwrite=True)
    m.add('ivan/gmail', "my super secret password", overwrite=True)

    print 'test:', m.get('test')
    print 'ivan/gmail:', m.get('ivan/gmail')

    m.ls()

if __name__ == '__main__':
    main()

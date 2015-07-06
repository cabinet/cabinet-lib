#!/usr/bin/env python
# encoding: utf-8
from getpass import getpass

from cabinet import Vault


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

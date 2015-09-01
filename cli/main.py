#!/usr/bin/env python
# encoding: utf-8
import os
import subprocess

from getpass import getpass
from pprint import pprint

from cabinet import Vault

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Cabinet test CLI app.')
    parser.add_argument('-a', '--add', action='store_true',
                        dest='add', help='add sample nodes')
    parser.add_argument('-g', '--get', action='store_true',
                        dest='get', help='get sample nodes')

    parser.add_argument('-c', '--create', action='store_true',
                        dest='create_key', help='create key pair')

    parser.add_argument('-k', '--get-key', action='store_true',
                        dest='get_key', help='show own key information')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # pkey = getpass('Enter the password to unlock your private key: ')
    pkey = 'asdfasdf'
    v = Vault(private_key_password=pkey)

    print "Init vault..."
    v.init()
    try:
        v.set_admin(v.get_my_fingerprint())
    except:
        pass

    if args.create_key:
        # Create dummy key for tests:
        fp = v.create_key('Test User', 'the_user@test.com', 'asdfasdf')
        print "The new key's fingerprint is {0}".format(fp)
        print '-'*20
        print v.get_key(fp)
        print '-'*20

    if args.get_key:
        fp = v.get_my_fingerprint()
        print "The user's fingerprint is {0}".format(fp)
        print '-'*20
        print v.get_key(fp)
        print '-'*20

    if args.add:
        print "adding nodes..."
        v.add('test', "Hellooo worrrrlddd!!", overwrite=True)
        v.add('ivan/gmail', "my super secret password", overwrite=True)
        v.add('ivan/bank-password', "1234", overwrite=True)
        v.add('my-company/alarm', "123456", overwrite=True)
        v.add('my-company/contact-mail',
              "mail: contact@my-company.com - pass: hard to kill",
              overwrite=True)
        # this produces an error, handle it
        # v.add('test/asdf', "some sensitive information", overwrite=True)

    if args.get:
        print "getting info from nodes..."
        print '>> get("test"):', v.get('test')
        print '>> get("ivan/gmail"):', v.get('ivan/gmail')

        print "Nodes: ",
        pprint(v.get_node_list())

        print "Tree on disk:"
        out = subprocess.check_output(
            ['tree', '-C', os.path.expanduser('~/.config/cabinet')])
        print out


if __name__ == '__main__':
    main()

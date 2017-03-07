#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import socket

from flask import Flask, session

from cabinet import Cabinet
from flask_jsonrpc import JSONRPC
from rpc import authenticate, token_urlsafe

app = Flask(__name__)


jsonrpc = JSONRPC(app, '/api/v1')

config_path = os.path.join(os.getcwd(), 'test.data', 'secrets')
vault_path = os.path.join(os.getcwd(), 'test.data', 'vaults')

# GLOBAL config object
vault_config = {
    'config_path': config_path,
    'vault_path': vault_path,
    'vault_name': None,
    'account_id': None,
    'password': None,
    'app_token': None,
    'app_port': None,
    'cabinet': None,
}


def check_auth(client_token):
    global vault_config
    token = vault_config.get('app_token')
    if token is None:
        # when we set the token to None we meant to say that no token is
        # required to do requests
        return True

    return client_token == token


@jsonrpc.method('App.open_vault(username=str, password=str,'
                'vault_name=str, vault_path=str) -> str')
@authenticate(check_auth)
def open_vault(username, password, vault_name, vault_path=None):
    # TODO: Implement username/password/vault validation and opening

    global vault_config
    config_path = vault_config.get('config_path')
    if vault_path is None:
        vault_path = vault_config.get('vault_path')

    cab = Cabinet(username, password, config_path)
    cab.open(vault_name, vault_path)
    vault_config['cabinet'] = cab

    session['username'] = username
    session['password'] = password
    session['vault_path'] = vault_path
    return {'success': True}  # TODO: don't hardcode this


@jsonrpc.method('App.get_all')
def get_all():
    global vault_config
    cab = vault_config.get('cabinet')
    return cab.get_all()


@jsonrpc.method('App.get(name=str)')
def get(name):
    global vault_config
    cab = vault_config.get('cabinet')
    return cab.get(name)


@jsonrpc.method('App.add(item=dict)')
def add(item):
    global vault_config
    cab = vault_config.get('cabinet')
    return cab.add(item)


@jsonrpc.method('Cabinet.test', authenticated=check_auth)
def index():
    return u'hello world!'


@jsonrpc.method('App.echo(name=str) -> str', validate=True)
@authenticate(check_auth)
def echo(name='Flask JSON-RPC'):
    return u'Hello {0}'.format(name)


def get_random_open_port():
    """
    Return a random available port.

    :rtype: int
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def run_rpc_server(port, no_token):
    global vault_config

    if port is not None:
        app_port = port
    else:
        app_port = get_random_open_port()
    vault_config['app_port'] = app_port

    # The server will respond only to requests with this token
    # If token is set to None, the server will respond to any request
    app_token = None
    if not no_token:
        app_token = token_urlsafe(32)
    vault_config['app_token'] = app_token

    # Print token/port for the calling process to be able to comunicate
    print(app_token, file=sys.stdout, flush=True)
    print(app_port, file=sys.stdout, flush=True)

    # Redirect stdout and stderror to log files
    sys.stdout = open('rpc-server.out', 'w')
    sys.stderr = open('rpc-server.err', 'w')

    app.secret_key = token_urlsafe(32)

    # WARNING: Debug mode will re-execute the token and port generation.
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(port=port, debug=True)  # only localhost, default port
    app.run(port=app_port)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Argparse test program')
    parser.add_argument('-p', '--port', type=int,
                        help='Use this port instead of a random one')
    parser.add_argument('-n', '--no-token', action='store_true',
                        help='Do not require token for requests')
    args = parser.parse_args()

    run_rpc_server(args.port, args.no_token)

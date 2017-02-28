#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pprint
import requests

from subprocess import Popen, PIPE
from time import sleep


class RPCClient:
    def __init__(self):
        self._headers = {'content-type': 'application/json'}
        self._server_started = False

    def start_server(self):
        """Start server and use it for API calls."""
        self._server = Popen(['python', 'rpc-server.py'], stdout=PIPE)
        out = self._server.stdout
        token = out.readline().decode('ascii').strip()
        port = out.readline().decode('ascii').strip()

        self._url = "http://localhost:{port}/api/v1".format(port=port)
        self._headers['token'] = token

        # Wait until the server starts
        sleep(2)

        print('Server started')
        print("Token: {token}".format(token=token))
        print("Port: {port}".format(port=port))
        self._server_started = True

    def set_server(self, port, token):
        """Use this to use an already running server."""
        self._url = "http://localhost:{port}/api/v1".format(port=port)
        self._headers['token'] = token

    def stop_server(self):
        if not self._server_started:
            print("Error, server not started.")
            return

        self._server.terminate()
        self._server_started = False
        print("Server stopped")

    def _rpc_call(self, method_name, **kwargs):
        if not self._server_started:
            print("Error, server not started.")
            return

        payload = {
            "method": method_name,
            "params": kwargs,
            "jsonrpc": "2.0",
            'id': 0,
        }

        res = requests.post(
            self._url,
            data=json.dumps(payload),
            headers=self._headers)
        response = res.json()

        return response

    def open_vault(self, username, password, vault_name):
        response = self._rpc_call(
            "App.open_vault",
            username=username,
            password=password,
            vault_name=vault_name)

        return response

    def open_vault_invalid(self, username='User 1', password='Some secret',
                           vault_name='my-vault'):
        valid_headers = self._headers

        # wrong headers
        self._headers = {
            'content-type': 'application/json',
            'token': 'WRONG TOKEN'
        }

        response = self._rpc_call(
            "App.open_vault",
            username=username,
            password=password,
            vault_name=vault_name)

        # restore valid headers
        self._headers = valid_headers
        return response

    def get_all(self):
        response = self._rpc_call("App.get_all")
        return response

    def get(self, name):
        response = self._rpc_call("App.get", name=name)
        return response


def show_response(msg, r):
    print('-' * 20)
    print(msg)
    pprint.pprint(r)
    print()


def main():
    client = RPCClient()
    client.start_server()

    # Vault data, same as on test-app.py
    account_id = 'my-name@my-company.com'
    password = 'asdfasdf'
    vault_name = 'test-vault'

    # Open a vault
    r = client.open_vault(account_id, password, vault_name)
    show_response("Open vault with correct token", r)

    # Open a vault, but with a false token
    r = client.open_vault_invalid(account_id, password, vault_name)
    show_response("Open vault with wrong token", r)

    # Note: use `test-app.py` to add some random data
    items = client.get_all()
    show_response("Get all the items", items)

    r = client.get(name='test-item #42')
    show_response("Get one item", r)

    client.stop_server()


if __name__ == "__main__":
    main()

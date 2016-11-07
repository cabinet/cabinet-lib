#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import pprint

from subprocess import Popen, PIPE
from time import sleep

url = "http://localhost:5000/api/v1"
headers = {'content-type': 'application/json'}


def setUrlPort(port=5000):
    global url
    url = "http://localhost:{port}/api/v1".format(port=port)


def setHeaderToken(token=None):
    global headers
    headers['token'] = token


def rpc_call(method_name, **kwargs):
    payload = {
        "method": method_name,
        "params": kwargs,
        "jsonrpc": "2.0",
        'id': 0,
    }

    res = requests.post(url, data=json.dumps(payload), headers=headers)
    response = res.json()

    return response


def get_all():
    payload = {
        "method": "App.get_all",
        "params": None,
        "jsonrpc": "2.0",
        'id': 0,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response
    # assert response["result"] == "hello world!"
    # assert response["jsonrpc"]
    # assert response["id"] == 0


def get(name='test-item #1'):
    payload = {
        "method": "App.get",
        "params": {'name': name},
        "jsonrpc": "2.0",
        'id': 0,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response


def open_vault(username, password, vault_name):
    payload = {
        "method": "App.open_vault",
        "params": {
            'username': username,
            'password': password,
            'vault_name': vault_name
        },
        "jsonrpc": "2.0",
        'id': 0,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response


def fake_open_vault(username='User 1', password='Some secret',
                    vault_name='my-vault'):
    payload = {
        "method": "App.open_vault",
        "params": {
            'username': username,
            'password': password,
            'vault_name': vault_name
        },
        "jsonrpc": "2.0",
        'id': 0,
    }

    fake_headers = {
        'content-type': 'application/json',
        'token': 'WRONG TOKEN'
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=fake_headers).json()

    return response


def getTokenAndPort():
    p = Popen(['python', 'rpc-server.py'], stdout=PIPE)
    token = p.stdout.readline().decode('ascii').strip()
    port = p.stdout.readline().decode('ascii').strip()
    return token, port


def show_response(msg, r):
    print('-' * 20)
    print(msg)
    pprint.pprint(r)
    print()


def main():

    token, port = getTokenAndPort()

    print("Token: {token}".format(token=token))
    print("Port: {port}".format(port=port))

    setHeaderToken(token)
    setUrlPort(port)

    # Just wait for a delay until the server opens the port
    sleep(2)

    # Vault data, same as on test-app.py
    account_id = 'my-name@my-company.com'
    password = 'asdfasdf'
    vault_name = 'test-vault'

    # Open a vault
    r = open_vault(account_id, password, vault_name)
    show_response("Open vault with correct token", r)

    # Open a vault, but with a false token
    r = fake_open_vault(account_id, password, vault_name)
    show_response("Open vault with wrong token", r)

    # Note: use `test-app.py` to add some random data
    items = rpc_call("App.get_all")
    show_response("Get all the items", items)

    r = rpc_call('App.get', name='test-item #42')
    show_response("Get one item", r)


if __name__ == "__main__":
    main()

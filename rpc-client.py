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


def open_vault(username='User 1', password='Some secret',
               vault_path='/some/path'):
    payload = {
        "method": "App.open_vault",
        "params": {
            'username': username,
            'password': password,
            'vault_path': vault_path
        },
        "jsonrpc": "2.0",
        'id': 0,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response


def getTokenAndPort():
    p = Popen(['python', 'rpc-server.py'], stdout=PIPE)
    token = p.stdout.readline().decode('ascii').strip()
    port = p.stdout.readline().decode('ascii').strip()
    return token, port


def main():

    token, port = getTokenAndPort()

    print("Token: {token}".format(token=token))
    print("Port: {port}".format(port=port))

    setHeaderToken(token)
    setUrlPort(port)

    # Just wait for a delay until the server opens the port
    sleep(2)

    # Open a vault
    r = open_vault(username='Facundo',
                   password='some pass',
                   vault_path='/somepath')
    pprint.pprint(r)

    # Note: use `test-app.py` to add some random data
    items = rpc_call("App.get_all")
    pprint.pprint(items)

    pprint.pprint(rpc_call('App.get', name='test-item #42'))

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

from subprocess import Popen, PIPE

url = "http://localhost:5000/api/v1"
headers = {'content-type': 'application/json'}


def setUrlPort(port=5000):
    global url
    url = "http://localhost:{port}/api/v1".format(port=port)


def setHeaderToken(token=None):
    global headers
    headers['token'] = token


def rpc_call(method_name, **kwargs):
    url = "http://localhost:5000/api/v1"
    headers = {'content-type': 'application/json'}

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


def getTokenAndPort():
    p = Popen(['python', 'rpc-server.py'], stdout=PIPE)
    token = p.stdout.readline().decode('ascii').strip()
    port = p.stdout.readline().decode('ascii').strip()
    return token, port


def main():

    token, port = getTokenAndPort()

    print(token)
    print(port)

    setHeaderToken(token)
    setUrlPort(port)

    # Note: use `test-app.py` to add some random data
    # items = rpc_call("App.get_all")
    # import pprint
    # pprint.pprint(items)
    #
    # pprint.pprint(rpc_call('App.get', name='test-item #42'))

if __name__ == "__main__":
    main()

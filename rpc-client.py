#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

url = "http://localhost:5000/api/v1"
headers = {'content-type': 'application/json'}


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


def main():
    # uncomment to insert some test data
    # content = {
    #     'username': 'testuser - rpc',
    #     'password': 'asdfasdf',
    #     'site-url': 'https://example.com/rpc',
    #     'notes': 'added using rpc',
    # }
    # item = {
    #     'name': 'test-item #3',
    #     'tags': ['rpc', 'remote', 'test'],
    #     'content': content,
    # }
    # rpc_call('App.add', item=item)

    # items = get_all()
    items = rpc_call("App.get_all")
    import pprint
    pprint.pprint(items)

    pprint.pprint(rpc_call('App.get', name='test-item #2'))

if __name__ == "__main__":
    main()

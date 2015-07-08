#!/usr/bin/env python
# encoding: utf-8

import requests

NODES = [
    "ivan/gmail",
    "sample-item",
    "my-company/alarm-code",
    "test/yahoo-mail",
    "test/family-safe-code",
    "my-company/admin-mail"
]

BASE = 'http://localhost:8000/vault/nodes'

new_node = '/ivan_asdf'

r = requests.get(BASE)
# print r.text
assert r.json() == NODES

r = requests.get(BASE + new_node)
assert r.status_code == 404

payload = {'name': 'ivan/asdf', 'data': 'hello world!'}
r = requests.post(BASE, params=payload)
node = r.json()
# print node
assert node == payload

# r = requests.get(BASE)
# print r.text

r = requests.get(BASE + new_node)
assert r.json() == 'hello world!'

r = requests.delete(BASE + new_node)
# print r.json()

# r = requests.get(BASE)
# print r.text

r = requests.get(BASE + new_node)
assert r.status_code == 404

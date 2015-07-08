#!/usr/bin/env python
# encoding: utf-8

from flask import Flask  # , request < why not to use this?
from flask_restful import Api, Resource, reqparse  # , abort

# this is needed to run the api server on the same host as the web page
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('data', type=str)

VAULT = {
    'ivan/gmail': ('account: ivan@gmail.com\n'
                   'password: my super secret password'),
    'sample-item': 'hello there',
    'test/yahoo-mail': 'email credentials here',
    'test/family-safe-code': '0000-1234',
    'my-company/alarm-code': '123456',
    'my-company/admin-mail': ('account: admin@my-company.com\n'
                              'password: qwertyuiop'),
}


class Node(Resource):
    """
    Resource to show (get), delete (delete) and edit/update (put) a single
    vault node.
    """

    def get(self, node_id):
        """ Get a specific node from the vault. """
        node_id = node_id.replace('_', '/')
        node = VAULT.get(node_id)

        if node is not None:
            return node

        return "", 404

    def delete(self, node_id):
        """ Remove a new node from the vault. """
        node_id = node_id.replace('_', '/')

        if VAULT.get(node_id) is not None:
            del VAULT[node_id]

    def put(self, node_id):
        """ Edit/update an existing node in the vault. """
        node_id = node_id.replace('_', '/')

        args = parser.parse_args()

        if not args.get('data'):
            # abort(301, message="Missing data")
            return "Missing data", 301

        VAULT[node_id] = args.get('data')

        return VAULT[node_id], 201


class Nodes(Resource):
    """ Resource to list (get) and add (post) nodes into the vault. """

    def get(self):
        """
        Get the list of nodes in the vault.
        """
        return VAULT.keys()

    def post(self):
        """
        Add a new node to the vault.
        """
        args = parser.parse_args()
        name = args['name']
        data = args['data']

        if not name or not data:
            # abort(301, message="Missing data")
            return "Missing data", 301

        VAULT[name] = data

        return {'name': name, 'data': VAULT[name]}, 201


api.add_resource(Nodes, '/vault/nodes')
api.add_resource(Node, '/vault/nodes/<node_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=True)

#!/usr/bin/env python
# encoding: utf-8

from getpass import getpass

from flask import Flask  # , request < why not to use this?
from flask_restful import Api, Resource, reqparse  # , abort

# this is needed to run the api server on the same host as the web page
from flask_cors import CORS

from cabinet import Vault


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('data', type=str)


# (module level) global instance to access from Node and Nodes
_pkey = getpass('Enter the password to unlock your private key: ')
_vault = Vault(private_key_password=_pkey)


class Node(Resource):
    """
    Resource to show (get), delete (delete) and edit/update (put) a single
    vault node.
    """

    def get(self, node_id):
        """ Get a specific node from the vault. """
        # we can't use '/' when we request for some node, how could we escape
        # it? right now we rely on curl-ing with '_' when we mean '/'
        node_id = node_id.replace('_', '/')
        data = _vault.get(node_id)
        return {'name': node_id, 'data': data}
        # return {'name': 'my-email-account', 'data': 'my secret password'}

    def delete(self, node_id):
        """ Remove a new node from the vault. """
        # _vault.remove(node_id)
        pass

    def put(self, node_id):
        """ Edit/update an existing node in the vault. """
        # curl http://localhost:8000/test/123 -d "data=my secret data" -X PUT
        args = parser.parse_args()

        if not args.get('data'):
            # abort(301, message="Missing data")
            return "Missing data", 301

        # TODO: fail on non-existing node

        _vault.add(node_id, args['data'], overwrite=True)
        node = {'name': node_id, 'data': _vault.get(node_id)}

        return node, 201


class Nodes(Resource):
    """ Resource to list (get) and add (post) nodes into the vault. """

    def get(self):
        """
        Get the list of nodes in the vault.
        """
        return _vault.get_tree()

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

        node = {'name': name, 'data': data}
        _vault.add(name, data)

        return node, 201


api.add_resource(Nodes, '/vault/nodes')
api.add_resource(Node, '/vault/nodes/<node_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=True)

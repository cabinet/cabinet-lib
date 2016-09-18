# -*- coding: utf-8 -*-
# Flask jsonrpc forces to always send the username and the password on every
# request that need authentication. This is unnecessary if the check_auth
# method is properly implemented.
from inspect import getargspec
from flask_jsonrpc import JSONRPC, _parse_sig


class FixedJSONRPC(JSONRPC):
    def method(self, name, authenticated=False, safe=False, validate=False,
               **options):
        def decorator(f):
            """This decorator doesn't have assumptions about the arguments."""

            arg_names = getargspec(f)[0]
            X = {'name': name, 'arg_names': arg_names}
            if authenticated:
                _f = self.auth_backend(f, authenticated)
            else:
                _f = f
            method, arg_types, return_type = _parse_sig(X['name'],
                                                        X['arg_names'],
                                                        validate)
            _f.json_args = X['arg_names']
            _f.json_arg_types = arg_types
            _f.json_return_type = return_type
            _f.json_method = method
            _f.json_safe = safe
            _f.json_sig = X['name']
            _f.json_validate = validate
            self.site.register(method, _f)
            return _f
        return decorator

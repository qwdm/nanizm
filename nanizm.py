#!/usr/bin/env python3.6
"""
Skeleton of wsgi lightweight framework, only for example of router

Router:
simple tree-like router (tree is represented as nested dict)
with special termination symbol <TARGET_SYMBOL>

App:
router + get requests + json responses
"""

import json

TARGET_SYMBOL = '__never_use_such_url__'


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, target):
        """ :param target: callable returning json-serializable data """
        elements = path.split('/')
        route = self.routes
        for element in elements:
            if element.startswith('<'): # and endswith('>')
                # just a wildcard
                element = '<>'
            if element in route:
                route = route[element]
            else:
                route[element] = {}
                route = route[element]

        route[TARGET_SYMBOL] = target

    def get_target(self, path):

        wildcards = []
        route = self.routes
        elements = path.split('/')
        for element in elements:
            if element in route:
                route = route[element]
            elif '<>' in route:
                route = route['<>']
                wildcards.append(element)
            else:
                return None, None

        target = route[TARGET_SYMBOL]

        return target, wildcards



class App:
    def __init__(self):
        self.router = Router()

    def __call__(self, environ, start_response):
        """ heart of wsgi interface """

        response_headers = [
                ('Content-type', 'application/json'),
                ('Content-Encoding', 'utf-8'),
        ]

        path = environ.get('PATH_INFO')
        target, wildcards = self.router.get_target(path)

        if target is None:
            status = '404 Not Found'
            response_data = {}
        else:
            status = '200 OK'
            response_data = target(*wildcards)

        start_response(status, response_headers)

        if response_data:
            return [json.dumps(response_data).encode('UTF-8')]
        else:
            return []

    def route(self, path):
        """ app.route decorator for register paths """
        def register(target):

            self.router.add_route(path, target)

            return target

        return register

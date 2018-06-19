#!/usr/bin/env python3.6

import json

TARGET_SYMBOL = '!***T_A_R_G_E_T*%^&!@()'

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
#            route = route.get(element)
#            print()
#            print(element, route)
            elif '<>' in route:
                route = route['<>']
                wildcards.append(element)
            else:
                return None

        target = route[TARGET_SYMBOL]

        return target, wildcards





class App:
    def __init__(self):
        self.router = Router()

    def __call__(self, environ, start_response):

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
#            args = get_wildcards(path)
            response_data = target(*wildcards)

        start_response(status, response_headers)

        if response_data:
            return [json.dumps(response_data).encode('UTF-8')]
        else:
            return []

    def route(self, path):
        def register(target):

            self.router.add_route(path, target)

            return target

        return register

        self.router



#def get_wildcards(path):
    

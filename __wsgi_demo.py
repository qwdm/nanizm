#!/usr/bin/env python3.6

import json

def wsgi_app(environ, start_response):

    status = '200 OK'
    resp_headers = [
            ('Content-type', 'application/json'),
            ('Content-Encoding', 'utf-8'),
            ('X-Bullshit', 'nodata'),
    ]
    start_response(status, resp_headers)

    environ_json = {}
    json_types = (
            bool,
            list,
            dict,
            str,
            type(None),
    )
    for k, v in environ.items():
        if isinstance(v, json_types):
            environ_json[k] = v
        else:
            environ_json[k] = repr(v)

    response_data = {
            'Status': 'OK',
            'Environ': environ_json,
    }

    return [json.dumps(response_data).encode('UTF-8')]

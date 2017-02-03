from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

class HTTPRequestHandler(BaseHTTPRequestHandler):
    """Handler that will be call by the DaemonServer to routes requests"""

    routes = {'GET': {}, 'POST': {}, 'DELETE': {}}

    @staticmethod
    def get(route):
        def mapping(func):
            HTTPRequestHandler.routes['GET'][route] = func
            return func
        return mapping

    @staticmethod
    def post(route):
        def mapping(func):
            HTTPRequestHandler.routes['POST'][route] = func
            return func
        return mapping

    @staticmethod
    def delete(route):
        def mapping(func):
            HTTPRequestHandler.routes['DELETE'][route] = func
            return func
        return mapping

    def __match(self, request_method):
        func = self.routes[request_method].get(self.path)
        if func is not None:
            response = func(self)
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.text.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        self.__match('GET')

    def do_POST(self):
        content_length = int(self.headers.get('content-length'))
        data = self.rfile.read(content_length).decode('utf-8')
        self.fields = parse_qs(data)
        self.__match('POST')
from http.server import BaseHTTPRequestHandler

class HTTPRequestHandler(BaseHTTPRequestHandler):

    routes = {'GET': {}, 'POST': {}}

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

    def do_GET(self):
        func = self.routes['GET'].get(self.path)
        if func is not None:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(func().encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        func = self.routes['POST'].get(self.path)
        if func is not None:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(func().encode())
        else:
            self.send_response(404)
            self.end_headers()


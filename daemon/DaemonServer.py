from http.server import HTTPServer
from HTTPRequestHandler import HTTPRequestHandler

@HTTPRequestHandler.get('/')
def index():
    return 'Get the home page bitch'

httpd = HTTPServer(('127.0.0.1', 8000), HTTPRequestHandler)
httpd.serve_forever()

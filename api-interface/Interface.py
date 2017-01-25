from flask import Flask

from endpoints import authentication

class InterfaceServer(object):

    def __init__(self, **kwargs):
        self.app = Flask(__name__)
        authentication.register_routes(self.app)

    def start(self):
        self.app.run(debug=True)

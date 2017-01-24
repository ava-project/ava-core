from flask import Flask

class InterfaceServer(object):

    def __init__(self, **kwargs):
        self.app = Flask(__name__)

        @self.app.route("/")
        def hello():
            return "Hello World!"

    def start(self):
        self.app.run()

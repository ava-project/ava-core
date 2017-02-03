from http.server import HTTPServer
from HTTPRequestHandler import HTTPRequestHandler
import requests

class DaemonServer():
    """Contains all the routes for the CLI"""

    _user = {}
    _is_log = False

    def __init__(self, base_url):
        self._is_running = False
        DaemonServer._base_url = base_url

    @staticmethod
    @HTTPRequestHandler.get('/')
    def index():
        return 'Get the home page my dear'

    @staticmethod
    @HTTPRequestHandler.post('/login')
    def post_user_login(request):
        data = {'email': request.fields['email'], 'password': request.fields['password']}
        r = requests.post(DaemonServer._base_url + '/user/login.json', data=data)
        if r.ok:
            DaemonServer._is_log = True
            DaemonServer._user['_token'] = r.json()['data']
            DaemonServer._user['_email'] = request.fields['email'][0]
        return r

    @staticmethod
    @HTTPRequestHandler.get('/logout')
    def get_user_logout(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/logout.json', auth=auth)
        if r.ok:
            DaemonServer._is_log = False
            DaemonServer._token = None
        return r

    @staticmethod
    @HTTPRequestHandler.get('/me')
    def get_user_me(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return r

    def run(self, adress='127.0.0.1', port=8001):
        httpd = HTTPServer((adress, port), HTTPRequestHandler)
        self._is_running = True
        httpd.serve_forever()

if __name__ == '__main__':
    d = DaemonServer("http://127.0.0.1:8000")
    d.run()

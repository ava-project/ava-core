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
        DaemonServer._mock_url = "127.0.0.1:3000"

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

    # todo
    @staticmethod
    @HTTPRequestHandler.get('/plugins')
    def get_plugins(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._mock_url + '/plugins', auth=auth)
        return r

    # todo
    @staticmethod
    @HTTPRequestHandler.get('/plugins/:id')
    def get_plugin(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return r

    # todo
    @staticmethod
    @HTTPRequestHandler.get('/plugins/:id/install')
    def get_install_plugin(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return r

    # todo
    @staticmethod
    @HTTPRequestHandler.delete('/plugins/:id/install')
    def delete_uninstall_plugin(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return r

    # todo
    @staticmethod
    @HTTPRequestHandler.get('/plugins/:id/enable')
    def get_enable_plugin(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return r

    # todo
    @staticmethod
    @HTTPRequestHandler.get('/plugins/:id/disable')
    def get_disable_plugin(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        r = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return r

    def run(self, adress='127.0.0.1', port=8001):
        httpd = HTTPServer((adress, port), HTTPRequestHandler)
        self._is_running = True
        httpd.serve_forever()

if __name__ == '__main__':
    d = DaemonServer("http://163.5.84.224:80")
    d.run()

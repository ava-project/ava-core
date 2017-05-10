from threading import Thread
from http.server import HTTPServer
from server.HTTPRequestHandler import HTTPRequestHandler
import requests

class DaemonServer():
    """Contains all the routes for the CLI"""

    _user = {}
    _is_log = False

    def __init__(self, daemon, base_url):
        self._is_running = False
        self._httpd = None
        self._th = None
        DaemonServer._daemon = daemon
        DaemonServer._base_url = base_url
        DaemonServer._mock_url = "http://127.0.0.1:3000"

    @staticmethod
    @HTTPRequestHandler.get('/')
    def index(request):
        return requests.get(DaemonServer._mock_url + '/')

    @staticmethod
    @HTTPRequestHandler.post('/login')
    def post_user_login(request):
        data = {'email': request.fields['email'], 'password': request.fields['password']}
        res = requests.post(DaemonServer._base_url + '/user/login.json', data=data)
        if res.ok:
            DaemonServer._is_log = True
            DaemonServer._user['_token'] = res.json()['data']
            DaemonServer._user['_email'] = request.fields['email'][0]
        return res

    @staticmethod
    @HTTPRequestHandler.get('/logout')
    def get_user_logout(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + '/user/logout.json', auth=auth)
        if res.ok:
            DaemonServer._is_log = False
            DaemonServer._token = None
        return res

    @staticmethod
    @HTTPRequestHandler.get('/me')
    def get_user_me(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return res

    # mock
    @staticmethod
    @HTTPRequestHandler.get('/plugins/')
    def get_plugins(request):
        res = requests.get(DaemonServer._mock_url + '/plugins')
        return res

    # mock
    @staticmethod
    @HTTPRequestHandler.get('/plugins/:id')
    def get_plugin(request):
        res = requests.get(DaemonServer._mock_url + '/plugins/' + request.url_vars['id'])
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:author/:plugin_name/download')
    def get_download_plugin(request):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + '/plugins/' + request.url_vars['author'] + '/' + request.url_vars['plugin_name'] + '/download', auth=auth)
        if res.ok:
            download_url = res.json()['url']
            download_folder = DaemonServer._daemon._config.get('plugin_folder_download') + '/'
            DaemonServer.__download_file(download_folder + request.url_vars['plugin_name'], download_url, extension='.zip')
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:plugin_name/install')
    def get_install_plugin(request):
        plugin_path = '../plugins_manager/demo/' + request.url_vars['plugin_name'] + '.zip'
        DaemonServer._daemon.install_plugin(plugin_path)
        res = requests.Response()
        res.status_code = 200
        return res

    @staticmethod
    @HTTPRequestHandler.delete('/plugins/:plugin_name')
    def delete_uninstall_plugin(request):
        plugin_name = request.url_vars['plugin_name']
        DaemonServer._daemon.uninstall_plugin(plugin_name)
        res = requests.Response()
        res.status_code = 200
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:plugin_name/enable')
    def get_enable_plugin(request):
        plugin_name = request.url_vars['plugin_name']
        DaemonServer._daemon.enable_plugin(plugin_name)
        res = requests.Response()
        res.status_code = 200
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:plugin_name/disable')
    def get_disable_plugin(request):
        plugin_name = request.url_vars['plugin_name']
        DaemonServer._daemon.disable_plugin(plugin_name)
        res = requests.Response()
        res.status_code = 200
        return res

    @staticmethod
    def __download_file(path, url, extension=''):
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + url, auth=auth, stream=True)
        with open(path + extension, 'wb') as dfile:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    dfile.write(chunk)

    def run(self, adress='127.0.0.1', port=8001):
        self._httpd = HTTPServer((adress, port), HTTPRequestHandler)
        self._is_running = True
        self._th = Thread(None, self._httpd.serve_forever)
        self._th.start()
        print('DaemonServer is listening on %s:%d' % (adress, port))

    def stop(self):
        print('Stopping the DaemonServer...')
        self._httpd.shutdown()
        self._th.join()
        self._is_running = False

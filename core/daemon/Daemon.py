import sys
from threading import Thread, Condition
from collections import deque
from subprocess import Popen, PIPE
from server.DaemonServer import DaemonServer
from plugins_manager.plugins_manager import plugins_manager
from daemon.ConfigLoader import ConfigLoader

class Daemon:
    def __init__(self):
        self._event_queue = deque([])
        self._th = Thread(None, self.__run)
        self._cv = Condition()
        self._is_running = False
        self._config = ConfigLoader("../")
        self._config.load('settings.json')
        self._ds = DaemonServer(self, self._config.get('API_address'))
        self._plugin_manager = plugins_manager(self._config.get('plugin_folder_install'))

    def __run(self):
        while self._is_running:
            while len(self._event_queue) != 0:
                self.__exec()
            else:
                self._cv.acquire()
                self._cv.wait()

    def __exec(self):
        event = self._event_queue.popleft()
        process = Popen(event.get_cmd(), shell=True, stdout=PIPE)
        process.wait()
        out, err = process.communicate()
        if err is not None:
            print(err.decode(sys.stdout.encoding))
        print(out.decode(sys.stdout.encoding))

    def run(self):
        self._is_running = True
        self._th.start()
        self._ds.run()

    def stop(self):
        self._is_running = False
        self._cv.acquire()
        self._cv.notify()
        self._cv.release()
        self._ds.stop()

    def add_event(self, event):
        self._cv.acquire()
        self._event_queue.append(event)
        self._cv.notify()
        self._cv.release()

    def install_plugin(self, file_path):
        self._plugin_manager.install(file_path)

    def uninstall_plugin(self, plugin_name):
        self._plugin_manager.uninstall(plugin_name)

    def enable_plugin(self, plugin_name):
        self._plugin_manager.enable(plugin_name)

    def disable_plugin(self, plugin_name):
        self._plugin_manager.disable(plugin_name)

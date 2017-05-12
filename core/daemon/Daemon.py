import sys
from threading import Thread, Condition
from collections import deque
from subprocess import Popen, PIPE
from server.DaemonServer import DaemonServer
from plugins_manager.plugins_manager import plugins_manager
from daemon.ConfigLoader import ConfigLoader

class Daemon:
    """
    The Daemon class is the main class from AVA.
    It contains the vocal interpretor, the plugin manager and the http server.
    """
    def __init__(self):
        """
        Initializer

            no param
        """
        self._event_queue = deque([])
        self._th = Thread(None, self.__run)
        self._cv = Condition()
        self._is_running = False
        self._config = ConfigLoader(sys.path[1])
        self._config.load('settings.json')
        self._ds = DaemonServer(self, self._config.get('API_address'))
        self._plugin_manager = plugins_manager(self._config.get('plugin_folder_install'))

    def __run(self):
        """
        Private method
        This method wait until it have an event to process
        """
        while self._is_running:
            while len(self._event_queue) != 0:
                self.__exec()
            else:
                self._cv.acquire()
                self._cv.wait()

    def __exec(self):
        """
        Private method
        This method execute an event and remove it from the event queue
        """
        event = self._event_queue.popleft()
        process = Popen(event.get_cmd(), shell=True, stdout=PIPE)
        process.wait()
        out, err = process.communicate()
        if err is not None:
            print(err.decode(sys.stdout.encoding))
        print(out.decode(sys.stdout.encoding))

    def run(self):
        """
        Launch the daemon (ready to process event) and the http server
        """
        self._is_running = True
        self._th.start()
        self._ds.run()

    def stop(self):
        """
        Stop the daemon and the http server
        """
        self._is_running = False
        self._cv.acquire()
        self._cv.notify()
        self._cv.release()
        self._ds.stop()

    def add_event(self, event):
        """
        Add an event to the event queue

            @param event: the event to add to the queue
            @type event: Event
        """
        self._cv.acquire()
        self._event_queue.append(event)
        self._cv.notify()
        self._cv.release()

    def install_plugin(self, file_path):
        """
        Install a plugin (using the plugin manager)

            @param file_path: path to the plugin (.zip)
            @type file_path: string
            @exception: OSError if the file can't be open
        """
        self._plugin_manager.install(file_path)

    def uninstall_plugin(self, plugin_name):
        """
        Uninstall a plugin (using the plugin manager)

            @param plugin_name: the plugin name
            @type plugin_name: string
        """
        self._plugin_manager.uninstall(plugin_name)

    def enable_plugin(self, plugin_name):
        """
        Enable a plugin (using the plugin manager)

            @param plugin_name: the plugin name
            @type plugin_name: string
            @return: if the operation success
            @rtype: bool
        """
        return self._plugin_manager.enable(plugin_name)

    def disable_plugin(self, plugin_name):
        """
        Disable a plugin (using the plugin manager)

            @param plugin_name: the plugin name
            @type plugin_name: string
            @return: if the operation success
            @rtype: bool
        """
        return self._plugin_manager.disable(plugin_name)

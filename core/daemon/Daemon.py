import sys
from threading import Thread
from queue import Queue
from subprocess import Popen, PIPE
from core.vocal_interpretor.interpretor import Interpretor
from core.server.DaemonServer import DaemonServer
from core.plugins_manager.sources.plugins_manager import PluginsManager
from core.daemon.ConfigLoader import ConfigLoader
from core.daemon.FileCrawler import FileCrawler
from core.daemon.Builtin import Builtin


class Daemon(object):
    """
    The Daemon class is the main class from AVA.
    It contains the vocal interpretor, the plugin manager and the http server.
    """
    def __new__(cls, *args, **kwargs):
        """
        Contructor - Singleton
        """
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst

    def __init__(self):
        super(Daemon, self).__init__()
        """
        Initializer

            no param
        """
        self._is_running = False
        self._event_queue = Queue()
        self._th = Thread(None, self.__run)
        self._config = ConfigLoader(sys.path[0])
        self._config.load('settings.json')
        self._interpretor = Interpretor(self)
        self._ds = DaemonServer(self, self._config.get('API_address'))
        self._file_crawler = FileCrawler(self._config.get('FileCrawler_preferences'))
        self._plugin_manager = PluginsManager(self._config.resolve_path_from_root(self._config.get('plugin_folder_install')))
        self._builtin = Builtin(self)

    def __run(self):
        """
        Private method
        This method wait until it have an event to process
        """
        while self._is_running:
            event = self._event_queue.get(block=True)
            if event is None:
                break
            self.__exec(event)
            self._event_queue.task_done()

    def __exec(self, event):
        """
        Private method
        This method execute an event and remove it from the event queue
        """

        target = event.get_cmd().split(' ')
        try:
            if self._builtin.exec_builtin(target) is False:
                if len(target) >= 2:
                    plugin_manager_result = self._plugin_manager.run(target[0], str(' '.join(target[1:])))
                    if plugin_manager_result[0] is False:
                        print(plugin_manager_result[1])
                else:
                    target = self._file_crawler.locateExecutablePath(event.get_cmd())
                    if target is not False:
                        process = Popen(target, shell=True, stdout=PIPE)
                        process.wait()
                        out, err = process.communicate()

        except RuntimeError as exec_error:
            print("Error on Plugin manager call : " + str(exec_error))
        except BaseException as e:
            print("Standard Exception : " + str(e))


    def run(self):
        """
        Launch the daemon (ready to process event) and the http server
        """
        self._is_running = True
        self._th.start()
        self._ds.run()
        self._interpretor.run()

    def stop(self):
        """
        Stop the daemon and the http server
        """
        self._is_running = False
        self._ds.stop()
        self._interpretor.stop()

    def add_event(self, event):
        """
        Add an event to the event queue

            @param event: the event to add to the queue
            @type event: Event
        """
        self._event_queue.put_nowait(event)

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

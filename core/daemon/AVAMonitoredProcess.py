
import sys
import os
import multiprocessing

class AVAMonitoredProcess(object):
    """
        To encapsulate a process meant to be monitored by ava

        :param plugin : The plugin object returned by the plugin manager
        :param parent_connection : multiprocess.queue linked to AVA Daemon

        :attr pid : this process pid
        :attr answer_timeout : timeout waiting for data transmission
    """
    def __init__(self, plugin, parent_connection):
        super(AVAMonitoredProcess, self).__init__()
        self._plugin = plugin
        self._connection = parent_connection
        self._pid = os.getpid();
        self._answer_timeout = 1;

    def get() :
#        if not self._connection.isEmpty() :
        return self._connection.get(timeout=self._answer_timeout) if not self._connection.isEmpty() else False

    def send(message):
        self._connection.put(message)

    def execute(command):
        args_received = self.get()
        result = "";
        try :
            if args_received is not False:
                result = str(self._plugin.get_commands[command](args_received))
            else :
                result = str(self._plugin.get_commands[command]())
        except Exception as plugin_execution_error:
            result += "[ --- ]" + str(plugin_execution_error)
        send(result);

from os import path

class Builtin():
    """
    The Builtin class is the class that will manage built-ins
    """
    def __init__(self, daemon_inst):
        """
        Initializer

            @param daemon_inst: a reference to the daemon object
            @type daemon_inst: Daemon
        """
        self._daemon = daemon_inst

    def exec_builtin(self, cmd):
        """
        Method that will call the right builtin if the command have to be
        handle by it.

            @param cmd: the input command parsed
            @type cmd: list
            @return: if a builtin handle the command
            @rtype: bool
        """
        func = Builtin.builtins.get(cmd[0])
        if func is None:
            return False
        func(self, cmd)
        return True

    def install_plugin(self, cmd):
        """
        Install a plugin

            @param cmd: the input command parsed
            @type cmd: list
        """
        plugin_path = path.join(self._daemon._config.get('plugin_folder_download'))
        plugin_path = self._daemon._config.resolve_path_from_root(plugin_path, cmd[1] + '.zip')
        self._daemon.install_plugin(plugin_path)

    def uninstall_plugin(self, cmd):
        """
        Uninstall a plugin

            @param cmd: the input command parsed
            @type cmd: list
        """
        self._daemon.uninstall_plugin(cmd[1])

    def enable_plugin(self, cmd):
        """
        Enable a plugin

            @param cmd: the input command parsed
            @type cmd: list
        """
        self._daemon.enable_plugin(cmd[1])

    def disable_plugin(self, cmd):
        """
        Disable a plugin

            @param cmd: the input command parsed
            @type cmd: list
        """
        self._daemon.disable_plugin(cmd[1])

    builtins = {
        'install': install_plugin,
        'uninstall': uninstall_plugin,
        'enable': enable_plugin,
        'disable': disable_plugin
    }

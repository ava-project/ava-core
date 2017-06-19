import os
from .package import *
from .execution import *
from avasdk.plugins.ioutils.utils import *
from avasdk.exceptions import RuntimeError

class plugins_manager(object):
    """ AVA plugins manager
    """

    def __init__(self, path):
        """
        Initializer
            @param:
                - string (/path/to/the/plugins/directory)
        """
        self._path = path
        self._plugins_list = {}
        self._plugins_running = {}
        self._plugins_disabled = []
        self._commands_for_a_specific_plugin = {}
        self._load_plugins()


    #
    #  Private methods
    #
    def _retrieve_plugins_name_and_files_extension(self, skip):
        """
        Handler for retrieving plugins names and files' extension
            @param:
                - skip: string  (extension to skip i.e "json")
            @behave:
                - raises an error if the specified directory does not exist.
        """
        if os.path.isdir(self._path) == False:
            raise RuntimeError(__name__, self._retrieve_plugins_name_and_files_extension.__name__, " Invalid path to the plugins' directory.")

        for directory in os.listdir(self._path):
            if self._plugins_list.get(directory) is not None:
                continue
            if os.path.isdir(self._path + '/' + directory) == True:
                for file in os.listdir(self._path + '/' + directory):
                    if file == 'setup.py':
                        continue
                    if file.find(".") > 0 and file[file.find(".") + 1:] not in skip:
                        self._plugins_list[directory] = {'lang': file[file.find(".") + 1:]}



    def _load_plugins(self):
        """
        Loads every plugin and caches the data.
        """
        try:
            self._retrieve_plugins_name_and_files_extension(['json', 'txt'])

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])

        try:
            for key, value in self._plugins_list.items():
                if len(self._plugins_list[key]) > 1:
                    continue
                parse_json_file_to_dictionary(self._path + '/' + key, self._plugins_list[key])
                if self._plugins_list[key]['build'] == True:
                    install_and_manage_packages(self._plugins_list[key])

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])



    def _extract_commands(self, skip):
        """
        Extracts each command name and its phonetic equivalent for a specific plugin.

            @return:
                Returns a dictionary formated as following {key, value} with:
                    - key: string (the commmand name)
                    - value: string (phonetic equivalent)
        """
        return {x: self._commands_for_a_specific_plugin[x] for x in self._commands_for_a_specific_plugin if x not in skip}


    #
    # Plugins handling
    #
    def install(self, path):
        """
        Install a plugin from the given zip file by unziping and copying its content to the plugins' directory
            @param:
                - string (/path/to/the/zip/file)

            @behave:
                - raises an error if the object pointed by 'path' is not a valid zip file.
        """
        try:
            unzip(path, self._path)
            self._load_plugins()

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])



    def uninstall(self, plugin):
        """
        Uninstall a plugin by removing the plugin's directory and all its content.
            @param:
                - string (plugin to uninstall)
        """
        try:
            remove_directory(self._path + '/' + plugin)

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])
            return

        if self._plugins_list.get(plugin) is not None:
            self._plugins_list.pop(plugin, None)
        if self._plugins_running.get(plugin) is not None:
            self._plugins_running.pop(plugin, None)



    def enable(self, plugin):
        """
        Enables the specified plugin

            @param:
                - plugin: string (the plugin name)

            @behave:
                - Plugins are enabled by default. Use this method if you want to
                enable a plugin which has been disabled by the 'disable' method.
        """
        if self._plugins_list.get(plugin) is None:
            return False
        if plugin in self._plugins_disabled:
            self._plugins_disabled.remove(plugin)
        return True



    def disable(self, plugin):
        """
        Disables the specified plugin

            @param:
                - plugin: string(the plugin name)
        """
        if self._plugins_list.get(plugin) is not None:
            if self._plugins_running.get(plugin) is not None:
                self._plugins_running.pop(plugin, None)
            if plugin in self._plugins_disabled:
                pass
            else:
                self._plugins_disabled.append(plugin)
            return True
        return False



    def get_commands(self, plugin):
        """
        Returns a dictionary containing the commands for the specified plugin. Data are kept in memory.

            @param:
                -   plugin: string (the plugin name)

            @return:
                Returns None if there is no such plugin, otherwise a dictionary formated as following:
                {key, value} with key: string (the command name)
                                value: sring (the phonetic equivalent of the command)
        """
        if self._plugins_list.get(plugin) is None:
            return None

        if self._commands_for_a_specific_plugin.get('name') is not None and self.commands_for_a_specific_plugin['name'] == plugin:
                return self._extract_commands("name")

        self._commands_for_a_specific_plugin.clear()
        self._commands_for_a_specific_plugin['name'] = plugin
        for cmd in self._plugins_list[plugin]['commands']:
            self._commands_for_a_specific_plugin[cmd['name']] = cmd['phonetic']
        return self._extract_commands("name")



    def run(self, plugin, command):
        """
        The main function of the plugins manager. If there is the corresponding
        plugin available, it performs the given command.

            @params:
                - plugin: string (plugin name)
                - command: string (the command to execute)

            @return:
                Return a boolean and a string {Boolean, String}.
                    - boolean: True of False whether an operation has been performed.
                    - string: Status of the operation
        """
        if self._plugins_list.get(plugin) is None:
            return False, "No plugin named '" + plugin + "' found."

        if plugin in self._plugins_disabled:
            return False, "The plugin named '" + plugin + "' is currently disabled."

        switcher = {
            "cpp": handle_cpp,
            "go": handle_go,
        }.get(self._plugins_list[plugin]['lang'], handle_python)(plugin, command, self._plugins_running)

        return switcher

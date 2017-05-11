import os, importlib
from avasdk.plugins.ioutils.utils import *
from avasdk.plugins.ioutils.exceptions import RuntimeError

class plugins_manager(object):
    """ AVA plugins-manager """

    def __init__(self, path):
        """
        Initializer
            @param:
                - string (/path/to/the/plugins/directory)
        """
        self.path = path
        self.plugins_list = {}
        self.plugins_running = {}
        self.plugins_disabled = []
        self.commands_for_a_specific_plugin = {}
        self.load_plugins()


    #
    #  Internal features
    #
    def retrieve_plugins_name_and_files_extension(self, skip):
        """
        Handler for retrieving plugins names and files' extension
            @param:
                - skip: string  (extension to skip i.e "json")
            @behave:
                - raises an error if the specified directory does not exist.
        """
        if os.path.isdir(self.path) == False:
            raise RuntimeError(__name__, self.retrieve_plugins_name_and_files_extension.__name__, " Invalid path to the plugins' directory.")

        for directory in os.listdir(self.path):
            if self.plugins_list.get(directory) is not None:
                continue
            if os.path.isdir(self.path + '/' + directory) == True:
                for file in os.listdir(self.path + '/' + directory):
                    if file.find(".") > 0 and file[file.find(".") + 1:] != skip:
                        self.plugins_list[directory] = {'lang': file[file.find(".") + 1:]}


    def load_plugins(self):
        """
        Loads every plugin and caches the data.
        """
        try:
            self.retrieve_plugins_name_and_files_extension("json")

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])

        try:
            for key, value in self.plugins_list.items():
                if len(self.plugins_list[key]) > 1:
                    continue
                parse_json_file_to_dictionary(self.path + '/' + key, self.plugins_list[key])

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])


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
            unzip(path, self.path)
            self.load_plugins()

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])


    def uninstall(self, plugin):
        """
        Uninstall a plugin by removing the plugin's directory and all its content.
            @param:
                - string (plugin to uninstall)
        """
        try:
            remove_directory(self.path + '/' + plugin)

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])
            return

        if self.plugins_list.get(plugin) is not None:
            self.plugins_list.pop(plugin, None)
        if self.plugins_running.get(plugin) is not None:
            self.plugins_running.pop(plugin, None)


    def enable(self, plugin):
        """
        Enables the specified plugin

            @param:
                - plugin: string (the plugin name)

            @behave:
                - Plugins are enabled by default. Use this method if you want to
                enable a plugin which has been disabled by the 'disable' method.
        """

        if self.plugins_list.get(plugin) is None:
            return False
        if plugin in self.plugins_disabled:
            self.plugins_disabled.remove(plugin)
        return True


    def disable(self, plugin):
        """
        Disables the specified plugin

            @param:
                - plugin: string(the plugin name)
        """

        if self.plugins_list.get(plugin) is not None:
            if self.plugins_running.get(plugin) is not None:
                self.plugins_running.pop(plugin, None)
            if plugin in self.plugins_disabled:
                pass
            else:
                self.plugins_disabled.append(plugin)
            return True

        return False




    def extract_commands(self, skip):
        """
        Extracts each command name and its phonetic equivalent for a specific plugin.

            @return:
                Returns a dictionary formated as following {key, value} with:
                    - key: string (the commmand name)
                    - value: string (phonetic equivalent)
        """
        return {x: self.commands_for_a_specific_plugin[x] for x in self.commands_for_a_specific_plugin if x not in skip}


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
        if self.plugins_list.get(plugin) is None:
            return None

        if self.commands_for_a_specific_plugin.get('name') is not None and self.commands_for_a_specific_plugin['name'] == plugin:
                return self.extract_commands("name")

        self.commands_for_a_specific_plugin.clear()
        self.commands_for_a_specific_plugin['name'] = plugin
        for cmd in self.plugins_list[plugin]['commands']:
            self.commands_for_a_specific_plugin[cmd['name']] = cmd['phonetic']
        return self.extract_commands("name")


    #
    # Execution handling
    #
    def handle_cpp(self, plugin, command):
        """ C++ handler to execute plugin's features """
        print("CPP: " + plugin + " - "  + command)
        return True, ""


    def handle_go(self, plugin, command):
        """ Golang handler to execute plugin's features """
        print("GO: " + plugin + " - "  + command)
        return True, ""


    def handle_python(self, plugin, command):
        """
        Python handler to execute plugin's features
            @params:
              - plugin: string (plugin name)
              - command: string (the command to execute)

            @return:
              Returns a boolean and a string {Boolean, String}.
                    boolean: True of False whether an operation has been performed.
                    string: Status of the operation
        """
        if self.plugins_running.get(plugin) is None:
            self.plugins_running[plugin] = getattr(importlib.import_module("plugins." + plugin + "." + plugin), plugin)()

        if self.plugins_running[plugin].get_commands().get(command) is None:
            return False, "The plugin '" + plugin + "' cannot handle the following command: " + command

        else:
            self.plugins_running[plugin].get_commands()[command]()
            return True, "Command correctly executed."



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
        if self.plugins_list.get(plugin) is None:
            return False, "No plugin named '" + plugin + "' found."

        if plugin in self.plugins_disabled:
            return False, "The plugin named '" + plugin + "' is currently disabled."

        switcher = {
            "cpp": self.handle_cpp,
            "go": self.handle_go,
        }.get(self.plugins_list[plugin]['lang'], self.handle_python)(plugin, command)

        return switcher

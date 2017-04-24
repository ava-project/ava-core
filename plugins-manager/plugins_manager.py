import os
import importlib
from avasdk.ioutils.exceptions import RuntimeError
from avasdk.ioutils.utils import unzip, remove_directory, format_output, parse_json_file_to_dictionary

class plugins_manager(object):
    "Handles AVA plugins"

    # Constructor
    # @param: string (/path/to/the/plugins/directory)
    def __init__(self, path):
        self.path = path
        self.plugins_list = {}
        self.plugins_running = {}


    # Handler for retrieving plugins names and files' extension
    # @param:
    #   - skip: string  (extension to skip i.e "json")
    #
    # @behave: raise an error if the specified directory does not exist.
    def retrieve_plugins_name_and_files_extension(self, skip):
        if os.path.isdir(self.path) == False:
            raise RuntimeError(__name__, self.retrieve_plugins_name_and_files_extension.__name__,'Invalid path to the plugins directory.')

        for directory in os.listdir(self.path):
            if os.path.isdir(self.path + '/' + directory) == True:
                for file in os.listdir(self.path + '/' + directory):
                    if file.find(".") > 0 and file[file.find(".") + 1:] != skip:
                        self.plugins_list[directory] = {'lang': file[file.find(".") + 1:]}


    # Run the 'plugins' directory and list all plugins name as well as provided
    # files' extension.
    def load_plugins(self):
        self.plugins_list.clear()

        try:
            self.retrieve_plugins_name_and_files_extension("json")

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])

        try:
            for key, value in self.plugins_list.items():
                parse_json_file_to_dictionary(self.path + '/' + key, self.plugins_list[key])

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])


    # Install a plugin from the given zip file by unziping and copying its content to the plugins' directory
    # @param: string (/path/to/the/zip/file)
    #
    # @behave: raise an error if the object pointed by 'path' is not a valid zip file.
    def install(self, path):
        try:
            unzip(path, self.path)
            self.load_plugins()

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])


    # Uninstall a plugin by removing the plugin's directory and all its content.
    # @param: string (plugin to uninstall)
    def uninstall(self, plugin):
        try:
            remove_directory(self.path + '/' + plugin)

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])
            return

        self.plugins_list.pop(plugin, None)
        self.plugins_running.pop(plugin, None)


    # C++ handler to execute plugin's features
    #
    #
    def handle_cpp(self, plugin, command):
        print("CPP: " + plugin + " - "  + command)
        return True, ""


    # Golang handler to execute plugin's features
    #
    #
    def handle_go(self, plugin, command):
        print("GO: " + plugin + " - "  + command)
        return True, ""


    # Python handler to execute plugin's features
    # @params:
    #   - plugin: string (plugin name)
    #   - command: string (the command to execute)
    #
    # @return:
    #   Return a boolean and a string {Boolean, String}.
    #         boolean: True of False whether an operation has been performed.
    #         string: Status of the operation
    #
    def handle_python(self, plugin, command):
        if self.plugins_running.get(plugin) is None:
            module = importlib.import_module(self.path + "." + plugin + "." + plugin)
            plugin_instance = getattr(module, plugin)
            self.plugins_running[plugin] = plugin_instance()
            if self.plugins_running[plugin].get_commands().get(command) is None:
                return False, "The plugin '" + plugin + "' cannot handle the following command: " + command
            else:
                self.plugins_running[plugin].get_commands()[command]()
                return True, "Command correctly executed."
        else:
            if self.plugins_running[plugin].get_commands().get(command) is None:
                return False, "The plugin '" + plugin + "' cannot handle the following command: " + command
            else:
                self.plugins_running[plugin].get_commands()[command]()
                return True, "Command correctly executed."



    # The main function of the plugins manager. If there is the corresponding
    # plugin available, it performs the given command.
    #
    # @params:
    #   - plugin: string (plugin name)
    #   - command: string (the command to execute)
    #
    # @return:
    #   Return a boolean and a string {Boolean, String}.
    #         boolean: True of False whether an operation has been performed.
    #         string: Status of the operation

    def run(self, plugin, command):
        if self.plugins_list.get(plugin) is None:
            return False, "No plugin named '" + plugin + "' found."

        lang = self.plugins_list[plugin]['lang']

        switcher = {
            "cpp": self.handle_cpp,
            "go": self.handle_go,
        }.get(lang, self.handle_python)(plugin, command)

        return switcher

# from utils import retrieve_plugins_name_and_files_extension
import os
from utils import format_output, remove_directory, unzip, parse_json_file_to_dictionary


class plugins_manager(object):
    "Handles AVA plugins"

    # Constructor
    # @param: string (/path/to/the/plugins/directory)
    def __init__(self, path):
        self.path = path
        self.plugins_list = {}


    # Handler for retrieving plugins names and files' extension
    # @param:
    #   - skip: string  (extension to skip i.e "json")
    #
    # @behave: raise an error if the specified directory does not exist.
    def retrieve_plugins_name_and_files_extension(self, skip):
        if os.path.isdir(self.path) == False:
            raise
        for directory in os.listdir(self.path):
            if os.path.isdir(self.path + '/' + directory) == True:
                for file in os.listdir(self.path + '/' + directory):
                    if file.find(".") > 0 and file[file.find(".") + 1:] != skip:
                        self.plugins_list[directory] = {'lang': file[file.find(".") + 1:]}


    # Run the 'plugins' directory and list all plugins name as well as provided
    # files' extension.
    def load_plugins(self):
        try:
            self.retrieve_plugins_name_and_files_extension("json")
        except:
            print(format_output(__name__, self.load_plugins.__name__) + "invalid path to the plugins' directory")

        for key, value in self.plugins_list.items():
            parse_json_file_to_dictionary(self.path + '/' + key, self.plugins_list[key])


    # Install a plugin from the given zip file by unziping and copying its content to the plugins' directory
    # @param: string (/path/to/the/zip/file)
    #
    # @behave: raise an error if the object pointer by 'path' is not a file.
    def install(self, path):
        if os.path.isfile(path) == True:
            try:
                unzip(path, self.path)
            except:
                print(format_output(__name__, self.install.__name__) + "error while unziping " + path)
        else:
            print(format_output(__name__, self.install.__name__) + "No such file or directory: " + path)


    # Uninstall a plugin by removing the plugin's directory and all its content.
    # @param: string (plugin to uninstall)
    def uninstall(self, plugin):
        try:
            remove_directory(self.path + '/' + plugin)
        except:
            print(format_output(__name__, self.uninstall.__name__) + "Specified plugin doesn't exist [" + plugin + "]")
            return
        self.plugins_list.pop(plugin, None)

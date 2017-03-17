from utils import retrieve_plugins_name_and_files_extension
from utils import format_output, remove_directory, parse_json_file_to_dictionary


class plugins_manager(object):
    "Handles AVA plugins"

    # Constructor
    # @param: string (/path/to/the/plugins/directory)
    def __init__(self, path):
        self.path = path
        self.plugins_list = {}

    # Run the 'plugins' directory and list all plugins name as well as provided
    # files' extension.
    def load_plugins(self):
        try:
            retrieve_plugins_name_and_files_extension(self.path, "json", self.plugins_list)
        except:
            print(format_output(__name__, self.load_plugins.__name__) + "invalid path to the plugins' directory.")

        for key, value in self.plugins_list.items():
            parse_json_file_to_dictionary(self.path + '/' + key, self.plugins_list[key])

    # Uninstall a plugin by removing the plugin's directory and all its content.
    # @param: string (plugin to uninstall)
    def uninstall(self, plugin):
        try:
            remove_directory(self.path + '/' + plugin)
        except:
            print(format_output(__name__, self.uninstall.__name__) + "Specified plugin doesn't exist [" + plugin + "]")
            return
        self.plugins_list.pop(plugin, None)

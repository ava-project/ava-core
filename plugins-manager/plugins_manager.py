from utils import retrieve_plugins_name_and_files_extension, remove_directory

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
            print("[plugins_manager]: invalid path to the plugins' directory.")

    # Uninstall a plugin by removing the plugin's directory and all its content.
    # @param: string (plugin to uninstall)
    def uninstall(self, plugin):
        try:
            remove_directory(self.path + '/' + plugin)
        except:
            print("[plugins_manager]: Specified plugin doesn't exist [" + plugin + "]")
            return
        self.plugins_list.pop(plugin, None)

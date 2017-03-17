from utils import retrieve_plugins_name_and_files_extension

class plugins_manager(object):
    "This class handles plugins"
    def __init__(self, path):
        self.path = path
        self.plugins_list = {}

    def load_plugins(self):
        retrieve_plugins_name_and_files_extension(self.path, "json", self.plugins_list)

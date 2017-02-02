import json

class ConfigManager:
    """This class will load the config file"""

    def __init__(self, path=None):
        self._path = path
        self._json = None
        self.parse()

    def set_config_path(self, new_path):
        self._path = new_path
        self.parse()

    def parse(self):
        if self._path is not None:
            with open(self._path) as data_file:
                self._json = json.load(data_file)

    
import json

class ConfigLoader():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self._file_loaded = None

    def load(self, filename):
        with open(self.folder_path + filename) as ofile:
            self._file_loaded = json.load(ofile)

    def get(self, path):
        properties = path.split('/')
        prop = None
        for key in properties:
            prop = self._file_loaded[key]

        return prop

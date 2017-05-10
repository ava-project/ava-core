import subprocess

class git(object):
    "Git plugin"

    def __init__(self):
        self.commands = {
            'log': self.log,
            'version': self.version,
        }

    def log(self):
        subprocess.call(["git", "log"])

    def version(self):
        subprocess.call(["git", "version"])


    def get_commands(self):
        return self.commands

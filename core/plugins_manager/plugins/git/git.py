import subprocess
from avasdk.plugins.python_model import PythonModel

class git(PythonModel):
    """
        Git plugin
    """

    def __init__(self, name="Git"):
        super(git, self).__init__(name)
        self.set_commands_list({**PythonModel._commands, **{\
        "log" : self.log, \
        "version" : self.version, \
        }})

    def log(self, command):
        subprocess.call(["git", "log"])

    def version(self, command):
        subprocess.call(["git", "version"])

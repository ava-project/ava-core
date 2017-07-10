import subprocess
from avasdk.plugins.python_model import PythonModel

class ssh(PythonModel):
    """
        SSH plugin
    """

    def __init__(self, name="SSH"):
        super(ssh, self).__init__(name)
        self.set_commands_list({**PythonModel._commands, **{\
        "connect" : self.connect, \
        }})

    def connect(self, command):
        subprocess.call(["ssh", "root@193.70.42.59"])

import subprocess

class ssh(object):
    "SSH plugin"

    def __init__(self):
        self.commands = {
            'connect': self.connect,
        }

    def connect(self, command):
        subprocess.call(["ssh", "root@193.70.42.59"])

    def get_commands(self):
        return self.commands

class git(object):
    "Git plugin"

    def __init__(self):
        self.commands = {
            'log': self.log,
            'version': self.version,
        }

    def log(self):
        print("PLUGIN: GIT - CMD = LOG !!!!")

    def version(self):
        print("PLUGIN: GIT - CMD = VERSION !!!!")


    def get_commands(self):
        return self.commands

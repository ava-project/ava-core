class git(object):
    "Git plugin"

    def log(self):
        print("GIT LOG !!!!")

    def version(self):
        print("GIT VERSION !!!!")

    def handle(self, command):
        if command == "log":
            self.log()
        elif command == "version":
            self.version()
        else:
            return

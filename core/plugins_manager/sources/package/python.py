import pip

def install_from_requirements(path, plugin):
    print(path)
    print(plugin)

    pip.main(['install', '-r', path + plugin['name'] + "/requirements.txt"])

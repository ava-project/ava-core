import pip, json

def install_from_requirements(plugin):

    with open('settings.json') as json_file:
        conf = json.load(json_file)

    pip.main(['install', '-r', conf['plugin_folder_install'] + '/' + plugin['name'] + "/requirements.txt"])

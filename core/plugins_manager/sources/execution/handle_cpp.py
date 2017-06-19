import importlib, json

def handle_cpp(plugin, command, plugins_running):
    """
    Handler to execute the features of a plugin written in C++.
    """
    cmd = command.split(' ')
    args = ' '.join(cmd[1:])

    with open('settings.json') as json_file:
        conf = json.load(json_file)

    with open(conf['plugin_folder_install'] + '/' + plugin + '/manifest.json') as json_file:
        data = json.load(json_file)

    for c in data['commands']:
        if cmd[0] in c['name']:

                if plugins_running.get(plugin) is None:
                    plugins_running[plugin] = getattr(importlib.import_module(plugin), cmd[0])

                plugins_running[plugin](args)
                return True, "Command correctly executed."

    return False,  "The plugin '" + plugin + "' cannot handle the following command: " + cmd[0]

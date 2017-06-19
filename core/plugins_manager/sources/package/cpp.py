import subprocess, json

def install_cpp_dependencies(plugin):

    with open('settings.json') as json_file:
        conf = json.load(json_file)

    setup = conf['plugin_folder_install'] + '/' + plugin['name'] + '/setup.py'
    subprocess.call(['python', setup, 'build'])
    subprocess.call(['python', setup, 'install'])

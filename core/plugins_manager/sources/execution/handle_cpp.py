import importlib

def handle_cpp(plugin, user_command, plugins_running):
    """
    Handler to execute the features of a plugin written in C++.
    """

    command = user_command.split(' ')
    args = ' '.join(command[1:])

    if plugins_running.get(plugin) is None:
        plugins_running[plugin] = getattr(importlib.import_module(plugin), command[0])

    print(plugins_running[plugin])
    print(plugins_running[plugin](args))
    return True, ""

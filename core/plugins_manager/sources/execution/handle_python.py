import importlib

def handle_python(plugin, user_command, plugins_running):
    """
    Python handler to execute plugin's features
        @params:
          - plugin: string (plugin name)
          - command: string (the command to execute)

        @return:
          Returns a boolean and a string {Boolean, String}.
                boolean: True of False whether an operation has been performed.
                string: Status of the operation
    """
    command = user_command.split(' ')
    if plugins_running.get(plugin) is None:
        plugins_running[plugin] = getattr(importlib.import_module("core.plugins_manager.plugins." + plugin + "." + plugin), plugin)()

    if plugins_running[plugin].get_commands().get(command[0]) is None:
        return False, "The plugin '" + plugin + "' cannot handle the following command: " + command[0]

    else:
        plugins_running[plugin].get_commands()[command[0]](str(' '.join(command[1:])))
        return True, "Command correctly executed."

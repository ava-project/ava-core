import avasdk
from plugins_manager import plugins_manager

if __name__ == "__main__":
    # Instanciate a plugins manager by specifying the path to the directory
    # storing the plugins' sources.
    manager = plugins_manager("./plugins")

    # Install a specific plugin by specifying the path to the zipfile containing
    # the plugin's sources.
    manager.install("./demo/ssh.zip")

    # Print all data stored for a specific plugin.
    print(manager.plugins_list['git'], "\n")

    # Retrieve a dictionary containing the commands handled by a specific plugin
    # as well as their phonetic equivalent.
    test = manager.get_commands("git")
    print(test, "\n")

    #
    #  Run a specific command for a dedicated plugin:
    #       result describes if the command has been performed.
    #       status describes how the command has been performed.
    #
    (result, status) = manager.run("git", "version")
    print(result, status, "\n")

    (result, status) = manager.run("ssh", "connect")
    print(result, status, "\n")

    # Uninstall the specified plugin.
    manager.uninstall("ssh")



    #
    # Enabling/disabling a plugin.
    #
    #
    # result = manager.disable(the_plugin_name)
    #   Returns true or false wether the plugin has been correctly disabled.
    #
    # Same behave for the 'enable' method:
    #
    # result = manager.enable(the_plugin_name)
    #   Returns true or false wether the plugin has been correctly enabled.

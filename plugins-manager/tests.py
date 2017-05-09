import avasdk
from plugins_manager import plugins_manager

if __name__ == "__main__":
    #
    manager = plugins_manager("./plugins")

    #
    manager.install("./demo/ssh.zip")

    #
    print('\n', manager.plugins_list['git'], '\n')

    #
    test = manager.get_commands("git")
    print('\n', test, '\n')

    #
    (result, status) = manager.run("git", "version")
    print('\n', result, status, '\n')
    #
    # #
    (result, status) = manager.run("ssh", "connect")
    print(result, status, '\n')

    # Uninstall the specified plugin.
    manager.uninstall("ssh")


    result = manager.disable_plugin("git")
    print(result)

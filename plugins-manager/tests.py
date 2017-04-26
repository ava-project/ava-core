import avasdk
from plugins_manager import plugins_manager

if __name__ == "__main__":
    # Print the version of the avasdk
    print(avasdk.__version__)
    # Instanciate the plugins manager
    # param: the path to the plugins' repository
    manager = plugins_manager("./plugins")
    # Load the plugins, this method must be called just after the instanciation
    # of the plugins manager.
    manager.load_plugins()

    print("\nDEBUG 1: ", manager.plugins_list, "\n")
    # Install a plugin by specifying the path towards the zipfile containing the plugin.
    # If an user wants to install a plugin through the CLI, the same method must be used.
    manager.install("./atom.zip")
    # Print cached information for a specific plugin.
    print("\nDEBUG 2: ", manager.plugins_list['atom'], "\n")
    # Uninstall the specified plugin.
    manager.uninstall("atom")
    print("\nDEBUG 3:", manager.plugins_list, "\n")
    #
    # Examples:
    #
    # Below some examples of how the 'run' method should be used.
    (result, status) = manager.run("atom", "atomizer")
    print(result, status)
    (result, status) = manager.run("git", "version")
    print(result, status)
    (result, status) = manager.run("ssh", "connect")
    print(result, status)

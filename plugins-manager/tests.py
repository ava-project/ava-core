import avasdk
from plugins_manager import plugins_manager

if __name__ == "__main__":
    print(avasdk.__version__)
    manager = plugins_manager("./dir_test")
    manager.install("./dir_test/atom.zip")
    manager.load_plugins()
    print(manager.plugins_list)
    manager.uninstall("atom")
    print("### DEBUG ###")
    print(manager.plugins_list)

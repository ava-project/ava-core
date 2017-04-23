import avasdk
from plugins_manager import plugins_manager

if __name__ == "__main__":
    print(avasdk.__version__)
    manager = plugins_manager("./dir_test")
    manager.load_plugins()
    print(manager.plugins_list)
    print("### DEBUG ###")
    manager.install("./dir_test/atom.zip")
    print(manager.plugins_list['atom'])
    manager.uninstall("atom")

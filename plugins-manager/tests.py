from plugins_manager import plugins_manager

if __name__ == "__main__":
    manager = plugins_manager("./dir_test")
    manager.load_plugins()
    for plugin, language in manager.plugins_list.items():
        print(plugin, language)

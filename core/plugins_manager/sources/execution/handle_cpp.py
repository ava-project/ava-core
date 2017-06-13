def handle_cpp(plugin, command, plugins_running):
    """ C++ handler to execute plugin's features """
    print("CPP: " + plugin + " - "  + command)
    return True, ""

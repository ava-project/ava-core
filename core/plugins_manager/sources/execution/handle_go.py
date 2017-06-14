def handle_go(plugin, command, plugins_running):
    """ Golang handler to execute plugin's features """
    print("GO: " + plugin + " - "  + command)
    return True, ""

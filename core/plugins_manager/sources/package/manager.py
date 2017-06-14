from .go import install_go_packages
from .python import install, install_from_requirements

PATH_TO_PLUGINS_FOLDER = "core/plugins_manager/plugins/"

def install_and_manage_packages(plugin):
    switcher = {
        "go": install_go_packages,
    }.get(plugin['lang'], install_from_requirements)(PATH_TO_PLUGINS_FOLDER, plugin)

    return switcher

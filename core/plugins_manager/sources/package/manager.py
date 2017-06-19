from .go import install_go_packages
from .cpp import install_cpp_dependencies
from .python import install_from_requirements

def install_and_manage_packages(plugin):

    switcher = {
        "go": install_go_packages,
        "cpp": install_cpp_dependencies,
    }.get(plugin['lang'], install_from_requirements)(plugin)

    return switcher

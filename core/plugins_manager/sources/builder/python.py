import pip

def install(package):
    pip.main(['install', package])

def install_from_requirements(requirements):
    pip.main(['install -r', requirements])

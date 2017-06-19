from distutils.core import setup, Extension

module = Extension('hello_world', sources=['core/plugins_manager/plugins/hello_world/hello_world.cpp'])
setup(name = 'packagename',
    version='1.0',
    description = 'a test package',
    ext_modules = [module])

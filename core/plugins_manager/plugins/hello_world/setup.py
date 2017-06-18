from distutils.core import setup, Extension

module = Extension('Hello_world', sources=['Hello_world.cpp'])
setup(name = 'packagename',
    version='1.0',
    description = 'a test package',
    ext_modules = [module])

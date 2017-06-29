# -*- coding: utf-8 -*-

import re

from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('core/version.py').read(),
    re.M
    ).group(1)

setup(

    name='avacore',
    version=version,
    packages=find_packages(),
    author='AVA Project',
    author_email='ava_2018@labeip.epitech.eu',
    description='The daemon of the AVA Project',
    long_description=open('README.md').read(),
    install_requires=[
        'flask==0.12',
        'avasdk',
        'requests'
    ],
    include_package_data=True,
    url='https://github.com/ava-project/ava-core',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'ava = core.ava:main',
        ],
    },
)

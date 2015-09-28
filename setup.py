#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Generate \'at\' commands for delayed execution',
    'author': 'Rick van de Loo',
    'url': 'https://github.com/vdloo/atscheduler',
    'author_email': 'rickvandeloo@gmail.com',
    'version': '0.1',
    'packages': ['atmap'],
    'name': 'atmap',
    'scripts': ['bin/atscheduler'],
    'install_requires': ['python-dateutil']
}

setup(**config)

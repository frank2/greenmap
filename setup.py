#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'greenmap'
    ,version = '1.0.0'
    ,author = 'frank2'
    ,author_email = 'frank2@dc949.org'
    ,description = 'A greenlet-based connect-style network scanner'
    ,license = 'GPLv3'
    ,keywords = 'network scanner'
    ,url = 'https://github.com/frank2/greenmap'
    ,package_dir = {'greenmap': 'lib'}
    ,packages = ['greenmap']
    ,install_requires = ['gevent', 'martinellis']
    ,long_description = '''A network-scanner program/library based on Greenlet.'''
    ,classifiers = [
        'Development Status :: 3 - Alpha'
        ,'Topic :: Internet'
        ,'Topic :: Software Development :: Libraries'
        ,'License :: OSI Approved :: GNU General Public License v3 (GPLv3)']
)

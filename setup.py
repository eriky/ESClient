#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sys import version_info

with open('README.rst') as file:
    long_description = file.read()

install_requires = ['requests']

if version_info < (2,7):
    install_requires.append('argparse')

setup(name='ESClient',
        version="0.5.8",
        description='A lightweight Python client for ElasticSearch, including a dump and import tool for indexes',
        author='Erik-Jan van Baaren',
        author_email='erikjan@gmail.com',
        url='https://github.com/eriky/ESClient',
        py_modules=['esclient'],
        license='New BSD license',
        keywords = ["elasticsearch"],
        install_requires = install_requires,
        scripts = ['bin/esdump', 'bin/esimport'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
            ],
        long_description = long_description
        )

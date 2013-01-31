#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='ESClient',
        version="0.5.5",
        description='A lightweight Python client for ElasticSearch, including a dump and import tool for indexes',
        author='Erik-Jan van Baaren',
        author_email='erikjan@gmail.com',
        url='https://github.com/eriky/ESClient',
        py_modules=['esclient'],
        license='New BSD license',
        keywords = ["elasticsearch"],
        requires = ['requests (>= 0.10.0)'],
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

#!/usr/bin/env python

from distutils.core import setup
import esclient

with open('README.rst') as file:
    long_description = file.read()

setup(name='ESClient',
        version=esclient.get_version(),
        description='A lightweight Python client for ElasticSearch',
        author='Erik-Jan van Baaren',
        author_email='erikjan@gmail.com',
        url='https://github.com/eriky/ESClient',
        py_modules=['esclient'],
        license='New BSD license',
        keywords = ["elasticsearch"],
        install_requires = ['requests'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
            ],
        long_description = long_description
        )

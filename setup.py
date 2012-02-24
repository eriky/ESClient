#!/usr/bin/env python

from distutils.core import setup

setup(name='ESClient',
        version='0.1',
        description='A lightweight Python client for ElasticSearch',
        author='Erik-Jan van Baaren',
        author_email='erikjan@gmail.com',
        url='https://github.com/eriky/ESClient',
        packages=['esclient'],
        license='New BSD license',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
            ]
        )

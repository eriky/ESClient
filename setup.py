#!/usr/bin/env python

from distutils.core import setup
import esclient

setup(name='ESClient',
        version=esclient.get_version(),
        description='A lightweight Python client for ElasticSearch',
        author='Erik-Jan van Baaren',
        author_email='erikjan@gmail.com',
        url='https://github.com/eriky/ESClient',
        py_modules=['esclient'],
        license='New BSD license',
        keywords = ["elasticsearch"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
            ],
        long_description = """\
ESClient is a Python library that uses the ElasticSearch REST API. It is meant
to be lightweight and be close to the actual REST API in terms of usage."""
        )

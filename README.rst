========
ESClient
========
ESClient is a Python library that uses the ElasticSearch REST API. It is meant
to be lightweight and be *close to the actual REST API* in terms of usage.

Installation
============
To install:
	``python setup.py install``

You can also install ESClient with easy_install or pip.
The following commands will install the latest released version of ESClient:

    easy_install esclient
	
    or with pip:
	
    pip install esclient

Usage
=====
Please take a look at the test_esclient.py file for usage examples. This code
at least covers all the API methods that are implemented.
As soon as the API reaches stability I will put more time into writing decent
documentation. I advice you to keep the ElasticSearch documentation at hand
when you start using this library. The documentation strings in the code
should be very useful.

Unit tests
==========
test_esclient.py can be used for unit testing. You can directly run this file
if you have an ElasticSearch instance running on localhost.
On Python 2.7 and up, you can also run all unit tests with:
python -m unittest discover

Note that the code will create an index called 'contacts_esclient_test'.

Bug Tracker and Issues
======================
If you find a bug or any other issue you may create an issue on GitHub!

https://github.com/eriky/ESClient/issues

Roadmap
=======
Some stuff that is currently on the roadmap:

* Implementing more of the API methods
* Implementing bulk indexing
* Pass timeout to ElasticSearch

License
=======
Licensed under the New BSD License. See also the LICENSE file

Credits
=======
This client library was written by Erik-Jan van Baaren (erikjan@gmail.com)

A small amount of code is inspired by `pyelasticsearch`_.

Dependencies
============
ESClient uses the excellent *requests* library. If you don't have it installed
you can use easy_install or pip install to fetch it.

Alpha quality disclaimer
=======================
Please note that the development status of this software is labeled alpha. It has only been
tested in "lab setup". Comments, suggestions, code enhancements etc are very welcome!

.. _`pyelasticsearch`: http://github.com/rhec/pyelasticsearch

Changelog
=========
master branch
-------------

0.2.0
-----
* Removed option to choose between JSON or hierachy of Python objects. It
  would have created too much hassle.
* Added API methods: mget, open+close index, create_alias, delete_alias
* small fixes here and there

0.1.1
-----
* Added docstring to the get API
* made sure that makedist.sh removes old MANIFEST file before making new
  package
* fixed version string in esclient.py


0.1.0
-----
From now on I will conform to the Semantic Versioning Guidelines outlined
on this site: http://semver.org/
In that spirit, I bumped the minor version to 0.1.0 and will keep doing so
until public API stability is reached.

0.0.1
-----
First official release that was published to PyPI. Alpha quality, but with
working unit tests for each API method.


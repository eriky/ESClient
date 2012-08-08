========
ESClient
========
ESClient is a Python library that uses the ElasticSearch REST API. It is meant
to be lightweight and be *close to the actual REST API* in terms of usage.

:Web: http://pypi.python.org/pypi/ESClient/
:Download: http://pypi.python.org/pypi/ESClient/
:Source: https://github.com/eriky/ESClient/

Installation
============

To install::

    python setup.py install

You can also install ESClient with easy_install or pip.
The following commands will install the latest released version of ESClient::

  $ easy_install esclient

Or with pip::

  $ pip install esclient

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

Bug Tracker and Issues
======================
If you find a bug or any other issue you may create an issue on GitHub!

https://github.com/eriky/ESClient/issues

Roadmap
=======
My target is to reach a stable 1.0 release in the coming months.
Currently on the roadmap to reach a 1.0 release are:

* Implementing most or even all the API methods
* Implementing bulk indexing

You may have noticed this software is labeled as alpha quality. I will not
remove this label until I have done extensive testing and am convinced that
most errors are handled cleanly. For normal usage this software works pretty
well so don't be too frightened of the alpha label!

License
=======
Licensed under the New BSD License. See also the LICENSE file

Credits
=======
This client library was written by Erik-Jan van Baaren (erikjan@gmail.com)

The style of this library is inspired by `pyelasticsearch`_.

Dependencies
============
* ESClient uses the excellent *requests* library.
* The unit tests only work on Python 2.7
* The code is tested mostly on Python 2.7 too..

Changelog
=========
0.4.0
-----
* Added API method: index_exists

0.3.0
-----
* Better error handling (by using _parse_json_response() method everywhere)
* Added API methods: get_mapping, put_mapping

0.2.1
-----
* Added API methods: status, flush
* some code improvements / beautifying

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

.. _`pyelasticsearch`: http://github.com/rhec/pyelasticsearch


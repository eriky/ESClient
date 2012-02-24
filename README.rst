========
ESClient
========
ESClient is a Python library that uses the ElasticSearch REST API. It is meant
to be light weight and be close to the actual REST API.

Usage
=====
Please take a look at the test_esclient.py file for usage examples. This code
at least covers all the API methods that are implemented.

Unit tests
==========
test_esclient.py can be used for unit testing. You can directly run this file
if you have an ElasticSearch instance running on localhost.
On Python 2.7 and up, you can also run all unit tests with:
python -m unittest discover

Note that the code will create an index called 'contacts_esclient_test'.

Roadmap
=======
Some stuff that is currently on the roadmap:

* Implementing more of the API methods
* Implementing bulk indexing
* Add much more (debug) logging

License
=======
Licensed under the New BSD License. See also the LICENSE file

Credits
=======
This client library was written by Erik-Jan van Baaren (erikjan@gmail.com)

A small amount of code is inspired by `pyelasticsearch`_.

Alpha quality disclaimer
=======================
Please note that the development status of this software is labeled alpha. It has only been
tested in "lab setup". Comments, suggestions, code enhancements etc are very welcome!
.. _`pyelasticsearch`: http://github.com/rhec/pyelasticsearch

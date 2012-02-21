========
ESClient
========

ESClient is a Python library that uses the ElasticSearch REST API. It is meant to be light weight. You can easilly 

Usage
=====
Please take a look at the test_esclient.py file for usage examples. This code at least covers all the API methods that are implemented.

Unit tests
==========
test_esclient.py can be used for unit testing. You can directly run this file if you have an ElasticSearch instance running on localhost. Note that the code will create an index called 'contacts_esclient_test'. Make sure you do not run these unit tests on a production index with the same name ;-)

Roadmap
=======
Some stuff that is currently on the roadmap:

* Using the Python unittest framework
* Implementing more API methods

License
=======
Licensed under the New BSD License.

Credits
=======
I used and adapted some code from `pyelasticsearch`_. Both that project and ESClient try to archieve the same thing: an easy to use Python library that helps in accessing the raw ElasticSearch REST API. I will keep looking at pyelasticsearch for inspiration but I also explicitly wanted to start my own project.

.. _`pyelasticsearch`: http://github.com/rhec/pyelasticsearch
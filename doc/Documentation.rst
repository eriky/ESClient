==============
ESClient usage
==============

Start or install ElasticSearch
------------------------------
First of all, you have to get ElasticSearch running. If you don't have it
installed, please head over to the ElasticSearch_ site and download it.
Once unpacked, you can simply run ElasticSearch in the foreground with:

``bin/elasticsearch -f``

See.. it's easy to get a test system up and running.

.. _ElasticSearch: http://www.elasticsearch.org/

Installing ESClient
-------------------
Installing ESClient is easy too. You can use pip or easy_install, whichever
you prefer.

E.g. with easy_install you'd enter:

``sudo easy_install esclient``

Alternatively you may also download ESClient from its Github_ site. After
unpacking, you can install ESClient with:

``sudo python setup.py install``

.. _Github: https://github.com/eriky/ESClient

An interactive Python session
-----------------------------
To demonstrate ESClient, we will walk through an interactive Python session
and show the ESClient API by example.

First, fire up python:

``$ python``

At the prompt, enter:

``>>> import esclient``

You can read the documentation that comes with the esclient code by entering:

``>>> help(esclient)``
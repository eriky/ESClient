import requests
from urllib import urlencode
try:
    import simplejson as json   # try the faster simplejson on old versions
except:
    import json
import logging
log = logging.getLogger(__name__)

__author__ = 'Erik-Jan van Baaren'
__all__ = ['ESClient']
__version__ = (0, 2, 0)


def get_version():
        return "%s.%s.%s" % __version__


class ESClientException(Exception):
    pass


class ESClient:
    """ESClient is a Python library that uses the ElasticSearch REST API.

    ESClient methods will always return a hierachy of Python objects and not
    the pure JSON as returned by ElasticSearch.

    Take a look at the unit tests to see usage examples for all available API
    methods that this library implements.
    Any API calls that are not (yet) implemented by ESClient can still be used
    by using the send_request() method to directly do an HTTP request to the
    ElasticSearch API (if you are adventurous).

    """

    def __init__(self, es_url='http://localhost:9200', es_timeout=10):
        self.es_url = es_url
        self.es_timeout = es_timeout

        if self.es_url.endswith('/'):
            self.es_url = self.es_url[:-1]

    """
    Internal helper methods
    """

    def _make_path(self, path_components):
        """Create path from components. Empty components will be
        ignored.

        """
        path_components = map(str, filter(None, path_components))
        path = '/'.join(path_components)
        if not path.startswith('/'):
            path = '/' + path
        return path

    def check_result(self, list, key, value):
        """Check if key is an element of list, and check if that element
        is equal (==) to value.
        
        Returns True if the key exists and is equal to given value, false
        otherwise.
        """
        try:
            if list[key] == value:
                return True
            else:
                return False
        except:
            return False

    def send_request(self, method, path, body="", query_string_args={}):
        """Make a raw HTTP request to ElasticSearch.

        You may use this method to manually do whatever is not (yet) supported
        by ESClient. This method does not return anything, but sets the class
        variable called last_response, which is the response object returned
        by the requests library.

        Arguments:
        method -- HTTP method, e.g. 'GET', 'PUT', 'DELETE', etc.
        path -- URL path
        body -- the body, as a hierachy of Python objects that is parseable
                to JSON with json.dumps()
        query_string_args -- the query string arguments, which are the
        key=value pairs after the question mark in any URL.

        """
        if query_string_args:
            path = "?".join([path, urlencode(query_string_args)])

        kwargs = { 'timeout': self.es_timeout }
        url = self.es_url + path

        if body:
            kwargs['data'] = json.dumps(body)

        if not hasattr(requests, method.lower()):
            raise ESClientException("No such HTTP Method '%s'!" %
                                    method.upper())
        
        self.last_response = requests.request(method.lower(), url, **kwargs)

    def _search_operation(self, request_type, query_body=None,
                    operation_type="_search", query_string_args=None,
                    indexes=["_all"], doctypes=[]):
        """Perform a search operation. This method can be use for search,
        delete by search and count.

        Searching in ElasticSearch can be done in two ways:
        1) with a query string, by providing query_args
        2) using a full query body (JSON) by providing
        the query_body.
        You can choose one, but not both at the same time.

        """
        if query_body and query_string_args:
            raise ESClientException("Found both a query body and query" +
                                    "arguments")

        indexes = ','.join(indexes)
        doctypes = ','.join(doctypes)
        path = self._make_path([indexes, doctypes, operation_type])

        if query_body:
            self.send_request(request_type, path, body=query_body)
        elif query_string_args:
            self.send_request(request_type, path,
                              query_string_args=query_string_args)
        elif operation_type == "_count":
            """ If both options were not used, there one more option left: no
            query at all. A query is optional when counting, so we fire a
            request to the URL without a query only in this specific case. """
            self.send_request('GET', path)
        else:
            raise ESClientException("Mandatory query was not supplied")

        try:
            return json.loads(self.last_response.text)
        except:
            raise ESClientException("Was unable to parse the ElasticSearch "
            "response as JSON: \n%s", self.last_response.text)

    """
    The API methods
    """

    def index(self, index, doctype, body, docid=None, op_type=None):
        """Index the supplied document.

        Options:
        index -- the index name (e.g. twitter)
        doctype -- the document types (e.g. tweet)
        op_type -- "create" or None:
            "create": create document only if it does not exists already
            None: create document or update an existing document

        Returns True on success (document added/updated or already exists
        while using op_type="create") or False in all other instances.

        """
        args = dict()
        if op_type:
            args["op_type"] = op_type
        path = self._make_path([index, doctype, docid])
        self.send_request('POST', path, body=body, query_string_args=args)
        rescode = self.last_response.status_code
        if 200 <= rescode < 300:
            return True
        elif rescode == 409 and op_type == "create":
            # If document already exists, ES returns 409
            return True
        else:
            return False

    def search(self, query_body=None, query_string_args=None,
                indexes=["_all"], doctypes=[]):
        """Perform a search operation.

        Searching in ElasticSearch can be done in two ways:
        1) with a query string, by providing query_args
        2) using a full query body (JSON) by providing
        the query_body.
        You can choose one, but not both at the same time.

        """
        return self._search_operation('GET', query_body=query_body,
                query_string_args=query_string_args, indexes=indexes,
                doctypes=doctypes)


    def delete_by_query(self, query_body=None, query_string_args=None,
                indexes=["_all"], doctypes=[]):
        """Delete based on a search operation.

        Searching in ElasticSearch can be done in two ways:
        1) with a query string, by providing query_args
        2) using a full query body (JSON) by providing
        the query_body.
        You can choose one, but not both at the same time.

        """
        return self._search_operation('DELETE', query_body=query_body,
                query_string_args=query_string_args, indexes=indexes,
                doctypes=doctypes, operation_type='_query')

    def count(self, query_body=None, query_string_args=None,
                indexes=["_all"], doctypes=[]):
        """Count based on a search operation. The query is optional, and when
        not provided, it will use match_all to count all the docs.

        Searching in ElasticSearch can be done in two ways:
        1) with a query string, by providing query_args
        2) using a full query body (JSON) by providing
        the query_body.
        You can choose one, but not both at the same time.

        """
        return self._search_operation('GET', query_body=query_body,
                query_string_args=query_string_args, indexes=indexes,
                doctypes=doctypes, operation_type='_count')

    def get(self, index, doctype, docid, fields=None):
        """Get document from the index.

        You need to supply an index, doctype and id. Optionally, you can
        list the fields that you want to retrieve, e.g.:
        fields=['name','address']

        """
        args = dict()
        if fields:
            fields = ",".join(fields)
            args['fields'] = fields

        path = self._make_path([index, doctype, docid])
        self.send_request('GET', path, query_string_args=args)
        return json.loads(self.last_response.text)

    def mget(self, index, doctype, ids, fields=None):
        """Perform a multi get. Although ElasticSearch supports it, this
        method does not allow you to specify fields per id. You can only
        specify the fields to retrieve once and this will be applied to
        all ids that are fetched.
        Similarly, you can not specify an index and different doctypes. If
        you need too, you should do a direct call with send_request instead.

        """
        path = self._make_path([index, doctype, '_mget'])
        docs = []
        for id in ids:
            doc = {'_id': id}
            if fields:
                doc['fields'] = fields
            docs.append(doc)
        body = {'docs': docs}
        self.send_request('GET', path, body=body)
        return json.loads(self.last_response.text)

    def delete(self, index, doctype, id):
        """Delete document from index.

        Returns true if the document was found and false otherwise.

        """
        path = self._make_path([index, doctype, id])
        self.send_request('DELETE', path)
        resp = json.loads(self.last_response.text)
        return resp['found']

    """
    Indices API
    """
    def create_index(self, index, body):
        """Create an index.

        You have to supply the optional settings and mapping yourself.

        """
        path = self._make_path([index])
        self.send_request('PUT', path, body=body)
        resp = json.loads(self.last_response.text)
        return self.check_result(resp, 'acknowledged', True)

    def delete_index(self, index):
        """Delete an entire index.

        Returns true if the index was deleted and false otherwise.

        """
        path = self._make_path([index])
        self.send_request('DELETE', path)
        resp = json.loads(self.last_response.text)
        return self.check_result(resp, 'acknowledged', True)

    def refresh(self, index):
        """Refresh index.

        Returns True on success, false otherwise.

        """
        path = self._make_path([index, '_refresh'])
        self.send_request('POST', path)
        resp = json.loads(self.last_response.text)
        return self.check_result(resp, 'ok', True)

    def aliases(self, alias, indexes):
        """Create an alias for one or more indexes
        
        Arguments:
        alias -- the alias name
        indexes -- a list of indexes that this alias spans over
        
        """
        query = []
        for index in indexes:
            query

    def open_index(self, index):
        """Open a closed index.
        
        Opening a closed index will make that index go through the normal
        recover process.
        
        Returns True on success, False of failure.
        
        """
        path = self._make_path([index, '_open'])
        self.send_request('POST', path)
        resp = json.loads(self.last_response.text)
        return self.check_result(resp, 'ok', True)
        
    def close_index(self, index):
        """Close an index. A closed index has almost no overhead on the
        cluster except for maintaining its metadata. A closed index is
        blocked for reading and writing.
        
        Returns True on success, False of failure.
        """
        path = self._make_path([index, '_close'])
        self.send_request('POST', path)
        resp = json.loads(self.last_response.text)
        return self.check_result(resp, 'ok', True)

if __name__ == '__main__':
    print "This is a library, it is not intended to be started by itself."

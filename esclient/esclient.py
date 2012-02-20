import requests
from urllib import urlencode
from pprint import pprint
try:
    import simplejson as json
except:
    import json

class ESClientException(Exception):
    pass

class ESClient:
    """
    This is the most basic ElasticSearch client possible. It leaves much of
    the work to you as a developer but it will take care of doing proper
    HTTP requests.
    There will also be a number of helper methods that you can optionally use
    to make life easier.
    """
    def __init__(self, es_url, es_timeout=10):
        self.es_url = es_url
        self.es_timeout = es_timeout

        if self.es_url.endswith('/'):
            self.es_url = self.es_url[:-1]

    """
    Helper methods
    """

    def _make_path(self, path_components):
        """
        Smush together the path components. Empty components will be ignored.
        """
        path_components = [str(component) for component
                            in path_components if component]
        path = '/'.join(path_components)
        if not path.startswith('/'):
            path = '/'+path
        return path

    def send_request(self, method, path, body="", query_string_args={}):
        """
        Make a raw HTTP request to ElasticSearch.

        You may use this method to manually do whatever is not (yet) supported
        by this ElasticSearch client. This method does not return anything,
        but sets the class variable called last_response, with is te response
        object returned by the requests library.
        """
        if query_string_args:
            path = "?".join([path, urlencode(query_string_args)])

        kwargs = { 'timeout': self.es_timeout }
        url = self.es_url + path

        if body:
            kwargs['data'] = body

        if not hasattr(requests, method.lower()):
            raise ESClientException("No such HTTP Method '%s'!" %
                                    method.upper())

        req_method = getattr(requests, method.lower())
        self.last_response = req_method(url, **kwargs)
        resp_code = self.last_response.status_code
        print "HTTP response from url %s: %s" % (url, resp_code)


    def _search_operation(self, request_type, query_body=None,
                    operation_type="_search", query_string_args=None,
                    indexes=["_all"], doctypes=[]):
        """
        Perform a search operation. This method can be use for search,
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
            """ ES docs says you can use POST here too """
            self.send_request('GET', path, body=query_body)
            return json.loads(self.last_response.text)

        elif query_string_args:
            self.send_request('GET', path, query_string_args=query_string_args)
            return json.loads(self.last_response.text)
        elif operation_type == "_count":
            """
            A query is optional when counting, so we fire a request
            to the URL without a query only in this specific case.
            """
            self.send_request('GET', path)
            return json.loads(self.last_response.text)
        else:
            raise ESClientException("No query body or query arguments")
    """
    The API methods
    """
    def index(self, index, doctype, body, docid=None, op_type=None):
        """
        Index the supplied document.

        Options:
        index -- the index name (e.g. twitter)
        doctype -- the document types (e.g. tweet)
        op_type -- "create" or None:
            "create": create document only if it does not exists already
            None: create document or update an existing document

        Returns True on success (document added/updated or already exists
        while using op_type="create") or False in all other instances
        """
        args = dict()
        if op_type:
            args["op_type"] = op_type
        path = self._make_path([index, doctype, docid])
        self.send_request('POST', path, body=body, query_string_args=args)
        rescode = self.last_response.status_code
        if rescode == 200:
            return True
        elif rescode == 409 and op_type=="create":
            """ If document already exists, ES returns 409 """
            return True
        else:
            """ TODO: do some debug loggin """
            return False

    def search(self, query_body=None, query_string_args=None,
                indexes=["_all"], doctypes=[]):
        """
        Perform a search operation.

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
        """
        Delete based on a search operation.

        Searching in ElasticSearch can be done in two ways:
        1) with a query string, by providing query_args
        2) using a full query body (JSON) by providing
        the query_body.
        You can choose one, but not both at the same time.
        """
        return self._search_operation('DELETE', query_body=query_body,
                query_string_args=query_string_args, indexes=indexes,
                doctypes=doctypes)

    def count(self, query_body=None, query_string_args=None,
                indexes=["_all"], doctypes=[]):
        """
        Count based on a search operation. The query is optional, and when
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

    def refresh(self, index):
        path = self._make_path([index, '_refresh'])
        self.send_request('POST', path)

    def get(self, index, docid, doctype="", fields=None):
        args = dict()
        if fields:
            fields = ",".join(fields)
            args['fields'] = fields

        path = self._make_path([index, doctype, docid])
        self.send_request('GET', path, query_string_args=args)
        return json.loads(self.last_response.text)

    def delete(self, index, doctype, id):
        path = self._make_path([index, doctype, id])
        self.send_request('DELETE', path)


if __name__ == '__main__':
    """ TODO: Run tests """
    pass

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
    def __init__(self, es_url, es_timeout=60):
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
        path_components = [str(component) for component in path_components if component]
        path = '/'.join(path_components)
        if not path.startswith('/'):
            path = '/'+path
        return path

    def send_request(self, method, path, body="", querystring_args={}):
        """
        Use the requests library to do an HTTP request.

        Returns the JSON document returned by ElasticSearch and parsed using
        json.loads() or False on error.
        You can inspect the response manually by accessing the last_response
        object.
        """
        if querystring_args:
            path = "?".join([path, urlencode(querystring_args)])

        kwargs = { 'timeout': self.es_timeout }
        url = self.es_url + path

        if body:
            kwargs['data'] = json.dumps(body)

        if not hasattr(requests, method.lower()):
            raise ESClientException("No such HTTP Method '%s'!" % method.upper())
        req_method = getattr(requests, method.lower())
        self.last_response = req_method(url, **kwargs)
        resp_code = self.last_response.status_code


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

        Returns True on success (document added/updated or already exists while
        using op_type="create") or False in all other instances
        """
        args = dict()
        if op_type:
            args["op_type"] = op_type
        path = self._make_path([index, doctype, docid])
        self.send_request('POST', path, body=body, querystring_args=args)
        rescode = self.last_response.status_code
        if rescode == 200:
            return True
        elif rescode == 409 and op_type=="create":
            """ If document already exists, ES returns 409 """
            return True
        else:
            return False

    def refresh(self, index):
        path = self._make_path([index, '_refresh'])
        return self.send_request('POST', path)

    def get(self, index, docid, doctype="", fields=None):
        args = dict()
        if fields:
            fields = ",".join(fields)
            args['fields'] = fields

        path = self._make_path([index, doctype, docid])
        self.send_request('GET', path, querystring_args=args)
        return json.loads(self.last_response.text)
        
    def search(self, index, query):
        pass
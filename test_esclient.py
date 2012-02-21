from esclient import esclient
import unittest
from pprint import pprint

class TestESClient(unittest.TestCase):
    """Test all API methods implemented in esclient library"""

    def setUp(self):
        """Create an ESClient"""
        self.es = esclient.ESClient("http://localhost:9200/")

        """ Create a test schema once """
        # TODO
        
        """ Index some test data """
        data = {"name": "Joe Tester","age": 21, "sex": "male"}
        self.assertTrue(self.es.index("contacts", "person", body=data,
                        docid=1))
        data = {"name": "Joe Schmoe","age": 17, "sex": "male"}
        self.assertTrue(self.es.index("contacts", "person", body=data,
                                        docid=2))
        
        result = self.es.refresh('contacts')
        self.assertTrue(result['ok'])

    def tearDown(self):
        """docstring for tearDownClass"""
        
        """Delete a document"""
        result = self.es.send_request('DELETE', '/contacts/person/1')
        result = self.es.get('contacts', 'person', 1)
        self.assertFalse(result['exists'])
        """Delete the test schema"""
        # TODO
        pass


    def test_index_api(self):
        data = {"naam": "Jane Tester","age": 23, "sex": "female"}
        self.assertTrue(self.es.index("contacts", "person", body=data,
                        docid=3))
        """
        Again, now with op_type='create', meaning: only index when
        the document id does not exist yet
        """
        self.assertTrue(self.es.index("contacts", "person", body=data,
                        docid="3", op_type="create"))
        
        """ Ensure that the document has really been indexed """
        result = self.es.get('contacts', 'person', 3)
        self.assertTrue(result['exists'])

    def test_get_api(self):
        result = self.es.get('contacts', 'person', 1)
        self.assertTrue(result['exists'])

    def test_search_queryargs_api(self):
        """docstring for test_search_api"""
        query_string_args = {
                "q": "name:Joe",
                "sort":"age",
                "timeout":10,
                "fields": "id,age"
                }
        result = self.es.search(query_string_args=query_string_args)
        self.assertEqual(result['hits']['total'], 2)

    def test_search_body_api(self):
        """docstring for test_search_body_api"""
        query_body = {
            "query": {
               "term": {"name": "joe"}
            }
        }
        result = self.es.search(query_body=query_body)
        self.assertEqual(result['hits']['total'], 2)

    def test_count_api(self):
        """docstring for count_api"""
        result = self.es.count(indexes=['contacts'])
        """ We can be sure there are at least two docs indexed """
        self.assertTrue(result['count'] > 1)
        
    def test_deletebyquery_api(self):
        """docstring for test_deletebyquery_api"""
        pass
        
if __name__ == '__main__':
    unittest.main()
import esclient
import unittest
from pprint import pprint

class TestESClient(unittest.TestCase):
    """Test all API methods implemented in esclient library"""

    @classmethod
    def setUpClass(cls):
        """Create an ESClient"""
        cls.es = esclient.ESClient("http://localhost:9200/")

        """Delete the test schema, if any. This will prevent any errors
        due to the schema already existing """
        cls.es.delete_index("contacts_esclient_test")

    def setUp(self):
        """ Create a test schema once """
        body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        self.assertTrue(self.es.create_index('contacts_esclient_test', body))
        self.assertFalse(self.es.create_index('contacts_esclient_test', body))


        """ Index some test data """
        data = {"name": "Joe Tester","age": 21, "sex": "male"}
        self.assertTrue(self.es.index("contacts_esclient_test", "person", body=data,
                                        docid=1))
        data = {"name": "Joe Schmoe","age": 17, "sex": "male"}
        self.assertTrue(self.es.index("contacts_esclient_test", "person", body=data,
                                        docid=2))

        self.assertTrue(self.es.refresh('contacts_esclient_test'))

    def tearDown(self):
        """docstring for tearDownClass"""

        """Delete the test schema"""
        self.assertTrue(self.es.delete_index("contacts_esclient_test"))

    def test_index_api(self):
        data = {"name": "Jane Tester","age": 23, "sex": "female"}
        self.assertTrue(self.es.index("contacts_esclient_test", "person", body=data,
                        docid=3))
        """
        Again, now with op_type='create', meaning: only index when
        the document id does not exist yet
        """
        self.assertTrue(self.es.index("contacts_esclient_test", "person", body=data,
                        docid="3", op_type="create"))

        """ Ensure that the document has really been indexed """
        result = self.es.get('contacts_esclient_test', 'person', 3)
        self.assertTrue(result['exists'])

    def test_get_api(self):
        result = self.es.get('contacts_esclient_test', 'person', 1)
        self.assertTrue(result['exists'])

    def test_search_queryargs_api(self):
        """docstring for test_search_api"""
        query_string_args = {
                "q": "name:Joe",
                "sort":"age",
                "timeout":10,
                "fields": "id,name,age"
                }
        result = self.es.search(query_string_args=query_string_args,
                                indexes=['contacts_esclient_test'])
        self.assertEqual(result['hits']['total'], 2)

    def test_search_body_api(self):
        """docstring for test_search_body_api"""
        query_body = {
            "query": {
               "term": {"name": "joe"}
            }
        }
        result = self.es.search(query_body=query_body,
                                indexes=['contacts_esclient_test'])
        self.assertEqual(result['hits']['total'], 2)

    def test_deletebyquery_querystring_api(self):
        """Delete documents with a query using querystring option"""
        query_string_args = {
                "q": "name:Joe",
                "sort":"age",
                "timeout":10,
                "fields": "id,name,age"
                }
        result = self.es.delete_by_query(query_string_args=query_string_args,
                                         indexes=['contacts_esclient_test'])
        self.assertTrue(result['ok'])
        self.assertTrue(self.es.refresh('contacts_esclient_test'))
        result = self.es.get('contacts_esclient_test', 'person', 1)
        self.assertFalse(result['exists'])
        result = self.es.get('contacts_esclient_test', 'person', 1)
        self.assertFalse(result['exists'])

    def test_deletebyquery_body_api(self):
        """Delete documents with a query in a HTTP body"""
        query_body = { "term": {"name": "joe"}}
        result = self.es.delete_by_query(query_body=query_body,
                                indexes=['contacts_esclient_test'],
                                doctypes=['person'])
        self.assertTrue(result['ok'])
        self.assertTrue(self.es.refresh('contacts_esclient_test'))
        result = self.es.get('contacts_esclient_test', 'person', 1)
        self.assertFalse(result['exists'])
        result = self.es.get('contacts_esclient_test', 'person', 1)
        self.assertFalse(result['exists'])

    def test_count_api(self):
        """docstring for count_api"""
        result = self.es.count(indexes=['contacts_esclient_test'])
        """ We can be sure there are at least two docs indexed """
        self.assertTrue(result['count'] > 1)

    def test_delete_api(self):
        """Delete a document"""
        result = self.es.delete('contacts_esclient_test', 'person', 1)
        result = self.es.get('contacts_esclient_test', 'person', 1)
        self.assertFalse(result['exists'])

if __name__ == '__main__':
    unittest.main()

import esclient
import unittest

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
        self.assertTrue(self.es.create_index('contacts_esclient_test2', body))


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

        """Delete the test schemas"""
        self.assertTrue(self.es.delete_index("contacts_esclient_test"))
        self.assertTrue(self.es.delete_index("contacts_esclient_test2"))

    def test_open_close_index(self):
        """docstring for test_open_index"""
        self.assertTrue(self.es.close_index('contacts_esclient_test'))
        self.assertTrue(self.es.open_index('contacts_esclient_test'))

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

    def test_mget_api(self):
        """docstring for test_mget_api"""
        result = self.es.mget('contacts_esclient_test', 'person',
                              ids=[1,2], fields=['name','age'])

        for doc in result['docs']:
            self.assertTrue(doc['_id'] == '1' or  doc['_id'] == '2')

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

    def test_create_delete_alias_api(self):
        self.es.create_alias('contacts_alias', ['contacts_esclient_test',
                                                'contacts_esclient_test2'])
        self.es.delete_alias('contacts_alias', ['contacts_esclient_test',
                                                'contacts_esclient_test2'])
    def test_status(self):
        """docstring for test_status"""
        result = self.es.status(indexes=['contacts_esclient_test'])
        self.assertTrue(result['ok'])

    def test_flush(self):
        """docstring for test_flush"""
        self.assertTrue(self.es.flush(['contacts_esclient_test'], refresh=True))

    def test_get_mapping(self):
        """docstring for test_get_mapping"""
        m = self.es.get_mapping(indexes=['contacts_esclient_test'])
        self.assertIn("contacts_esclient_test", m)

    def test_put_mapping(self):
        """docstring for test_put_mapping"""
        mapping = {'persons': {'properties':{'name': {'type': 'string'}}}}
        result = self.es.put_mapping(doctype='person', mapping=mapping, indexes=['contacts_esclient_test', 'contacts_esclient_test2'])
        self.assertTrue(result['ok'])

    def test_index_exists(self):
        result = self.es.index_exists("contacts_esclient_test")
        self.assertTrue(result)

    def test_bulk(self):
        self.es.bulk_index('contacts_esclient_test', 'bulk', {'test':'test'}, 1)
        self.es.bulk_index('contacts_esclient_test', 'bulk', {'test':'test'}, 2)
        self.assertTrue(self.es.bulk_push())
        result = self.es.get('contacts_esclient_test', 'bulk', 2)
        self.assertTrue(result['exists'])
        self.es.bulk_index('contacts_esclient_test', 'bulk', {'test':'test'}, 3)
        self.es.bulk_delete('contacts_esclient_test', 'bulk', 2)
        self.assertTrue(self.es.bulk_push())
        result = self.es.get('contacts_esclient_test', 'bulk', 2)
        self.assertFalse(result['exists'])
        result = self.es.get('contacts_esclient_test', 'bulk', 3)
        self.assertTrue(result['exists'])

if __name__ == '__main__':
    unittest.main()

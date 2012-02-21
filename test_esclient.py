from esclient import esclient
import unittest

class TestESClient(unittest.TestCase):
    """Test all API methods implemented in esclient library"""

    @classmethod
    def setUpClass(self):
        """Create an ESClient once"""
        self.es = esclient.ESClient("http://localhost:9200/")

        """ Create a test schema once """
        # TODO

    @classmethod    
    def tearDownClass(self):
        """docstring for tearDownClass"""
        
        """Delete the test schema"""
        # TODO
        pass


    def test_index_api(self):
        data = {"name": "Joe Tester","age": 21, "sex": "male"}
        self.assertTrue(self.es.index("contacts", "person", body=data, docid=1))
        
    
    def test_get_api(self):
        pass
        
    def test_delete_api(self):
        pass
    
    def test_search_api(self):
        """docstring for test_search_api"""
        pass
        
    def test_deletebyquery_api(self):
        """docstring for test_deletebyquery_api"""
        pass
        
if __name__ == '__main__':
    unittest.main()
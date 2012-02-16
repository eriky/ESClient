from esclient import esclient
from pprint import pprint

# Connect
es = esclient.ESClient("http://localhost:9200/", es_timeout=10)

# Index API
data = {"name": "Joe Tester","age": 21}
print "Insert doc id 1"
result = es.index("contacts", "person", body=data, docid=1)
pprint(result)
es.refresh("contacts")

data = {"name": "Jane Tester","age": 23, "sex": "female"}
print "Insert doc id 2"
es.index("contacts", "person", body=data, docid=2)
pprint(result)
es.refresh("contacts")

data = {"name": "Jane Tester","age": 23, "sex": "female"}
print "Insert doc id 2 again with op_type = create"
es.index("contacts", "person", body=data, docid="2", op_type="create")
pprint(result)
es.refresh("contacts")

# Get API
print "Get doc id 1"
result = es.send_request('GET', '/contacts/person/1')
pprint(result)
es.refresh("contacts")

# DELETE API
print "Delete doc id 1"
result = es.send_request('DELETE', '/contacts/person/1')
pprint(result)
es.refresh("contacts")

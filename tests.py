from esclient import esclient
from pprint import pprint

# Connect
es = esclient.ESClient("http://localhost:9200/", es_timeout=10)

# Index API
data = {"naam": "Joe Tester","age": 21, "sex": "male"}
print "Insert doc id 1"
if not es.index("contacts", "person", body=data, docid=1):
    print "[Test failed] Error while adding document"

data = {"naam": "Jane Tester","age": 23, "sex": "female"}
print "Insert doc id 2"
if not es.index("contacts", "person", body=data, docid=2):
    print "[Test failed] Error while adding document"

print "Insert doc id 2 again with op_type = create"
if not es.index("contacts", "person", body=data, docid="2", op_type="create"):
    print "[Test failed] Error while adding document"

data = {"naam": "Joe Schmoe","age": 17, "sex": "male"}
print "Insert doc id 4"
if not es.index("contacts", "person", body=data, docid=4):
    print "[Test failed] Error while adding document"

es.refresh("contacts")

# Get API
print "Get doc id 1"
result = es.get('contacts', 1, 'person')
pprint(result)

# Search API
print "Search for name:Joe in all indexes and all doctypes, using query args"
query_string_args = {
        "q": "naam:Joe",
        "sort":"age",
        "timeout":10,
        "fields": "id,age"
        }
result = es.search(query_string_args=query_string_args)
pprint(result)

print "Search for name:Joe in all indexes and all doctypes, using a JSON query"
query_body = """
{
    "query": {
       "term": {"naam": "joe"}
    }
}
"""
result = es.search(query_body=query_body)
pprint(result)

# COUNT API
print "Doing a count on all items in our contacts index"
result = es.count(indexes=['contacts'])
pprint(result)
# DELETE API
print "Delete doc id 1"
#result = es.send_request('DELETE', '/contacts/person/1')
es.refresh("contacts")

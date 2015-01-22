from flask import Flask, request, json
from pymongo import MongoClient
from bson.json_util import dumps
# from elasticsearch import Elasticsearch

app = Flask(__name__)
client = MongoClient('localhost', 27017)
# es = Elasticsearch({'host': 'localhost', 'port': 9200})
db = client.test.spaceObjects

MONGO_COMPARATORS = ['gt', 'gte', 'in', 'lt', 'lte', 'ne', 'nin']


# converts values into numbers if applicable
def parse(val):
	try:
		return float(val)
	except Exception:
		return val


# decorate query for mongodb
def transform_query(q):
	for comparator in MONGO_COMPARATORS:
		if comparator in q:
			key = '${}'.format(comparator)
			val = q.split(comparator)[1]
			return {key: parse(val)}
	return q


@app.route('/', methods=['GET'])
def search():
	# Converts (request.args)ImmutableDict to dict
	query_dict = json.loads(json.dumps(request.args))
	object_types = query_dict.get('types')

	if object_types:
		object_types = object_types.split()
		
		if len(object_types) > 1:
			query_dict['types'] = {'$in': object_types}
	
	for key in query_dict:
		query_dict[key] = transform_query(query_dict.get(key))

	print 'Query: {}'.format(query_dict)
	print 'Results:'
	obj_list = []
	for item in db.find(query_dict):
		obj_list.append(item)
		print item

	return dumps({'results': obj_list})


# trying out mongodb's full text search
@app.route('/fts/<string:query>', methods=['GET'])
def fts_search(query):
	query.replace('galaxies', 'galaxy')
	query.replace('stars', 'star')
	query.replace('interstellar matter', 'interstellar_matter')

	print 'Full Text Search:'
	obj_list = []
	for item in db.find({'$text': { '$search': query }}):
		obj_list.append(item)
		print item
	return dumps({'results': obj_list})


if __name__ == '__main__':
    app.run(debug=True)
README
-------------
SkyWatch Co-op Technical Challenge

*search.py*

Contains the logic for converting a string to the correct query string for the API. Assumes that a search query will be structured in one of the following ways:
1. <object types> with <physical criteria>
2. <object types>
3. <physical criteria>

Multiple items are assumed to be delimited by commas and the word 'and'.

Algorithm:

1. Resolve plurals to singular.
2. Attempt to split the query by with keyword
3. Determine if the query has both object types and physical criteria or not, and if the with keyword was used.
4. If the with keyword is not used, everything must be tokenized by commas and categorized, takes O(N*M) where N is number of tokens, and M is number of unique objects to check for.
5. For each part of the query, further split the string into tokens delimited by ',' or 'and'.
6. For physical criteria, convert comparator symbols to the correct comparator strings (a la mongodb docs) while only removing whitespace between the comparator and operands.

*api.py*

A flask application that would mimic SkyWatch's backend and convert the request to a mongodb query. There are two endpoints. The first simply converts the query string structured in the form above to a mongodb query. The second uses MongoDB's full text search on the query string. This requires a text index on all the relevant fields to be searched.

Example:

```python
db.collection.ensureIndex({
	<field_name_here>: "text"
})
```

This would allow for searching by name, but it wouldn't be able to search by value. For example, 'galaxies and stars with redshift greater than 2' would return all items that have type galaxy or star and has a redshift field, but it wouldn't be able to figure out how to use comparators.

As for flexibility and performance, each text index should probably be weighted based on how trends of how people use the API. For more advanced search features (such as fuzzy-searching or natural language such as above), it would probably be good to use a search platform such as Solr, Sphinx or Elasticsearch with data being streamed in from mongodb.

Need to Install:

1. MongoDB 2.6 for Full Text Search
2. pymongo (bson comes with this)
3. Flask

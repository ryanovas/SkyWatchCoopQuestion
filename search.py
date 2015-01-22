CMP_SYM = ['>=', '<=', '!=', '=', '>', '<']
CMP_STR = ['=gte', '=lte', '=ne', '=', '=gt', '=lt']
OBJECT_TYPES = ['star', 'galaxy', 'interstellar_matter']
PHYSICAL_CRITERIA = ['vmag', 'redshift', 'plx', 'mes']
BASE_URL = 'http://api.skywatch.co/?'


# just an enum
class CriteriaType():
	ObjectType, PhysCriteria = range(2)
 

# converts comparators to text suitable for api
def cmp_helper(q):

	for i in range(len(CMP_SYM)):
		if CMP_SYM[i] in q:
			q = q.split(CMP_SYM[i])
			cmp_string = q[0] + CMP_STR[i] + q[1]
			return cmp_string


# will generate the api query string for
# object type or physical criteria queries
def gen_criteria_string(c_list, index, c_type):

	c_string = ""

	# fix whitespace issues
	items = map(lambda x: x.strip(), c_list[index].split(','))

	if c_type == CriteriaType.ObjectType:
		c_string += "types="
		for item in items:
			c_string += item + '+'
	elif c_type == CriteriaType.PhysCriteria:
		items = map(lambda x: x.strip(), c_list[index].split(','))
		for item in items:
			c_string += cmp_helper(item.replace(' ', '')) + '&'
	
	return c_string[:-1]


# converts a search query to the correct api endpoint call
def query_to_api(q):

	# convert plural to singular
	q = q.replace('stars', 'star')
	q = q.replace('galaxies', 'galaxy')
	q = q.replace('interstellar matter', 'interstellar_matter')

	# try to split data into the two components
	data = q.replace(' and ', ',').split(' with ')
	data_len = len(data)
	full_string = BASE_URL
	flag_obj, flag_pc = 0, 0  # determines which type of query was found

	# determine type of query
	for o in OBJECT_TYPES:
		if o in data[0]:
			flag_obj = 1
			break

	for pc in PHYSICAL_CRITERIA:
		if pc in data[0]:
			flag_pc = 1
			break

	if flag_obj == 1:
		# for bonus (no with keyword), tokenize everything, O(N^2)
		if flag_pc == 1:
			items = data[0].split(',')
			obj_types, phys_crit = '', ''

			for item in items:
				for o in OBJECT_TYPES:
					if o in item:
						obj_types += item + ','
						break

				for pc in PHYSICAL_CRITERIA:
					if pc in item:
						phys_crit += item + ','
						break

			full_string += gen_criteria_string([obj_types[:-1]], 0, CriteriaType.ObjectType)
			full_string += '&'
			full_string += gen_criteria_string([phys_crit[:-1]], 0, CriteriaType.PhysCriteria)

		# can be singular or compound
		else:
			full_string += gen_criteria_string(data, 0, CriteriaType.ObjectType)

			# is it compound?
			if data_len > 1:
				full_string += '&' + gen_criteria_string(data, 1, CriteriaType.PhysCriteria)

	# must be singular
	else:
		full_string += gen_criteria_string(data, 0, CriteriaType.PhysCriteria)

	return full_string


# Tests
assert query_to_api("stars with vmag > 0") == 'http://api.skywatch.co/?types=star&vmag=gt0'
assert query_to_api("stars, galaxies and interstellar matter") == 'http://api.skywatch.co/?types=star+galaxy+interstellar_matter'
assert query_to_api("galaxies with redshift > 0.001, plx < 1 and mes = jpl+flux_v") == 'http://api.skywatch.co/?types=galaxy&redshift=gt0.001&plx=lt1&mes=jpl+flux_v'
assert query_to_api("stars, redshift > 0.001, galaxies") == 'http://api.skywatch.co/?types=star+galaxy&redshift=gt0.001'
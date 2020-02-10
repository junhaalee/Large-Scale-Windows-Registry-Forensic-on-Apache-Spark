from pyspark import SparkContext
import json

'''
Structure

1. QueryKey
	Input : Key
	Output : # of subkeys / value pairs

2. QueryValue
	Input : Key, value name
	Output : value data

3. EnumKey
	Input : Key
	Output : subkeys

4. EnumValue
	Input : Key
	Output : value pairs

'''


def openkey(key):

	sc = SparkContext()
	
	#Requires Modification
	sample = sc.wholeTextFiles('/user/cloudera/test')

	sample_json = sample.map(lambda (fname, x) : json.loads(x))
	
	#Requires Modification
	data = sample_json.take(1)[0]

	keys = key.split("\\")

	for key in keys:
		data = data[key]

	return data

# two querykey methods
def querykey_subkey(key):

	subkey = []

	for k in key:
		if type(key[k]) == dict:
			subkey.append(k)

	num_of_subkeys = len(subkey)

	return num_of_subkeys


def querykey_value(key):

	value_pairs = []

	for k in key:
		if type(key[k]) == unicode:
			value_pairs.append({k:key[k]})

	return value_pairs


def queryvalue(key,value_name):

	value_data = key[value_name]

	return value_data


def enumkey(key):

	subkey = []

	for k in key:
		if type(key[k]) == dict:
			subkey.append(k)

	return subkey


def enumvalue(key):

	value_pairs = []

	for k in key:
		if type(key[k]) == unicode:
			value_pairs.append({k:key[k]})

	return value_pairs


def keyword_search(keyword,data,loc,result):

	keys = list(data.keys())

	for key in keys:

		if type(data[key]) == unicode:
			if keyword in data[key]:
				if len(loc) >= 1:
					result.append({loc+'\\'+key : data[key]})
				else:
					result.append({key : data[key]})

		else:
			if len(loc) >= 1:
				keyword_search(keyword,data[key],loc+'\\'+key,result)
			else:
				keyword_search(keyword,data[key],key,result)
	
	return result




if __name__ == "__main__":
	
	key = 'HKEY_CLASSES_ROOT\\*'
	value_name = 'ConflictPrompt'

	#openkey -> querykey
	#print(querykey_subkey(openkey(key)))
	#print(querykey_value(openkey(key)))

	#openkey -> queryvalue
	#print(queryvalue(openkey(key),value_name))

	#openkey -> enumkey
	#print(enumkey(openkey(key)))

	#openkey -> enumvalue
	#print(enumvalue(openkey(key)))

	

	#test keyword search
	sc = SparkContext()
	sample = sc.wholeTextFiles('/user/cloudera/test')
	sample_json = sample.map(lambda (fname, x) : json.loads(x))
	data = sample_json.take(1)[0]

	result = keyword_search('image',data,'',[])

	for res in result:
		print(res)

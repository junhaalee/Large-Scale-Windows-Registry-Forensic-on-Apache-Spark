from pyspark import SparkContext
import time


#Pre-Processing
def multi2single(data):

	sample = data.collect()[2:]
	
	ind = 0
	while(True):
		if ind == len(sample):
			break
		if len(sample[ind]) >= 1 and str(sample[ind])[-1] == '\\':
			sample[ind] = sample[ind][:-1]+sample[ind+1][2:]
			del sample[ind+1]
		else:
			ind += 1

	return sample



#Pre-Processing
def mk_unit(data):

	sample = multi2single(data)

	data = []

	ind = 0
	while(True):
		if ind >= len(sample):
			break
		if len(sample[ind]) != 0 and str(sample[ind])[0] == '[':
			temp = []
			k = ind
			while(True):
				if k >= len(sample) or len(sample[k]) == 0:
					break
				else:
					temp.append(str(sample[k]))
					k += 1
			data.append(temp)
			ind = k+1
		else:
			ind += 1

	result = []

	for d in data:
		if len(d) == 1:
			result.append(d[0][1:-1])
		else:
			for ind in range(1, len(d)):
				result.append(d[0][1:-1]+'\\'+d[ind])

	return result



#save as key-value
def reg2dict(data):

	if '=' in data:
		value_name = 'default' if data.split('=')[0].split('\\')[-1] == '@' else data.split('=')[0].split('\\')[-1][1:-1]
		value_data = data.split('=')[1] if str(data.split('=')[1])[0] != '"' else data.split('=')[1][1:-1]
		values = [{value_name : value_data}]
		keys = data.split('=')[0].split('\\')[:-1]
	else:
		values = [{}]
		keys = data.split('\\')
	
	key_value = keys+values

	for i in range(len(key_value)-2,-1,-1):
		key_value[i] = { key_value[i] : key_value[i+1] }

	return key_value[0]



		

#reduce
def dict_reduce(x,y):

	keys = []
	
	check = 0

	while(True):
		if x.values()[0].keys() != y.values()[0].keys():
			keys.append(x.keys()[0])
			if y.values()[0].keys()[0] in x.values()[0].keys():
				check = 1
			break
		else:
			keys.append(x.keys()[0])
			x = x.values()[0]
			y = y.values()[0]

	if check == 1:
		x.values()[0][y.values()[0].keys()[0]].update(y.values()[0].values()[0])
	else:
		x.values()[0].update(y.values()[0])

	result = x.values()[0]

	for ind in range(len(keys)-1,-1,-1):

		result = {keys[ind] : result}

	return result

	

#keyword search

def search(keyword,data,loc,result):

       keys = list(data.keys())

       for key in keys:

       	if type(data[key]) == str:
                       if keyword in data[key]:
                               if len(loc) >= 1:
                                       result.append({loc+'\\'+key :
data[key]})
                               else:
                                       result.append({key : data[key]})

               else:
                       if len(loc) >= 1:
                               search(keyword,data[key],loc+'\\'+key,result)
                       else:
                               search(keyword,data[key],key,result)

       return result


if __name__ == "__main__":

	sc = SparkContext()

	

	partition_size = 20

	temp_data = sc.textFile('/user/cloudera/sample/sample.reg').repartition(partition_size)

	
	data = sc.parallelize(mk_unit(temp_data)).flatMap(lambda x : x.split('/n')).map(lambda x : reg2dict(x)).reduce(lambda x,y : dict_reduce(x,y))


	start_time = time.time()

	search('sys',data,'',[])

	finish_time = time.time()
	
	print("time : "+str(finish_time - start_time))
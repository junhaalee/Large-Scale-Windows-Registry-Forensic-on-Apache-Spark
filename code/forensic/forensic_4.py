from pyspark import SparkContext
import time



#Pre-Processing - multi line value
def multi2single(path):

	data = sc.textFile(path).collect()[:]

	temp = []

	for d in data:

		if len(d) > 1:
			try:
				temp.append(str(d).replace('\x00',''))
			except:
				temp.append(str(d.encode('utf8')).replace('\x00',''))
	
	ind = 0
	while(True):
		if ind == len(temp):
			break
		if len(temp[ind]) >= 1 and str(temp[ind])[-1] == '\\':
			temp[ind] = temp[ind][:-1]+temp[ind+1][2:]
			del temp[ind+1]
		else:
			ind += 1

	return temp



#Pre-Processing
def mk_unit(path):

	sample = multi2single(path)

	data = []

	ind = 0
	while(True):

		if ind >= len(sample):
			break

		if str(sample[ind])[0] == '[':

			temp = [str(sample[ind])]
			k = ind+1

			while(True):
				if k >= len(sample) or sample[k][0] == '[':
					break
				else:
					temp.append(str(sample[k]))
					k += 1
			
			data.append(temp)
			ind = k
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
		
		if str(data.split('=')[1])[0] != '"':
			value_data = data.split('=')[1]
		elif data.split('=')[1] == '""':
			value_data = 'none'
		else:
			value_data = data.split('=')[1][1:-1]
		values = [{value_name : value_data}]
		keys = data.split('=')[0].split('\\')[:-1]
	else:
		values = ['none']
		keys = data.split('\\')
	
	key_value = keys+values

	for i in range(len(key_value)-2,-1,-1):
		key_value[i] = { key_value[i] : key_value[i+1] }

	return key_value[0]


def forensic(ex_data,data,result):

	klist, value = [], ''

	temp = data

	while(True):
		if len(temp.values()) > 0 :
			if type(temp.values()[0]) != dict:
				klist.append(temp.keys()[0])
				value = temp.values()[0]
				break

			klist.append(temp.keys()[0])
			temp = temp.values()[0]
		else:
			break
	
	ind = 0
	ex = ex_data
	check = True

	#key
	while(True):
	
		if ind == len(klist):
			break
	
		if klist[ind] in ex.keys():
			ex = ex[klist[ind]]
		else:
			result = 'key : '+str(data)
			check = False

		ind += 1

	#value
	if check:
		try:
			ex = eval(str(ex))
			if not ex.keys() and not ex.values():
				if value != ex:
					result = 'value : '+str(data)
		except:
			if value != ex:
				result = 'value : '+str(data)
	return result


if __name__ == "__main__":

	ex_reg_path = 'gs://dataproc-temp-asia-east1-804846661812-lspxomee/old.json'
	new_reg_path = 'gs://dataproc-temp-asia-east1-804846661812-lspxomee/new.reg'
	partition_num = 4
	sc = SparkContext()

	#old data
	data = sc.textFile(ex_reg_path).map(lambda x : eval(x)).collect()[0]
	old_data = {data.keys()[1]:data.values()[1]}

	#new data
	# new_data = sc.parallelize(mk_unit(new_reg_path)).flatMap(lambda x : x.split('/n')).map(lambda x : reg2dict(x))
	# new_data.saveAsTextFile('gs://dataproc-temp-asia-east1-804846661812-lspxomee/new')

	start_time = time.time()

	forensic_data = sc.textFile('gs://dataproc-temp-asia-east1-804846661812-lspxomee/new/part-00000').repartition(partition_num).flatMap(lambda x : x.split('/n')).map(lambda x : eval(x)).map(lambda x : forensic(old_data,x,''))

	finish_time = time.time()

	print("Number of Partition : "+str(forensic_data.getNumPartitions())+"    Time : "+str(finish_time - start_time))


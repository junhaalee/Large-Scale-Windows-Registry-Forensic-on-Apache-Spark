import json
import time
import multiprocessing


def openkey(key):

    with open('/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data/sample.json') as json_file: 
        data = json.load(json_file) 

    keys = key.split('\\')

    for key in keys:
        data = data[key]

    return data



def querykey(key):

    subkey = []
    value_pairs = []

    for k in key:
        if type(key[k]) == dict:
            subkey.append(k)
        elif type(key[k]) == str:
            value_pairs.append({k:key[k]})
    
    num_of_subkeys = len(subkey)

    return num_of_subkeys, value_pairs



def queryvalue(key, value_name):

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
        if type(key[k]) == str:
            value_pairs.append({k:key[k]})

    return value_pairs



def mkunit(path):

    f = open(path, 'r')

    # 첫째 줄에 있는 data는 사용X    
    with open(path, 'r', encoding='utf-16') as f:
        data = f.read().split("\n\n")[1:]

    result = []
    for sample in data:
        temp = multi2single(sample)
        result.append(temp)

    #key-value_name-value_data 묶어주기
    data = []
    ind = 0
    while(True):
        if ind >= len(result):
            break
        if len(result[ind]) != 0 :
            temp = []
            k = ind
            while(True):
                if k >= len(result) or len(result[k]) == 0:
                    break
                else:
                    temp.append(result[k])
                    k+=1
            data += temp
            ind = k+1
        else:
            ind += 1
    
    #key-value single-line으로 묶어주기
    result = []
    for d in data:
        if len(d) == 1:
            result.append(d[0][1:-1])
        else:
            for ind in range(1, len(d)):
                result.append(d[0][1:-1]+'\\'+d[ind])
    
    return result


def multi2single(sample):

    sample = sample.split('\n')

    ind = 0
    while(True):
        if ind == len(sample):
            break
        if sample[ind].endswith('\\'):
            sample[ind] = sample[ind][:-1]+sample[ind+1][2:]
            del sample[ind+1]
        else:
            ind += 1
            
    return sample


'''
def keyword_search(keyword,data,loc,result):

    keys = list(data.keys())

    for key in keys:

        if type(data[key]) == str:
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
'''


def keyword_search(temp):
    keyword = 'sys'
    result = []
    for t in temp:
        if keyword in t:
            result.append(t)




if __name__ == "__main__":
    
    path = "/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data/registry.reg"
    result = mkunit(path)

    n = int(input())

    reg_list = []
    size = len(result)//n

    i = 0
    while(True):
        if len(reg_list) == n-1:
            reg_list.append(result[i:])
            break
        else:
            reg_list.append(result[i:i+size])
            i += size
    

    for _ in range(10):
        pool = multiprocessing.Pool(processes=n)

        start_time = time.time()
        
        pool.map(keyword_search,reg_list)    
        
        finish_time = time.time()

        pool.close()
        pool.join()

        print(finish_time-start_time)





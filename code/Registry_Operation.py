import json
import time


'''
Structure

1.	QueryKey
    Input : Key
    Output : # of subkeys / value pairs

2.	QueryValue - Done
    Input : Key, Value name
    Output : Value data

3.	EnumKey
    Input : Key
    Output : subkeys

4.	EnumValue
    Input : Key
    Output : value pairs
'''


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



if __name__ == "__main__":
    
    start_time = time.time()

    #setting
    key = ''
    value_name = ''

    # #openkey -> querykey
    # print(querykey(openkey(key))[0])
    # print(querykey(openkey(key))[1])

    # #openkey -> queryvalue -> closekey
    # print(queryvalue(openkey(key), value_name))

    # #openkey -> enumkey
    # print(enumkey(openkey(key)))

    # #openkey -> enumvalue
    # print(enumvalue(openkey(key)))

    #keyword search
    with open('/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data/HKEY_LOCAL_MACHINE.json') as json_file: 
        data = json.load(json_file) 

    keywords = ['sys','exe','file']

    for keyword in keywords:
        keyword_search(keyword,data,'',[])

    #time
    finish_time = time.time()
    print("time : "+str(finish_time-start_time))

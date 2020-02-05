import json

'''
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

    with open('/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data/HKEY_CLASSES_ROOT.json') as json_file: 
        data = json.load(json_file) 

    keys = key.split('\\')

    for key in keys:
        data = data[key]

    return data


def queryvalue(data, value_name):

    value_data = data[value_name]

    return value_data


def querykey(data):

    return data

def enumkey(data):

    return data

def enumvalue(data):

    return data




value = queryvalue(openkey('HKEY_CLASSES_ROOT\\*'), 'ConflictPrompt')
print(value)
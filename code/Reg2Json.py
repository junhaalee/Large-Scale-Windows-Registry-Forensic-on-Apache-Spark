import os
import json

def list_files_subdir(destpath, ext):
    
    filelist = []
    
    for path, subdirs, files in os.walk(destpath):
        for filename in files:
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                if filename.endswith(ext):
                    filelist.append(f)
    return filelist

def save_value(values):

    value_pair = {}

    for value in values:

        if value.split('=')[0] == '@':
            value_name = 'default'
        else:
            value_name = value.split('=')[0][1:-1]

        if value.split('=')[1][1] == '"':
            value_data = value.split('=')[1][1:-1]
        else:
            value_data = value.split('=')[1][1:-1]

        if len(value_data) == 0:
            pair = {value_name : ' '}
        else:
            pair = {value_name : value_data}

        value_pair.update(pair)

    return value_pair

def save_as_json(file_list,path):
        
    for file_name in file_list:

        reg = {}

        try:
            with open(file_name, 'r') as f:
                data = f.read().split("\n\n")[1:]
        except:
            with open(file_name, 'r', encoding='utf-16') as f:
                data = f.read().split("\n\n")[1:]

        for sample in data:

            keys = sample.split('\n')[0][1:-1].split('\\')

            try:
                values = sample.split('\n')[1:]
            except:
                pass
                
            for i in range(len(values)-1,0,-1):
                if '=' not in values[i]:
                    values[i-1] += values[i]
            
            ind = 0
            while(True):

                if ind == len(values):
                    break
                
                if '=' not in values[ind]:
                    del values[ind]
                else:
                    ind += 1

            temp = reg

            for key in keys :
                try:
                    if key not in list(temp.keys()):
                        if key == keys[-1]:
                            temp[key] = save_value(values)
                        else:
                            temp[key] = {}
                    else:
                        temp = temp[key]
                except:
                    print(keys)
        
        name = file_name.split('data/')[1].split('.')[0]

        with open(path+'/'+name+'.json','w') as towrite:
            json.dump(reg,towrite,ensure_ascii=False)

if __name__ == "__main__":
    path = '/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data'
    file_list = list_files_subdir(path,'reg')
    registry_json = save_as_json(file_list, path)


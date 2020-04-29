import os
import json
import io

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

        if value.split('=')[1][0] == '"':
            value_data = value.split('=')[1][1:-1]
        else:
            value_data = value.split('=')[1]

        if len(value_data) == 0:
            pair = {value_name : 'none'}
        else:
            pair = {value_name : value_data}

        value_pair.update(pair)

    return value_pair


def save_as_json(file_list,path):

    file_name = file_list[4]

    for file_name in file_list:

        reg = {}

        try:
            with io.open(file_name, 'r') as f:
                data = f.read().split("\n\n")[1:]
        except:
            with io.open(file_name, 'r', encoding='utf-16') as f:
                data = f.read().split("\n\n")[1:]

        sample = data[157]

        for sample in data:

            keys = map(str,sample.split('\n')[0][1:-1].split('\\'))

            try:
                values = map(str,sample.split('\n')[1:])
            except:
                pass
            
            #value_data가 여러줄에 걸쳐있는 경우 하나의 value_data로 만들어주기
            ind = 0
            while(True):
                if ind == len(values):
                    break
                if values[ind][-1:] == '\\':
                    values[ind] = values[ind][:-2]+str(',')+values[ind+1][2:]     
                    del values[ind+1] 
                else: 
                    ind += 1
            
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
                    pass


        final = eval(str(reg).replace('{}',"'none'").replace(',\\  ',','))
        
        name = file_name.split('data/')[1].split('.')[0]

        with open(path+'/'+name+'.json','w') as towrite:
            json.dump(final,towrite,ensure_ascii=True)


if __name__ == "__main__":
    path = '/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data'
    file_list = list_files_subdir(path,'reg')
    registry_json = save_as_json(file_list, path)

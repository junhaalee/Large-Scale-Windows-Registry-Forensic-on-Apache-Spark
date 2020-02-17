import os

def mkunit(path):

    f = open(path, 'r')

    # 첫째 줄에 있는 data는 사용X    
    data = f.read().split('\n\n')[1:]

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


if if __name__ == "__main__":
    
    path = "/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data/test.reg"
    new_path = "/Users/junha/Documents/Junha/Study/Bigbase/Registry_MapReduce/data/test_v.reg"

    result = mkunit(path)



rdd = [{'a':{}},{'a':{'b':1}},{'a':{'c':2}}]

def reduce_fuction(x,y):
    return x.update(y)

result = reduce_fuction(rdd[0],rdd[1])
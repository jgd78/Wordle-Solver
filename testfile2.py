def create(values,length):
    if length==0:
        return [()]
    retlist=[]
    for val in values:
        for comb in create(values, length-1):
            retlist.append((val,)+comb)
    return retlist
print(create([0,1,2], 3))
    

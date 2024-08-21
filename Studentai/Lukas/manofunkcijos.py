def pout(a, limit=20):
    if len(a) > limit:
        print(f'Rodoma {limit} eilutės iš {len(a)}')
    for k,i in enumerate(a):
        if k > limit-1:
            break
        l = []
        for n in i:
            f = f'{str(n):^16.16}'
            l.append(f)
        t = f'|{k:^3}|'+'|'.join(l)+'|'
        print(t)



def convert_to_floats(arr):
    '''
    Pakeičia string'u sąraša į float'u sąraša
    '''
    # Use the map function to apply the float function to each element in the input list
    result = map(float, arr)
    # Return the resulting iterator as a list
    return list(result)



def convert_strarrs_to_floatarrs(arr, separator):
    '''
    Pakeičia sąrašą sąrašų su string'ai į sąrašą sąrašų su float'ai
    '''
    # padaro sarasa sarasu su str elementai
    new_arr = []
    for one_arr in arr:
        new_arr.append(one_arr.split(separator))

    # padaro sarasa sarasu su float elementais
    arrs = []
    for i in new_arr:
        arrs.append(convert_to_floats(i))

    return arrs
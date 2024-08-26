import numpy as np



def pout(a, limit=5):
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



class SolarAnalyzer():
    def __init__(self, failas, skirtukas):
        self.failas = failas
        self.col1 = []
        self.col2 = []
        self.col3 = []
        self.col4 = []
        
        
        
        with open(failas, mode='r', encoding='utf-8') as file:
            self.turinys = file.readlines()
            
        for i in self.turinys[1:]:
            line = i.split(skirtukas)
            self.col1.append(float(line[0]))
            self.col2.append(float(line[1]))
            self.col3.append(float(line[2]))
            self.col4.append(float(line[3]))
    
    def get_name(self):
        self.name = str(self.failas.split('\\')[-1].split('_')[0])
        return self.name
            
    def get_pce(self):
        self.pce = float(np.absolute(np.min(self.col4)))
        return self.pce
    
    def get_jsc(self):
        min_abs = list(map(lambda x: abs(0-x), self.col1))
        mn = min(min_abs)
        idx = len(min_abs)-1
        
        while idx >= 0:
            if min_abs[idx] == mn:
                idx = idx
                break
            idx = idx - 1
        
        self.jsc = abs(self.col3[idx])
        return self.jsc
        
        # self.smallest = np.min(np.absolute(self.col1))
        # self.idx_jsc = self.col1.index(self.smallest)
        # self.jsc = float(np.absolute(self.col3[self.idx_jsc]))
        # return self.jsc
    
    def get_Uoc(self):
        min_abs = list(map(lambda x: abs(0-x), self.col3))
        mn = min(min_abs)
        idx = len(min_abs)-1
        
        while idx >= 0:
            if min_abs[idx] == mn:
                idx = idx
                break
            idx = idx - 1
        
        self.Uoc = abs(self.col1[idx])
        
        
        # self.smallest = np.min(np.absolute(self.col3))
        # self.idx_Uoc = self.col3.index(self.smallest)
        # self.Uoc = float(np.absolute(self.col1[self.idx_Uoc]))
        return self.Uoc
    
    def get_FF(self):
        return (self.get_pce() / (self.get_jsc() * self.get_Uoc())) *100
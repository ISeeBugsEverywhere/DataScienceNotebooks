import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector as cnt
from matplotlib.patches import ConnectionPatch



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
        self.pce = float(abs(min(self.col4)))
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
        return self.Uoc
    
    
    def get_FF(self):
        return (self.get_pce() / (self.get_jsc() * self.get_Uoc())) *100
    


def PieOfPie(pie1, pie1_labels, pie2, pie2_labels):
    name_pie1 = input('tite1?')
    name_pie2 = input('tite2?')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))

    angle = -180 * pie1[0]
    width = 0.2
    explode = [0.1 , 0, 0, 0 ,0]

    ax1.pie(pie1, labels=pie1_labels, autopct='%.2f%%', startangle=angle,
            explode=explode)


    ax2.pie(pie2, labels=pie2_labels, autopct='%.2f%%', startangle=angle,
            radius=0.5, textprops={'size':'smaller'})

    ax1.set_title(name_pie1)
    ax2.set_title(name_pie2)

    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
    center, r  = ax1.patches[0].center, ax1.patches[0].r

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, 0.5), xyB=(x, y),
                          coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = np.sin(np.pi /180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, -0.5), xyB=(x, y), coordsA="data",
                          coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    plt.show
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


class SolarAnalyzer():

    def __init__(self, fname, sep=';') -> None:
        self.fname= fname
        self.sep=sep
        self.__U = None
        self.__I = None
        self.__J = None
        self.__P = None
        self.__pce = None
        self.__FF = None
        self.__Uoc = None
        self.__jsc = None        
        
    
        f = open(fname, mode='r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        uv = []
        ia = []
        j = []
        p = []
        for line in lines[1:]:
            r = line.split(self.sep)
            uvi = float(r[0])
            iai = float(r[1])
            ji = float(r[2])
            pi = float(r[3])
            uv.append(uvi)
            ia.append(iai)
            j.append(ji)
            p.append(pi)
        calc1 = []
        for val in uv:
            calc1.append(abs(val-0))
        calc2 = []
        for val in j:
            calc2.append(abs(val-0))
        self.__U = uv
        self.__I = ia
        self.__J = j
        self.__P = p
        self.__pce = abs(min(p)/100*100)
        self.__jsc = abs(j[calc1.index(min(calc1))])
        self.__Uoc = abs(uv[calc2.index(min(calc2))])
        self.__FF = abs((self.__pce/(self.__jsc*self.__Uoc))*100)
    
    def U(self):
        return self.__U
    def I(self):
        return self.__I
    def J(self):
        return self.__J
    def P(self):
        return self.__P
    def pce(self):
        return self.__pce
    def FF(self):
        return self.__FF
    def Uoc(self):
        return self.__Uoc
    def jsc(self):
        return self.__jsc
    
    
def col(fname, sep=';') -> None:
    fname= fname
    sep
    __columns = []
       
        
  
    f = open(fname, mode='r', encoding='utf-8')
    line = f.readline()
    lines = f.readlines()
    f.close()
    names = line.split(sep)
    n = len(names)
    x = 0
    for i in range(n):
        globals()[f"col_{i}"] = []
        __columns.append(f"col_{i}")
        for line in lines[1:]:
            r = line.split(';')
            globals()[f"col_{i}"].append(r[x])
        x = x + 1
    pavadinimai = []
    for a, b in zip(names, __columns):
        pavadinimai.append(a+" priskirtas stulpeliui "+b)
    return pavadinimai

def pop1(sar1,sar1labels,sar2,sar2labels,indeksas = 0,title1 = '',title2 = ''):    
    
    import matplotlib.pyplot as plt
    from matplotlib.patches import ConnectionPatch
    import numpy as np

    # make figure and assign axis objects
    fig = plt.figure(figsize=(9, 5.0625))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    fig.subplots_adjust(wspace=0)
    # large pie chart parameters
    ratios = sar1
    labels = sar1labels
    angle = -180 * ratios[indeksas]
    ax1.pie(ratios, autopct='%1.1f%%', startangle=angle,
            labels=labels)
    # small pie chart parameters
    ratios = sar2
    labels = sar2labels
    width = .2
    ax2.pie(ratios, autopct='%1.1f%%', startangle=angle,
            labels=labels, radius=0.5, textprops={'size': 'smaller'})
    
    ax1.set_title(title1)
    ax2.set_title(title2)

    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[indeksas].theta1, ax1.patches[indeksas].theta2
    center, r = ax1.patches[indeksas].center, ax1.patches[indeksas].r

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, .5), xyB=(x, y),
                        coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, -.5), xyB=(x, y), coordsA="data",
                        coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(2)

    return plt.show()
    

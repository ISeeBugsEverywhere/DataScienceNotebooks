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
    def __init__(self, f='REF_D_1k_FW_2.08.dat', skirtukas=';'):
        
        self.skirtukas = skirtukas
        self.f=f
        #self.pce1=-1
        
        failas = open(self.f, mode='r', encoding='utf-8')
        self.turinys = failas.readlines()[1:]
        failas.close()
        
        self.c1, self.c2, self.c3, self.c4 = [], [], [], []
        for line in self.turinys:
            fs = line.split(skirtukas)
            self.c1.append(float(fs[0]))
            self.c2.append(float(fs[1]))
            self.c3.append(float(fs[2]))
            self.c4.append(float(fs[3]))
            
    def MedziagosPavadinimas(self):
        self.m = self.f.split('\\')[-1].split('_')[0]
        return self.m
    
    def pce(self):
        self.pce1=abs(min(self.c4))
        return self.pce1
    
    def jsc(self):
        self.tmp=self.c1[0]
        
        for i in self.c1:
            if abs(i)<=abs(self.tmp):
                self.tmp=i
        
        self.jsc1=self.c3[self.c1.index(self.tmp)]
        return abs(self.jsc1)
        
    def uoc(self):
        self.tmp=self.c3[0]
        
        for i in self.c3:
            if abs(i)<=abs(self.tmp):
                self.tmp=i
        
        self.uoc1=self.c1[self.c3.index(self.tmp)]
        return self.uoc1
    
    def ff(self):
        return abs(self.pce1/(self.jsc1*self.uoc1)*100)
        
    
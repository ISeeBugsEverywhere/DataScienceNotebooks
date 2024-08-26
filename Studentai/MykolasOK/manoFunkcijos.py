def pout(a, limit=5):
    if len(a) > limit:
        print(f'Rodoma {limit} eil. iš {len(a)}')
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
    def __init__(self,failas,sep=';',header=1):
        self.failas=failas
        self.U = []
        self.I = []
        self.j = []
        self.P = []
        print('SolarAnalyzer.\nSkaitomas failas:',failas)
        failas = open(failas,mode='r') # Duomenų failas.
        for i in range(0,header):
            print('Praleista:',failas.readline(),end='')
        for eil in failas:
            emas=eil.split(sep)
            # print(emas)
            try:
                self.U.append(float(emas[0]))
                self.I.append(float(emas[1]))
                self.j.append(float(emas[2]))
                self.P.append(float(emas[3]))
            except ValueError:
                print('Nepavyko atpažinti:',eil)
        failas.close()
        # print(self.U)
        # print(self.I)
        # print(self.j)
        # print(self.P)        
        print('SolarAnalyzer() failas perskaitytas.')



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
        print('SolarAnalyzer. Skaitomas failas:',failas)

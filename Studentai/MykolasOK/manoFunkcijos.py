import os

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

# Žr. 2024-07-29 / class TxtReader()
class SolarAnalyzer():
    def __init__(self,failas,sep=';',header=1):
        self.failas=failas
        self.__U = []
        self.__I = []
        self.__j = []
        self.__P = []
        # print('SolarAnalyzer()\nSkaitomas failas:',failas)
        failoObj = open(failas,mode='r') # Duomenų failas.
        for i in range(0,header):
            pass
            failoObj.readline()
            # print('Praleista:',failoObj.readline(),end='')
        for eil in failoObj:
            emas=eil.split(sep) # 'emas'=Eilutės MASyvas.
            # print(emas)
            try:
                self.__U.append(float(emas[0]))
                self.__I.append(float(emas[1]))
                self.__j.append(float(emas[2]))
                self.__P.append(float(emas[3]))
            except ValueError:
                print('Nepavyko atpažinti:',eil)
        failoObj.close()

        self.n=len(self.__P)

        self.medžiaga = os.path.basename(failas).split('_',1)[0]

        # pce - naudingumo koeficientas [%]:
        self.pce = abs(min(self.__P))
        
        # j(sc) - maksimali srovė [mA/cm^2]:
        minimumIndex=0
        minimum=abs(self.__U[minimumIndex])
        for i in range(1,self.n) :
            if abs(self.__U[i])<minimum :
                minimum = abs(self.__U[i])
                minimumIndex = i
        self.jsc = abs(self.__j[minimumIndex])
        # print(f'Mažiausias |U|={minimum}, i={minimumIndex}, |j|={self.jsc}')

        # U(oc) - maksimali įtampa [V]:
        minimumIndex=0
        minimum=abs(self.__j[minimumIndex])
        for i in range(1,self.n) :
            if abs(self.__j[i])<minimum :
                minimum = abs(self.__U[i])
                minimumIndex = i
        self.Uoc = abs(self.__U[minimumIndex])
        # print(f'Mažiausias |j|={minimum}, i={minimumIndex}, |U|={self.Uoc}')

        # FF - naudingumo koeficientas, palyginus su idealia SE [%]
        self.FF = (self.pce*100)/(self.jsc*self.Uoc)

        # print(f"Rezultatas: '{self.medžiaga}' {self.pce} {self.jsc} {self.Uoc} {self.FF}")


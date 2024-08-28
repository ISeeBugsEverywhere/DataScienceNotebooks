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
        
import csv       
class SolarAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_data()
    
    def read_data(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)
            data = [list(map(float, row)) for row in reader]
        return data

    def process_data(self):
        col4_values = [row[3] for row in self.data]
        Pmin = min(col4_values)
        if Pmin < 0:
            Pmin = -Pmin

        col1_values = [row[0] for row in self.data]
        closest_to_zero_col1_idx = min(range(len(col1_values)), key=lambda i: abs(col1_values[i]))
        jsc = self.data[closest_to_zero_col1_idx][2]
        if jsc<0:
            jsc=-jsc

        col3_values = [row[2] for row in self.data]
        closest_to_zero_col3_idx = min(range(len(col3_values)), key=lambda i: abs(col3_values[i]))
        Uoc = self.data[closest_to_zero_col3_idx][0]
        
        FF = (Pmin / (jsc * Uoc)) * 100
        if FF < 0:
            FF = -FF
        
        return FF, Pmin, jsc, Uoc

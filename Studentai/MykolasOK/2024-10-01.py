print('Paskaita nr. 36\n2024-10-01\n')

import os
import sys

# print(os.getcwdb())
# print(sys.argv)

args=sys.argv
n=len(args)

# for i in range(n):
#     print(args[i])
# print(n)

if n==4 and args[1].isdigit() and args[3].isdigit():
    print('trys')
    a=float(args[1])
    m=args[2]
    b=float(args[3])
    if m=='+':
        rez=a+b
        print(f'{a}+{b}={rez}')
    elif m=='-':
        rez=a-b
        print(f'{a}-{b}={rez}')
    elif m in ['x','kart','*']: # Ženklas '*' turi spec. reikšmę.
        rez=a*b
        print(f'{a}x{b}={rez}')
    elif m=='/':
        rez=a/b
        print(f'{a}/{b}={rez}')
    else :
        print('Neatpažintas veiksmas')
else :
    print('Skaičiavimui netinkami parametrai.\n(python3 2024-10-01.py 7 x 8)\n')
# Alternatyva: eval()

import matplotlib.pyplot as plt
import numpy as np
 
A = np.arange(0, 10)
B = A*np.random.randint(1,11,10)
C = B*np.random.randint(1,11,10)
 
# fig, ax = plt.subplots()
# ax.plot(A,B)
# # plt.show()
 
# fig, ax = plt.subplots()
# ax.plot(A,C)
# # plt.show()

# Parašykite skriptą, kuriam galėtumėte nurodyti failą (pavadinimas arba pilnas kelias iki jo), 
# stulpelių skirtuką, stulpelius, kuriuos reikia atvaizduoti, 
# ir jūsų skriptas turi nuskaityti tą failą, ir nubraižyti pageidaujamą grafiką. 
# Patobulinkite, jog skriptui galima būtų nurodyti daugiau nei vieną failą, 
# jų turiniai turi būti atvaizduojami viename grafike.

import pandas as pd

# DUS2014.csv
n=len(args)
if n<3 :
    sys.exit('Nepakanka parametrų failui perskaityti.\n(python3 2024-10-01.py DUS2014.csv ,)')

duomenys=pd.read_csv(f'../../DATA/{args[1]}',sep=args[2])
if n>3 :
    # print(args)
    stulpeliai=args[3:]
    # print(stulpeliai)
    stulpeliai_int = list(map(int,stulpeliai))
    # print(stulpeliai_int)
    duomenys3=duomenys.iloc[:,stulpeliai_int]
else :
    duomenys3=duomenys

print(duomenys3.head(3))
print(duomenys3.tail(3))




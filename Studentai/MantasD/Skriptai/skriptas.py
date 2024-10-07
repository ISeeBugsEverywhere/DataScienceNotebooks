# import sys
# import os
# import matplotlib.pyplot as plt
# import numpy as np

# A = np.arange(0, 10)
# B = A*np.random.randint(1,11,10)
# C = B*np.random.randint(1,11,10)

# fig, ax = plt.subplots()
# ax.plot(A,B)
# plt.show()

# fig, ax = plt.subplots()
# ax.plot(A,C)
# plt.show()



    
#parašykite skriptą, kuriam galėtumėte nurodyti tris argumentus, du skaičius ir matematinį veiksmą. 
# Skriptas turi išspausdinti rezultatą. Nuspręskite, ką darysite, jei bus pateikta per daug, per mažai, ar netinkami parametrai.
# args = sys.argv
# if len(args) == 4:
#     print(f'Skriptui pateikti argumentai: skaičius {args[1]} , skaičius {args[2]} , veiksmas {args[3]}')
#     print(f' atsakymas {float(args[1])args[3]float(args[2])}')
# else:
#     print('Netinkamas argumentų skaičius')


# parašykite skriptą, kuriam galėtumėte nurodyti failą (pavadinimas arba pilnas kelias iki jo), 
# stulpelių skirtuką, stulpelius, kuriuos reikia atvaizduoti, ir jūsų skriptas turi nuskaityti tą failą, ir nubraižyti pageidaujamą grafiką. 
# Patobulinkite, jog skriptui galima būtų nurodyti daugiau nei vieną failą, jų turiniai turi būti atvaizduojami viename grafike.
fname = input('Iveskite failo lokaciją')
sep = input('Nurodykite separatorių')

def getinfo(fname, sep = ';'):
    f = open(fname, mode='r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines[1:]:
        r = line.split(sep)
        l = []
        for ls in range(len(r)):
            f = f'{str(r[ls]):^16.16}'
            l.append(f)
        t = f'| '.join(l)
        print(t)
getinfo(fname=fname)


            
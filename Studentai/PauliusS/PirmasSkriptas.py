# import sys 
# import os 

# # print(os.getcwd())    #rodo kur issaugojome 
# # print(sys.argv)       # pilnas kelias #argv grazina sarasa parametru (padeda pasiimti parametrus is PowerShell)

# args = sys.argv

# if len(args) > 1:
#     print('Skriptui buvo pateikta \n parametrai')
#     print(f'ju kiekis {len(args)-1}')


# parašykite skriptą, kuriam galėtumėte nurodyti tris argumentus, 
# du skaičius ir matematinį veiksmą. Skriptas turi išspausdinti rezultatą. 
# Nuspręskite, ką darysite, jei bus pateikta per daug, per mažai, ar netinkami 
# parametrai.

# parašykite skriptą, kuriam galėtumėte nurodyti failą 
# (pavadinimas arba pilnas kelias iki jo), stulpelių skirtuką, stulpelius, 
# kuriuos reikia atvaizduoti, ir jūsų skriptas turi nuskaityti tą failą, ir 
# nubraižyti pageidaujamą grafiką. Patobulinkite, jog skriptui galima būtų 
# nurodyti daugiau nei vieną failą, jų turiniai turi būti atvaizduojami 
# viename grafike.

# Galite panaudoti OOP_DATA aplanke turimus failus

import sys 
import os 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

args = sys.argv

failo_kelias = input('Irasykite failo kelia: ')

stulp_skirtukas = input('Irasykite stulpeliu skirtuka: ')

df = pd.read_csv(failo_kelias, delimiter=stulp_skirtukas)

stulpelis = input('Nurodykite stulpelio pavadinima: ')

sns.scatterplot(
    data=df,       # Nurodoma duomenų šaltinio DataFrame, iš kurio bus paimti duomenys
    x='age',       # X ašis atvaizduos 'age' stulpelio reikšmes, rodančias respondentų amžių
    y='charges',   # Y ašis atvaizduos 'charges' stulpelio reikšmes, rodančias išlaidas ar mokesčius
    hue='sex'      # Duomenų taškai bus spalvoti pagal 'sex' stulpelio reikšmes, atskiriant lytis
)


sns.scatterplot(data=df, x='U[V]', y='I[A]')













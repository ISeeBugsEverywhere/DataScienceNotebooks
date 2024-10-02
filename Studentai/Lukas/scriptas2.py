import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# A = np.arange(0, 10)
# B = A*np.random.randint(1,11,10)
# C = B*np.random.randint(1,11,10)

# fig, ax = plt.subplots()
# ax.plot(A,B)
# plt.title('title 1')
# # plt.show()

# fig, ax = plt.subplots()
# ax.plot(A,C)
# plt.title('title 2')
# plt.show()

# parašykite skriptą, kuriam galėtumėte nurodyti failą (pavadinimas arba pilnas kelias iki jo),
# stulpelių skirtuką, stulpelius, kuriuos reikia atvaizduoti,
# ir jūsų skriptas turi nuskaityti tą failą, ir nubraižyti pageidaujamą grafiką. 
# Patobulinkite, jog skriptui galima būtų nurodyti daugiau nei vieną failą,
# jų turiniai turi būti atvaizduojami viename grafike.

# .iloc[:, 1]

args = sys.argv
print(args, len(args))
d = '../../DATA/OOP_DATA/'
file = d + args[1]

df = pd.read_table(file, sep=args[2])
# print(df.head())
# print(args[3])
# print(args[4])
df_2 = df.iloc[:,[int(args[3]), int(args[4])]]
# df_2.plot(kind='line', x=df_2.iloc[:,0], y=df_2.iloc[:,1])

fig, ax = plt.subplots()

ax.plot(df_2.iloc[:,0], df_2.iloc[:,1])
plt.show()

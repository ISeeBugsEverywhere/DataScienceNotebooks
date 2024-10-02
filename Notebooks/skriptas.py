#parašykite skriptą, kuriam galėtumėte nurodyti tris argumentus, du skaičius ir matematinį veiksmą. Skriptas turi išspausdinti rezultatą. Nuspręskite, ką darysite, jei bus pateikta per daug, per mažai, ar netinkami parametrai.

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

A = np.arange(0, 10)
B = A*np.random.randint(1,11,10)
C = B*np.random.randint(1,11,10)

fig, ax = plt.subplots()
ax.plot(A,B)
# plt.show()

fig, ax = plt.subplots()
ax.plot(A,C)
plt.show()


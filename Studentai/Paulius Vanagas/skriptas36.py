# import sys
# import os

# args = sys.argv

# if len(args)== 4 :

#     if args[2] == '/' or args[2] != '*' or args[2] != '-' or args[2] != '+':
#         rez=eval(args[1]+args[2]+args[3])
#     else: 
#         rez='netinkamas matematinis veiksmas'
        
#     # if args[2] == '+':
#     #     rez = int(args[1]) + int(args[3])
#     # if args[2] == '-':
#     #     rez = int(args[1]) - int(args[3])
#     # if args[2] == '*':
#     #     rez = int(args[1]) * int(args[3])
#     # if args[2] == '/':
#     #     rez = int(args[1]) / int(args[3]) 
# else: 
#     rez= 'turi buti 3 simboliai: skaicius veiksmas skaicius'
 
# print(rez)

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

A = np.arange(0, 10)
B = A*np.random.randint(1,11,10)
C = B*np.random.randint(1,11,10)

fig, ax = plt.subplots()
ax.plot(A,B)
plt.show()

fig, ax = plt.subplots()
ax.plot(A,C)
plt.show()
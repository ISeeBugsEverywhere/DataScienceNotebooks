import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px
import glob

args = sys.argv

print(args)

df = pd.read_csv(r'C:\Users\pauli\Desktop\DataScienceNotebooks\DATA\OOP_DATA\REF_D_1k_FW_2.08.dat', sep=args[1])

fig, axis = plt.subplots()
axis.plot( df.index, df.iloc[:, int(args[2])], label = 'test')
# axis.set_xticks(dfKET['menuo'])
axis.legend(loc='best')
plt.title('bandymas')
plt.show()

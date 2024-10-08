# nuskaityti GMP failą (didenįjį), x, y koordinantes konvertuoti į pasaulines ilgumą ir platumą, pridėti gautąsias koordinantes kaip du naujus stulpelius.
# atrinkti tik gaisrus iki 3jų autocisternų ir jų įvykių vietas atvaizduoti plotly express mapbox grafike.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px
import sys, os
from LKS94WGS84 import *

gmp2 =  pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/GMP.csv')

x = list(gmp2['X'])
y = list(gmp2['Y'])
X =[]
Y = []
for a,b in zip(x,y):
    Y.append(grid2geo(a,b)[0])
    X.append(grid2geo(a,b)[1])

gmp2['NX'] = pd.DataFrame(X, columns=['NX'])
gmp2['NY'] = pd.DataFrame(Y, columns=['NY'])

def gaisras(d):
    if str("Gaisras") in str(d):
        return True
    else:
        False

gmp2['Gaisras'] = gmp2['zemesnis_ivykio_tipas'].apply(gaisras)

def did_gaisras(d):
    if "Gaisras" in str(d) and "Gaisras 0" not in str(d):
        return True
    else:
        False

gmp2['Did_gaisras'] = gmp2['zemesnis_ivykio_tipas'].apply(did_gaisras)

gmp2_dg = gmp2[gmp2['Did_gaisras']==True]

fig = px.scatter_mapbox(data_frame=gmp2_dg, lon='NX', lat='NY', zoom=6.1)
fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(width=800, height=600)
fig.show()

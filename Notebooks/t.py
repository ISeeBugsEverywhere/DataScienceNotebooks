import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px


import os, sys, requests

url = 'https://api.meteo.lt/v1/stations/vilniaus-ams/observations/latest'

page = requests.get(url)
r = page.json()

df = pd.DataFrame(data=r['observations'])
df.rename(columns={'observationTimeUtc':'time'}, inplace=True)
df['time'] = pd.to_datetime(df['time'])

def qtWindow(fig):
    import plotly.offline
    from PyQt5.QtCore import QUrl
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWidgets import QApplication    
    plotly.offline.plot(fig, filename='name.html', auto_open=False)    
    app = QApplication(sys.argv)
    web = QWebEngineView()
    file_path = os.path.abspath(os.path.join(os.getcwd(), "name.html"))
    print(os.path.dirname(__file__), os.getcwd(), file_path, sep="\n=======\n")
    web.load(QUrl.fromLocalFile(file_path))
    web.show()
    sys.exit(app.exec_())


fig =  px.line(data_frame=df, x='time', y='airTemperature')

qtWindow(fig)

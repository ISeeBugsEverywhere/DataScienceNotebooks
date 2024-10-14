import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px 
import requests
import os

import selenium
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from bs4 import BeautifulSoup
import time

opcijos = Options()
opcijos.add_argument('--incognito')
driver = webdriver.Chrome(options=opcijos)
url = 'https://autoplius.lt/skelbimai/naudoti-automobiliai?page_nr=1'
driver.get(url)
time.sleep(5)
source = driver.page_source

bs = BeautifulSoup(source, 'html.parser')
# print(bs)
auto_nuorodos = []


auto_links = bs.find('div', {'class':'auto-lists lt'}).find_all('a')
for link in auto_links:
    # print(link['href'])
    auto_nuorodos.append(link['href'])

# print(auto_nuorodos)
# print(len(auto_nuorodos))

kitas = bs.find('div', {'class':'page-navigation-container'}).find('a', {'class':'next'})
print(kitas['href'])

next_nuoroda = f'https://autoplius.lt{kitas['href']}'
# print(next_nuoroda)

page = 1
while page < 201:
    for nuoroda in auto_nuorodos:
        # atsidarom kieviena nuoroda su get metodu, pasiimam reikiama info
        # info irasome i duomenu baze
        pass
    
    # su get metodu atsidarom next_nuoroda
    # nuskaitome next puslapi
    # pasiimam nuajas auto nuorodas ir nauja next nuorodas
    # cikla kartojam is naujo
    page =+ 1

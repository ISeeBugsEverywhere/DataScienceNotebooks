# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('ignore')
# import seaborn as sns
import sqlite3
import mysql.connector as cnt
# import plotly.express as px 
# import requests
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

page = 1
# while page < 201:
while page < 11:
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
    # print(kitas['href'])
    kitas_psl = kitas['href']
    next_nuoroda = f'https://autoplius.lt{kitas_psl}'
    # print(next_nuoroda)


    for nuoroda in auto_nuorodos:
        # atsidarom kieviena nuoroda su get metodu, pasiimam reikiama info
        # info irasome i duomenu baze
        markes5 = []
        modeliai5= []
        keys5 = []
        values5 = []
        car_i5 = {}
        
        duomenys = {
        'Marke': 'None',
        'Modelis':'None',
        'Kaina':'None',
        'Rida':'None',
        'Variklis':'None',
        'Kuro tipas':'None',
        'Pavarų dėžė':'None',
        'Varantieji ratai':'None',
        'Baterijos talpa, kWh':'None',
        'Elektra nuvažiuojamas atstumas':'None',
        '':'None',
        'Defektai':'None',
        'Spalva':'None',
        'Kėbulo tipas':'None',
        'Vidutinės':'None',
        'Mieste':'None',
        'Užmiestyje':'None',
        'Pirma registracija':'None',
        'Pirmosios registracijos šalis':'None',
        'Bendroji masė, kg':'None',
        'Nuosava masė, kg':'None',
        'Durų skaičius':'None',
        'Kėbulo numeris (VIN)':'None',
        'Ilgis':'None',
        'Aukštis':'None',
        'Tech. apžiūra iki':'None',
        'CO₂ emisija, g/km':'None',
        'Euro standartas':'None',
        'Taršos mokestis':'None',
        'SDK':'None',
        'Klimato valdymas':'None',
        'Sėdimų vietų skaičius':'None',
        'Ratlankių skersmuo':'None'
        }

        url = nuoroda
        driver.get(url)
        time.sleep(1)
        source = driver.page_source
        
        bs_auto = BeautifulSoup(source, 'html.parser')
        
        if bs_auto.find('div', {'class':'error'}):
            print('skelbimas neegzistuoja')
        else:
            car = bs_auto.find('ol', {'class':'breadcrumbs'}).find_all('li', {'class':'crumb'})
            marke = car[2].text.strip()
            modelis = car[3].text.strip()
            markes5.append(marke)
            modeliai5.append(modelis)
            # print(marke, modelis)
            duomenys['Marke'] = marke
            duomenys['Modelis'] = modelis

            car_price = bs_auto.find('div', {'class':'prices'})
            kaina = car_price.text.split('€')[0].strip()
            duomenys['Kaina'] = kaina

            car_info = bs_auto.find_all('div', {'class':'parameter-row'})
            for info in car_info[1:]:
                # print(info)
                # if info is not None:
                #     # print('::NRW:::')
                key = info.find('div', {'class':'parameter-label'}).text.strip()
                # print(key.text.strip())
                keys5.append(key)
                if info.find('div', {'class':'parameter-value green-vehicle'}):
                    value = info.find('div', {'class':'parameter-value green-vehicle'}).text.strip()
                if info.find('div', {'class':'parameter-value co2-tax approximate free'}):
                    value = info.find('div', {'class':'parameter-value co2-tax approximate free'}).text.strip()
                else:
                    value = info.find('div', {'class':'parameter-value'}).text.strip()
                values5.append(value)
                # print(key, value)
                # print(value.text.strip())
                duomenys[key] = value

        # for k, v in zip(keys5)    
        # print(duomenys)
        data = tuple(duomenys.values())
        data1 = []
        data1.append(data)

        SDB = sqlite3.connect('Auto.db')  # jei neegzistuoja db , bus sukurta nauja db
        Cs = SDB.cursor()

        #  if not exists - tikrina ar jau sukurta DB
        sql = '''create table if not exists Autopliuslt
        (
        Marke text not null,
        Modelis text not null,
        Kaina text not null,
        Rida text not null,
        Variklis text not null,
        Kuras text not null,
        PavaruDeze text not null,
        VarantiejiRatai text not null,
        BaterijosTalpakWh text not null,
        ElektraNuvažiuojamasAtstumas text not null,
        Ikraunamas text not null,
        Defektai text not null,
        Spalva text not null,
        KebuloTipas text not null,
        VidutinesSanaudos text not null,
        MiesteSanaudos text not null,
        UzmiestyjeSanaudos text not null,
        PirmaRegistracija text not null,
        PirmosiosRegistracijosSalis text not null,
        BendrojiMase text not null,
        NuosavaMase text not null,
        DuruSkaicius text not null,
        KebuloNr text not null,
        Ilgis text not null,
        Aukstis text not null,
        TechApžiuraIki text not null,
        COemisijagkm text not null,
        EuroStandartas text not null,
        TarsosMokestis text not null,
        SDK text not null,
        KlimatoValdymas text not null,
        SedimosVietos text not null,
        Ratlankiai text not null
        )
        '''
        Cs.execute(sql)

        sql_template = '''insert into Autopliuslt values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        Cs.executemany(sql_template, data1)

        SDB.commit() # commit() butinas jei norim irasyti duomenis i DB

        SDB.close()
        

    driver.get(next_nuoroda)
    
    # su get metodu atsidarom next_nuoroda
    # nuskaitome next puslapi
    # pasiimam nuajas auto nuorodas ir nauja next nuorodas
    # cikla kartojam is naujo
    page = page +1
    print('data written to DB')
    print(f'kitas puslapis: {kitas_psl}')

driver.close()
print('Baigta!!!')
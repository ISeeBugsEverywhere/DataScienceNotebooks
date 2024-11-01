from manofunkcijos import *
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver # naršyklės kontroleris
from selenium.webdriver.chrome.options import Options #Naršyklės
import time
import datetime

def timing():
    Objekto_tipai = {'Butai pardavimui':'butai', 'Butai nuomai':'butu-nuoma'}
    Miestai = {'Kaunas':'kaune', 'Vilnius':'vilniuje', 'Klaipėda':'klaipedoje', 'Šiauliai':'siauliuose', 'Panevėžys':'panevezyje', 'Alytus':'alytuje', 'Palanga':'palangoje'}

    # database_location = ''
    # table_name = ''
    # database_location = str(input(f'Įveskte duomenų bazės pavadinimą arba pilną kelią su failo pavadinimu. Formatas "pavyzdys.db" arba "../../../pavyzdys.db"'))
    # table_name = str(input(f'Įveskite lentelės pavadinimą'))

    # Trigeriai
    continue_trigger = False
    city_trigger = False
    continue_trigger_input = ''

    Miesto_pasirinkimai = []
    Miesto_pasirinkimai = input(f'Įveskite norimus aruodo skelbimų miestus su skyrinkliu ",".\nSąrašas miestų {list(Miestai.keys())}.\nJei nepasirinksite nieko tokiu atveju bus imami visų Aruode esančių miestų skelbimai.').split(',')
    if Miesto_pasirinkimai == ['']:
        city_trigger = False
        print(f'Pasirinkote visus Aruodo miestus')
    else:
        city_trigger = True
        print(f'Pasirinkote {Miesto_pasirinkimai}')
        
    continue_trigger_input = input(f'Įveskite "Taip" jei norite tęsti pradėtą pildyti db arba "Ne" jai db pildoma pirmą kartą')
    if continue_trigger_input == 'Taip':
        continue_trigger = True
    else:
        continue_trigger = False
        remove_table('../../../web_scrap.db','aruodas')

    t= int(input(f'Įveskite darbo laiką minutėmis, jai nurodysite 0, tokiu atveju ciklas veiks kol pabaigs rinkti duomenis'))
    if t > 0:
        delta = t*60
    else:
        delta = None
    
    start_time = datetime.datetime.now()
    if city_trigger == False:
        for obj in Objekto_tipai.keys():
            print(Objekto_tipai[obj])
            puslapis = 1
            opcijos = Options()
            opcijos.add_argument('--incognito')
            driver = webdriver.Chrome(options=opcijos)
            url = f'https://www.aruodas.lt/{Objekto_tipai[obj]}/puslapis/{puslapis}/?FOwnerDbId0=1&FOwnerDbId2=1'
            driver.get(url)
            time.sleep(3)
            source = driver.page_source
            bs = BeautifulSoup(source, 'html.parser')
            first = bs.find('div', {'class':'markTexts'})
            skelbimai = first.find('div', {'class':'number'})
            puslapiai = int(int(skelbimai.text.strip().replace('(','').replace(')',''))/25)
            for puslapis in range(puslapiai):
                puslapis = puslapis + 1
                url = f'https://www.aruodas.lt/{Objekto_tipai[obj]}/puslapis/{puslapis}/?FOwnerDbId0=1&FOwnerDbId2=1'
                driver.get(url)
                source = driver.page_source
                bs = BeautifulSoup(source, 'html.parser')
                skelbimas = bs.find_all('div', {'class':'list-adress-v2'})
                for s in skelbimas:
                    try:
                        url = s.find('a')['href']
                        if continue_trigger == True:
                            continue_value = not check_if_value_exists_or_max('../../../web_scrap.db','aruodas','URL',url)
                        else:
                            continue_value = True
                        if continue_value:
                            skelbimai = {}
                            skelbimai['Miestas'] = s.find('a').text.strip()
                            skelbimai['Kaina'] = s.find_all('span', {'class':'list-item-price-v2'})[0].text.strip().replace(' ','')[:-1]
                            driver.get(url)
                            source = driver.page_source
                            bs = BeautifulSoup(source, 'html.parser')
                            pav = bs.find('dl', {'class':'obj-details'}).find_all('dt')
                            values = bs.find('dl', {'class':'obj-details'}).find_all('dd')
                            skelbimai['Adresas'] = bs.find('h1', {'class':'obj-header-text'}).text.strip()
                            for p, v in zip(pav,values):
                                skelbimai[p.text.strip()[:-1]] = v.text.strip()
                            skelbimai['URL'] = url
                            skelbimai['Tipas'] = obj
                            insert_into_db(skelbimai,'../../../web_scrap.db','aruodas')
                            check_time = datetime.datetime.now()
                            check_delta = (check_time-start_time).total_seconds()
                            if delta != None and check_delta >= delta:
                                return print('Stabdoma')
                    except Exception as e:
                        pass
            driver.close()
    else:
        for m in Miesto_pasirinkimai:
            miestas = Miestai[m]
            for obj in Objekto_tipai.keys():
                print(Objekto_tipai[obj])
                puslapis = 1
                opcijos = Options()
                opcijos.add_argument('--incognito')
                driver = webdriver.Chrome(options=opcijos)
                url = f'https://www.aruodas.lt/{Objekto_tipai[obj]}/{miestas}/puslapis/{puslapis}/?FOwnerDbId0=1&FOwnerDbId2=1'
                driver.get(url)
                time.sleep(3)
                source = driver.page_source
                bs = BeautifulSoup(source, 'html.parser')
                first = bs.find('div', {'class':'markTexts'})
                skelbimai = first.find('div', {'class':'number'})
                puslapiai = int(int(skelbimai.text.strip().replace('(','').replace(')',''))/25)
                for puslapis in range(puslapiai):
                    puslapis = puslapis + 1
                    url = f'https://www.aruodas.lt/{Objekto_tipai[obj]}/{miestas}/puslapis/{puslapis}/?FOwnerDbId0=1&FOwnerDbId2=1'
                    driver.get(url)
                    source = driver.page_source
                    bs = BeautifulSoup(source, 'html.parser')
                    skelbimas = bs.find_all('div', {'class':'list-adress-v2'})
                    for s in skelbimas:
                        try:
                            url = s.find('a')['href']
                            if continue_trigger == True:
                                continue_value = not check_if_value_exists_or_max('../../../web_scrap.db','aruodas','URL',url)
                            else:
                                continue_value = True
                            if continue_value:
                                skelbimai = {}
                                skelbimai['Miestas'] = s.find('a').text.strip()
                                skelbimai['Kaina'] = s.find_all('span', {'class':'list-item-price-v2'})[0].text.strip().replace(' ','')[:-1]
                                driver.get(url)
                                source = driver.page_source
                                bs = BeautifulSoup(source, 'html.parser')
                                pav = bs.find('dl', {'class':'obj-details'}).find_all('dt')
                                values = bs.find('dl', {'class':'obj-details'}).find_all('dd')
                                skelbimai['Adresas'] = bs.find('h1', {'class':'obj-header-text'}).text.strip()
                                for p, v in zip(pav,values):
                                    skelbimai[p.text.strip()[:-1]] = v.text.strip()
                                skelbimai['URL'] = url
                                skelbimai['Tipas'] = obj
                                insert_into_db(skelbimai,'../../../web_scrap.db','aruodas')
                                check_time = datetime.datetime.now()
                                check_delta = (check_time-start_time).total_seconds()
                                if delta != None and check_delta >= delta:
                                    return print('Stabdoma')
                        except Exception as e:
                            pass
                driver.close()
    return print('Ciklas baigtas')
timing()
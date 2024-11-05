import sys
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup as BS


conn = sqlite3.connect('aruodas_rent.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        price TEXT,
        namo_numeris TEXT,
        buto_numeris TEXT,
        plotas TEXT,
        kambariu_sk TEXT,
        aukstas TEXT,
        aukstu_sk TEXT,
        metai TEXT,
        pastato_tipas TEXT,
        sildymas TEXT,
        irengimas TEXT,
        energijos_klase TEXT
    )
''')
conn.commit()


options = FirefoxOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')  

service = Service(r'C:\Users\Batia\Downloads\geckodriver-v0.34.0-win64\geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)

def scrape_links(mode, max_pages):
    links = []
    for i in range(1, max_pages + 1):  
        print(f"Scraping {mode} listings page {i}...")
        url = f'https://www.aruodas.lt/butai/puslapis/{i}/?FOwnerDbId0=1&FOwnerDbId2=1' if mode == 'sale' else f'https://www.aruodas.lt/butu-nuoma/puslapis/{i}/?FOwnerDbId0=1&FOwnerDbId2=1'
        driver.get(url)
        time.sleep(2)

        bs = BS(driver.page_source, 'html.parser')
        bt = bs.find_all('div', {'class': 'list-photo-v2'})

        if not bt:
            print("No more pages. End.")
            break

        for skelbimas in bt:
            linkt = skelbimas.find('a')
            link = linkt.get('href')
            links.append(link)

    return links

def scrape_listing(url):
    driver.get(url)
    time.sleep(2)
    
    bs = BS(driver.page_source, 'html.parser')
    
    address = bs.find('h1', class_='obj-header-text').text.strip()
    
    price = bs.find('span', class_='price-eur').text.strip()
    
    details = bs.find('dl', class_='obj-details')
    details_dict = {}

    keys = details.find_all('dt')
    values = details.find_all('dd')

    for key, value in zip(keys, values):
        key_text = key.text.strip().replace(':', '')  # Clean the text, remove colon
        span_value = value.find('span', class_='fieldValueContainer')
        
        # Check if span_value exists
        if span_value:
            value_text = span_value.text.strip()
        else:
            value_text = 'N/A'  # Assign a default value if the span is not found
        
        details_dict[key_text] = value_text

    
    namo_numeris = details_dict.get('Namo numeris', 'N/A')
    buto_numeris = details_dict.get('Buto numeris', 'N/A')
    plotas = details_dict.get('Plotas', 'N/A')
    kambariu_sk = details_dict.get('Kambarių sk.', 'N/A')
    aukstas = details_dict.get('Aukštas', 'N/A')
    aukstu_sk = details_dict.get('Aukštų sk.', 'N/A')
    metai = details_dict.get('Metai', 'N/A')
    pastato_tipas = details_dict.get('Pastato tipas', 'N/A')
    sildymas = details_dict.get('Šildymas', 'N/A')
    irengimas = details_dict.get('Įrengimas', 'N/A')
    energijos_klase = details_dict.get('Pastato energijos suvartojimo klasė', 'N/A')

    
    listing_data = (
        address, price, namo_numeris, buto_numeris, plotas, kambariu_sk, aukstas,
        aukstu_sk, metai, pastato_tipas, sildymas, irengimas, energijos_klase
    )
    
    return listing_data

def main():
    
    if len(sys.argv) < 5:
        print("Usage: python scraper.py <operation> <start/continue> <number_of_pages_for_links> <number_of_pages_for_details> <mode>")
        return

    operation = sys.argv[1]
    pages_for_links = int(sys.argv[2])
    pages_for_details = int(sys.argv[3])
    mode = sys.argv[4]  # sale or rent

    if mode not in ['sale', 'rent']:
        raise ValueError("Invalid mode. Use 'sale' or 'rent'.")

    if operation == 'start':
        cursor.execute("DELETE FROM listings")
        conn.commit()
        links = scrape_links(mode, pages_for_links)
        
        # Limit the number of details to scrape
        links_to_scrape = links[:pages_for_details]  # Only take the first 'pages_for_details' links

        for link in links_to_scrape:
            listing_data = scrape_listing(link)
            cursor.execute('''
                INSERT INTO listings (address, price, namo_numeris, buto_numeris, plotas, kambariu_sk, aukstas,
                aukstu_sk, metai, pastato_tipas, sildymas, irengimas, energijos_klase)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', listing_data)
            conn.commit()
        
    elif operation == 'continue':
        links = scrape_links(mode, pages_for_links)
        
        # Limit the number of details to scrape
        links_to_scrape = links[:pages_for_details]  # Only take the first 'pages_for_details' links

        for link in links_to_scrape:
            listing_data = scrape_listing(link)
            cursor.execute('''
                INSERT INTO listings (address, price, namo_numeris, buto_numeris, plotas, kambariu_sk, aukstas,
                aukstu_sk, metai, pastato_tipas, sildymas, irengimas, energijos_klase)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', listing_data)
            conn.commit()
    else:
        print("Invalid operation. Use 'start' or 'continue'.")

    driver.quit()  
    conn.close()  

if __name__ == "__main__":
    main()

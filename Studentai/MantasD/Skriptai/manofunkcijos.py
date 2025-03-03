import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import requests
import json
import os
import re
import datetime
import time
import random
import string

def pout(a, limit=5):
    if len(a) > limit:
        print(f'Rodoma {limit} eilutės iš {len(a)}')
    for k,i in enumerate(a):
        if k > limit-1:
            break
        l = []
        for n in i:
            f = f'{str(n):^16.16}'
            l.append(f)
        t = f'|{k:^3}|'+'|'.join(l)+'|'
        print(t)


class SolarAnalyzer():

    def __init__(self, fname, sep=';') -> None:
        self.fname= fname
        self.sep=sep
        self.__U = None
        self.__I = None
        self.__J = None
        self.__P = None
        self.__pce = None
        self.__FF = None
        self.__Uoc = None
        self.__jsc = None        
        
    
        f = open(fname, mode='r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        uv = []
        ia = []
        j = []
        p = []
        for line in lines[1:]:
            r = line.split(self.sep)
            uvi = float(r[0])
            iai = float(r[1])
            ji = float(r[2])
            pi = float(r[3])
            uv.append(uvi)
            ia.append(iai)
            j.append(ji)
            p.append(pi)
        calc1 = []
        for val in uv:
            calc1.append(abs(val-0))
        calc2 = []
        for val in j:
            calc2.append(abs(val-0))
        self.__U = uv
        self.__I = ia
        self.__J = j
        self.__P = p
        self.__pce = abs(min(p)/100*100)
        self.__jsc = abs(j[calc1.index(min(calc1))])
        self.__Uoc = abs(uv[calc2.index(min(calc2))])
        self.__FF = abs((self.__pce/(self.__jsc*self.__Uoc))*100)
    
    def U(self):
        return self.__U
    def I(self):
        return self.__I
    def J(self):
        return self.__J
    def P(self):
        return self.__P
    def pce(self):
        return self.__pce
    def FF(self):
        return self.__FF
    def Uoc(self):
        return self.__Uoc
    def jsc(self):
        return self.__jsc
    
    
def col(fname, sep=';') -> None:
    fname= fname
    sep
    __columns = []
       
        
  
    f = open(fname, mode='r', encoding='utf-8')
    line = f.readline()
    lines = f.readlines()
    f.close()
    names = line.split(sep)
    n = len(names)
    x = 0
    for i in range(n):
        globals()[f"col_{i}"] = []
        __columns.append(f"col_{i}")
        for line in lines[1:]:
            r = line.split(';')
            globals()[f"col_{i}"].append(r[x])
        x = x + 1
    pavadinimai = []
    for a, b in zip(names, __columns):
        pavadinimai.append(a+" priskirtas stulpeliui "+b)
    return pavadinimai

def pop(sar1,sar1labels,sar2,sar2labels,indeksas = 0,title1 = '',title2 = ''):    
    
    import matplotlib.pyplot as plt
    from matplotlib.patches import ConnectionPatch
    import numpy as np

    # make figure and assign axis objects
    fig = plt.figure(figsize=(9, 5.0625))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    fig.subplots_adjust(wspace=0)
    # large pie chart parameters
    ratios = sar1
    labels = sar1labels
    labels_for_ex = list(set(labels))
    explode = []
    ex = 0
    for e in labels_for_ex:
        if ex == indeksas:
            explode.append(0.1)
        else:
            explode.append(0)
        ex += 1 
    angle = -180 * ratios[indeksas]
    ax1.pie(ratios, autopct='%1.1f%%', startangle=angle,
            labels=labels, explode=explode)
    # small pie chart parameters
    ratios = sar2
    labels = sar2labels
    width = .2
    ax2.pie(ratios, autopct='%1.1f%%', startangle=angle,
            labels=labels, radius=0.5, textprops={'size': 'smaller'})
    
    ax1.set_title(title1)
    ax2.set_title(title2)

    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[indeksas].theta1, ax1.patches[indeksas].theta2
    center, r = ax1.patches[indeksas].center, ax1.patches[indeksas].r

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, .5), xyB=(x, y),
                        coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, -.5), xyB=(x, y), coordsA="data",
                        coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(2)

    return plt.show()
    
def bop(sar1,sar1labels,sar2,sar2labels,indeksas = 0,title1 = '',title2 = ''):
    import matplotlib.pyplot as plt
    import numpy as np

    from matplotlib.patches import ConnectionPatch

    # make figure and assign axis objects
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)

    # pie chart parameters
    overall_ratios = sar1
    labels = sar1labels
    labels_for_ex = list(set(labels))
    explode =[]
    ex = 0
    for e in labels_for_ex:
        if ex == indeksas:
            explode.append(0.1)
        else:
            explode.append(0)
        ex += 1 
    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[indeksas]
    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                        labels=labels, explode=explode)

    ax1.set_title(title1)
    
    # bar chart parameters
    age_ratios = sar2
    age_labels = sar2labels
    bottom = 1
    width = .2

    # Adding from the top matches the legend.
    for j, (height, label) in enumerate(reversed([*zip(age_ratios, age_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                    alpha=0.1 + 0.25 * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title(title2)
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[indeksas].theta1, wedges[indeksas].theta2
    center, r = wedges[indeksas].center, wedges[indeksas].r
    bar_height = sum(age_ratios)

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)

    plt.show()
    
    
def check_if_value_exists_or_max(db_path, table_name, column_name, value=None):
    import sqlite3
    # Prisijungimas prie SQLite duomenų bazės
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if value is None:
        # Jei value yra None, gauti maksimalią reikšmę kaip float
        sql = f"SELECT MAX(CAST(\"{column_name}\" AS REAL)) FROM {table_name}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        return result[0]  # Grąžinti maksimalią reikšmę (float)
    else:
        # Jei value nurodyta, patikrinti, ar yra įrašas su šia reikšme
        sql = f"SELECT 1 FROM {table_name} WHERE \"{column_name}\" = ? LIMIT 1"
        cursor.execute(sql, (value,))
        result = cursor.fetchone()
        conn.close()
        return result is not None  # Grąžinti True jei yra įrašas, False jei ne
        
        
def insert_into_db(data, db_path, table_name):
    import sqlite3
    try:
        # Prisijungimas prie SQLite duomenų bazės
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Funkcija, kuri patikrina, ar lentelėje jau yra stulpelis, jei ne, prideda jį
        def add_column_if_not_exists(column_name):
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]
            
            if column_name not in columns:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN \"{column_name}\" TEXT")

        # Sukurti lentelę, jei ji dar nesukurta
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)")

        # Patikrinti kiekvieną žodyno raktą (stulpelį), ar jis egzistuoja lentelėje, ir jei ne - pridėti
        for key in data.keys():
            add_column_if_not_exists(key)

        # Paruošti SQL užklausą dinamiškai
        columns = ', '.join(f'"{key}"' for key in data.keys())
        placeholders = ', '.join('?' for _ in data)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Įrašyti duomenis
        cursor.execute(sql, tuple(data.values()))

        # Išsaugoti pakeitimus ir uždaryti ryšį
        conn.commit()
        return conn.close()
    except Exception as e:
        print(e)
        return conn.close()
 
    
def update_row_in_db(db_path, table_name, data, condition_column, condition_value):
    import sqlite3
    """
    Atnaujina konkrečią eilutę SQLite duomenų bazėje pagal nurodytą stulpelį ir jo reikšmę.
    Jei stulpelio nėra, jis pridedamas, tada įrašoma reikšmė į nurodytą eilutę.

    Args:
        db_path (str): Kelias iki SQLite duomenų bazės failo.
        table_name (str): Lentelės pavadinimas, kurioje bus atliekami pakeitimai.
        data (dict): Žodynas, kurio key yra stulpelio pavadinimas, o value - reikšmė, kurią reikia įrašyti.
        condition_column (str): Stulpelio pavadinimas, pagal kurį bus identifikuojama eilutė.
        condition_value (str): Reikšmė, pagal kurią bus atrenkama eilutė.
    """
    # Prisijungiama prie DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Atnaujiname visus nurodytus stulpelius su atitinkamomis reikšmėmis
        for column_name, value in data.items():
            # Tikrinama, ar stulpelis jau egzistuoja
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]
            
            if column_name not in columns:
                # Pridedamas naujas stulpelis, jei jo nėra
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT;")
                print(f"Pridėtas naujas stulpelis: {column_name}")
            
            # Atnaujina konkrečią eilutę pagal sąlygą (condition_column = condition_value)
            cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?;", (value, condition_value))
            print(f"Atnaujinta eilutė, kur {condition_column} = '{condition_value}': nustatyta {column_name} = '{value}'")

        # Išsaugoma ir uždaroma
        conn.commit()

    except sqlite3.Error as e:
        print(f"Klaida vykdant SQL: {e}")
        conn.rollback()
    
    finally:
        conn.close()
        
def query_to_dataframe(db_path, query):
    import sqlite3
    import pandas as pd
    """
    Atlieka SQL užklausą SQLite duomenų bazėje ir grąžina rezultatus kaip pandas DataFrame.

    Args:
        db_path (str): Kelias iki SQLite duomenų bazės failo.
        query (str): SQL užklausa, kurią reikia vykdyti.

    Returns:
        pandas.DataFrame: Užklausos rezultatai kaip DataFrame.
    """
    # Prisijungiama prie duomenų bazės
    conn = sqlite3.connect(db_path)
    
    try:
        # SQL užklausos vykdymas ir rezultatų konvertavimas į DataFrame
        df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        print(f"Klaida vykdant SQL: {e}")
        return None
    finally:
        # Uždaryti ryšį su duomenų baze
        conn.close()
        

def remove_duplicates(db_name, table_name, column_name):
    import sqlite3

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Sukuriame laikiną lentelę be dublikatų
    cursor.execute(f'''
        CREATE TEMPORARY TABLE {table_name}_temp AS
        SELECT * FROM {table_name}
        WHERE rowid IN (
            SELECT MIN(rowid)
            FROM {table_name}
            GROUP BY {column_name}
        );
    ''')

    # Išvalome pradinę lentelę
    cursor.execute(f"DELETE FROM {table_name};")

    # Grąžiname duomenis iš laikinos lentelės atgal į pradinę
    cursor.execute(f'''
        INSERT INTO {table_name}
        SELECT * FROM {table_name}_temp;
    ''')

    # Pašaliname laikiną lentelę
    cursor.execute(f"DROP TABLE {table_name}_temp;")

    # Išsaugome pakeitimus ir uždarome ryšį
    conn.commit()
    conn.close()
    
def remove_table(db_name, table_name):
    import sqlite3

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Ištriname nurodytą lentelę
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    # Išsaugome pakeitimus ir uždarome ryšį
    conn.commit()
    conn.close()


def get_coordinates(address):
    import requests
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": "MyGeolocationApp/1.0 (example@domain.com)"  
    }
    
    response = requests.get(url, params=params, headers=headers)
    a = address
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0].get("lat")
            longitude = data[0].get("lon")
            return float(latitude), float(longitude)
        else:
            print(f"No coordinates found for this address {a}.")
            return None
    else:
        print("Error:", response.status_code)
        return None
    
def save_dataframe_to_sqlite(df, db_name, table_name, if_exists="replace"):
    import sqlite3
    """
    Įrašo DataFrame į SQLite duomenų bazę.

    Args:
        df (pd.DataFrame): Duomenys, kuriuos reikia įrašyti.
        db_name (str): SQLite duomenų bazės failo pavadinimas.
        table_name (str): Lentelės pavadinimas, kur bus įrašyti duomenys.
        if_exists (str): Veiksmas, jei lentelė jau egzistuoja. 
                         Galimi variantai: 'fail', 'replace', 'append'.
                         Numatytoji reikšmė yra 'replace'.

    Returns:
        None
    """
    try:
        # Sukuriamas ryšys su SQLite duomenų baze
        conn = sqlite3.connect(db_name)
        # Duomenų įrašymas į nurodytą lentelę
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        print(f"DataFrame sėkmingai įrašytas į '{db_name}' duomenų bazės '{table_name}' lentelę.")
    except Exception as e:
        print(f"Klaida įrašant DataFrame į SQLite: {e}")
    finally:
        # Uždaromas ryšys su duomenų baze
        conn.close()
        
        
class SimpleAverageRegressor:
    import pandas as pd
    import numpy as np
    def __init__(self):
        self.data = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        import pandas as pd
        import numpy as np
        if not isinstance(X, pd.DataFrame):
            raise ValueError("X turi būti pandas DataFrame objektas.")
        if not isinstance(y, pd.Series):
            raise ValueError("y turi būti pandas Series objektas.")
        
        self.data = X.copy()
        self.data['target'] = y.values

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        import pandas as pd
        import numpy as np
        if self.data is None:
            raise ValueError("Modelis dar nebuvo apmokytas. Naudokite fit() metodą.")

        if not isinstance(X, pd.DataFrame):
            raise ValueError("X turi būti pandas DataFrame objektas.")

        predictions = []
        for _, row in X.iterrows():
            filtered_data = self.data
            for col in X.columns:
                filtered_data = filtered_data[filtered_data[col] == row[col]]

            if not filtered_data.empty:
                predictions.append(filtered_data['target'].mean())
            else:
                predictions.append(np.nan)

        return np.array(predictions)
import sqlite3
import pandas as pd

def add(x, y):
    return x + y 

def divide(x,y):
    return x/y

def multiply(x, y):
    return x*y

def minus(x, y):
    return x -y

def saknis(x):
    if x >0:
        return x**(1/2)

# 1. Funkcija, kuri randa unikalias vertes sąraše    
def unikalus(lst):
    return sorted(list(set(lst)))


# 2. Funkcija, kuri grąžina sąrašą be neigiamų skaičių
def be_neigiamu(lst):
    return [num for num in lst if num >= 0]

# 3. Funkcija, kuri skaičiuoja, kiek kartų kiekvienas elementas pasikartoja sąraše
def kiek_kartu(lst):
    from collections import Counter
    return Counter(lst)


# 4. Funkcija, kuri sujungia du sąrašus į vieną, pašalindama pasikartojančius elementus
def sum_lst(lst1, lst2):
    lst3 = []
    for i in lst1:
        if i not in lst3:
            lst3.append(i)
    for i in lst2:
        if i not in lst3:
            lst3.append(i)
    return lst3


# 5. Funkcija, kuri grąžina sąrašą, kuriame yra tik tie elementai, kurie pasikartoja daugiau nei vieną kartą
def not_unique_lst(lst):
    nunique = []
    from collections import Counter
    diktas = Counter(lst)
    for k, v in diktas.items():
        if v > 1:
            nunique.append(k)
    return nunique

# 6. Funkcijos, kurios apskaičiuoja a) apskritimo plotą b) rutulio tūrį c) rutulio paviršiaus plotą

def apskr_S(r):
    if isinstance(r,int) or isinstance(r, float):
        if r > 0:
            return 3.14 * r**2  
        else:
            raise ValueError('r turi būti teigiamas')
    else:
        raise ValueError('r turi būti int arba float tipo')
    
    
    
def rut_V(r):
    if isinstance(r,int) or isinstance(r, float):
        if r > 0:
            return  round((4 / 3 *3.14 * r**3), 3)  
        else:
            raise ValueError('r turi būti teigiamas')
    else:
        raise ValueError('r turi būti int arba float tipo')
    

def rut_S(r):
    if isinstance(r,int) or isinstance(r, float):
        if r > 0:
            return  round((4 *3.14 * r**2), 3)  
        else:
            raise ValueError('r turi būti teigiamas')
    else:
        raise ValueError('r turi būti int arba float tipo')
    
    
# funkcija, skirta sudėtinių srašų (nested list) plokštinimui (flatten):
#  tarkim, duodami duomenys [1,2,[2,4,5],6,7] ---> rezultatas ---> 1,2,2,4,5,6,7
# Parašyti naudojantis tik ciklus ir if'us, ištestuoti pateikiant įvairius duomenis

def flatten_list(nested_list):
    flatten_lst = []
    for i in nested_list:
        if isinstance(i, int) or isinstance(i, float) or isinstance(i, str):
           flatten_lst.append(i)
        else:
            for j in i:
                flatten_lst.append(j)
    return flatten_lst



#  Parašykite funkcijas ir testus toms funkcijoms:
#  Funkcija turi grąžinti  5kių populiariausių gamintojų sąrašą
#  Funkcija turi surasti vidutines auto kainas (sąrašą) top 5kiems gamintojams.
#  Fukcija turi
#  SVARBU : duomenis turite šioms funkcijoms pateikti iš savo SQLite DB, pasinaudoti setUp metodu. SQLite DB turi pateikti raw duomenis (nerikiuoti, neapdoroti, negrupuoti papildomai).
# pasinaudokite tearDown() metodu - uždarykite SQLite DB po testų.

def get_markes_sql():
    SDB = sqlite3.connect('Auto.db')
    C = SDB.cursor()
    sql="""select Marke, count(*) as k from Autopliuslt
    group by Marke
    order by k DESC
    limit 5;"""
    C.execute(sql)
    ans = C.fetchall()
    markes, kiekiai = list(map(list, zip(*ans)))
    SDB.close()
    return markes


def get_markes_df():
    SDB = sqlite3.connect('Auto.db')
    C = SDB.cursor()
    sql="""select * from Autopliuslt;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)
    df = df_with_dubs.drop_duplicates()
    SDB.close()

    markes = df['Marke'].value_counts().head(5).index.to_list()
    return markes


def get_vid_kaina_top5():
    SDB = sqlite3.connect('Auto.db')
    C = SDB.cursor()
    sql="""select * from Autopliuslt;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)
    df = df_with_dubs.drop_duplicates()
    SDB.close()

    def kaina(x):
        if x != 'None':
            return int(x.replace(' ', ''))
        
    df['price'] = df['Kaina'].apply(kaina)
    markes = get_markes_df()

    df_top = df[df['Marke'].isin(markes)][['Marke', 'price']]
    df_top_gr = df_top.groupby('Marke').mean(numeric_only=True).round().reset_index()
    top_auto = df_top_gr['Marke'].tolist()
    top_kaina = df_top_gr['price'].tolist()

    top_ak = {}
    for a, k in zip(top_auto, top_kaina):
        top_ak[a] = k

    # return top_ak

    kainos = []
    for m in markes:
        k = top_ak[m]
        kainos.append(k)
    
    return kainos

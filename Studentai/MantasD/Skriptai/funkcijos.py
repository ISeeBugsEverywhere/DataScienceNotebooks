def add(x,y):
    return x + y

def divide(x, y):
    return x / y

# pridėkite dar testus daugybai, atimčiai, kv. šaknies traikuimui

def multi(x, y):
    return x * y

def substraction(x, y):
    return x - y

def sakn(x):
    return x**(1/2)

# 1. Funkcija, kuri randa unikalias vertes sąraše
def uniq(x):
    a = list(set(x))
    a.sort()
    return a

# 2. Funkcija, kuri grąžina sąrašą be neigiamų skaičių
def wotneg(x):
    x.sort()
    s = []
    for i in x:
        if i>=0:
            s.append(i)
    return s

# 3. Funkcija, kuri skaičiuoja, kiek kartų kiekvienas elementas pasikartoja sąraše
def countval(x):
    s = {}
    l = list(set(x))
    l.sort()
    for i in l:
        s[i] = x.count(i)
    return s

# 4. Funkcija, kuri sujungia du sąrašus į vieną, pašalindama pasikartojančius elementus
def uniqcon(x, y):
    c = list(set(x+y))
    c.sort()
    return c

# 5. Funkcija, kuri grąžina sąrašą, kuriame yra tik tie elementai, kurie pasikartoja daugiau nei vieną kartą
def countmt1(x):
    s = []
    l = list(set(x))
    l.sort()
    for i in l:
        a = x.count(i)
        if a > 1:
            s.append(i)
    return s

# 6. Funkcijos, kurios apskaičiuoja a) apskritimo plotą b) rutulio tūrį c) rutulio paviršiaus plotą
# a)
def ap_plot(r):
    import math
    return round(math.pi*(r**2),2)

# b)
def rut_V(r):
    import math
    return round(4/3*math.pi*(r**3),2)

# c)
def rut_S(r):
    import math
    return round(4*math.pi*(r**2),2)


#  funkcija, skirta sudėtinių srašų (nested list) plokštinimui (flatten):
#  tarkim, duodami duomenys [1,2,[2,4,5],6,7] ---> rezultatas ---> 1,2,2,4,5,6,7
# Parašyti naudojantis tik ciklus ir if'us, ištestuoti pateikiant įvairius duomenis
def flatten_and_get_unique(lst):
    l = []
    for i in lst:
        if isinstance(i, list):
            l.extend(flatten_and_get_unique(i))
        elif isinstance(i, (int, str)) and i is not None: 
            l.append(i)
    unique_list = sorted(set(l), key=lambda x: (isinstance(x, str), x))
    return unique_list


#  Parašykite funkcijas ir testus toms funkcijoms:
#  Funkcija turi grąžinti  5kių populiariausių gamintojų sąrašą
def get_pop_auto():
    import sqlite3
    conn = sqlite3.connect('../../../web_scrap.db')
    cursor = conn.cursor()

    sql = "SELECT Markė, count(*) as Kiekis FROM autopliuslt2 group by Markė order by Kiekis desc limit 5"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    x, y = list(map(list, zip(*result)))
    return x
#  Funkcija turi surasti vidutines auto kainas (sąrašą) top 5kiems gamintojams.
def get_pop_auto_avg_prices():
    import sqlite3
    conn = sqlite3.connect('../../../web_scrap.db')
    cursor = conn.cursor()

    sql = "SELECT Markė, count(*) as Kiekis, AVG(Kaina) FROM autopliuslt2 group by Markė order by Kiekis desc limit 5"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    x, y, z = list(map(list, zip(*result)))
    return z
#  Fukcija turi
#  SVARBU : duomenis turite šioms funkcijoms pateikti iš savo SQLite DB, pasinaudoti setUp metodu. SQLite DB turi pateikti raw duomenis (nerikiuoti, neapdoroti, negrupuoti papildomai).
# pasinaudokite tearDown() metodu - uždarykite SQLite DB po testų.
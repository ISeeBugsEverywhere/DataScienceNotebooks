import math

# def add(x, y):
#     return x + y

# def divide(x, y):
#     if y == 0:
#         return "Error: Division by zero"
#     return x / y

# def atimtis(x, y):
#     return x - y

# def daugyba(x, y):
#     return x * y

# def saknis(x):
#     return math.sqrt(x)


# 1. Funkcija, kuri randa unikalias vertes sąraše
# 2. Funkcija, kuri grąžina sąrašą be neigiamų skaičių
# 3. Funkcija, kuri skaičiuoja, kiek kartų kiekvienas elementas pasikartoja sąraše
# 4. Funkcija, kuri sujungia du sąrašus į vieną, pašalindama pasikartojančius elementus
# 5. Funkcija, kuri grąžina sąrašą, kuriame yra tik tie elementai, kurie pasikartoja daugiau nei vieną kartą


def unikalios_reiksmes(x):
    reiksmes = set(x)
    return list(reiksmes)


def tik_teigiami(x):
    teigiami = []  
    for i in x:
        teigiami.append(abs(i))  
    return teigiami


def pasikartoijimas(i):
    pasikartojimai = {}
    for y in i:
        if y in pasikartojimai:
            pasikartojimai[y] += 1
        else:
            pasikartojimai[y] = 1 
    return pasikartojimai


def du_sarasai(x, y):
    naujas_sarasas = x + y
    bendras_setas = set(naujas_sarasas)  
    return list(bendras_setas) 


def pasikartojantys(x):
    pasikartojimai = {}
    for i in x:
        if i in pasikartojimai:
            pasikartojimai[i] += 1
        else:
            pasikartojimai[i] = 1    
    pasikartojantys_elementai = []
    for i, skaicius in pasikartojimai.items():
        if skaicius > 1:
            pasikartojantys_elementai.append(i)
    return pasikartojantys_elementai




def plotas_turis_pavirsius(r):
    plotas = math.pi * r ** 2
    turis = (4/3) * math.pi * r ** 3
    pavirsius = 4 * math.pi * r ** 2
    return [plotas, turis, pavirsius]
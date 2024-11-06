def add(x, y):
    return x+y

def atimtis(x ,y):
    return x-y

def daugyba(x, y):
    return x*y

def dalyba(x, y):
    if y==0:
        return 'dalyba is 0 negalima'
    else:
        return x/y
    
def kv_saknis(x):
    if x>=0:
        return x**(1/2)
    else: 
        return 'netinkami duomenys'
    

# 1. Funkcija, kuri randa unikalias vertes sąraše
def unikalios(x:list) -> set:
    return set(x)

# 2. Funkcija, kuri grąžina sąrašą be neigiamų skaičių
def be_neigiamu(x):
    ats = []
    for i in x:
        if (isinstance(i, (int, float)) and i >= 0) or not isinstance(i, (int, float)):
            ats.append(i)
    return ats

# 3. Funkcija, kuri skaičiuoja, kiek kartų kiekvienas elementas pasikartoja sąraše
def pasikartoja(x):
    uni=list(set(x))
    ats={}
    for i in uni:    
        ats[i]=x.count(i)
    return ats

# 4. Funkcija, kuri sujungia du sąrašus į vieną, pašalindama pasikartojančius elementus
def sujungimas(x, y):
    return set(x+y)

# 5. Funkcija, kuri grąžina sąrašą, kuriame yra tik tie elementai, kurie pasikartoja daugiau nei vieną kartą
def pasikartoja(x):
    uni=list(set(x))
    ats=[]
    for i in uni:
        if x.count(i) > 1:
            ats.append(i)          
    return set(ats)

# 6. Funkcijos, kurios apskaičiuoja a) apskritimo plotą b) rutulio tūrį c) rutulio paviršiaus plotą
def apskritimo_plotas(r):
    if r <0:
        return 'spindulys neigiamas'
    else:
        s=round(3.14*r*r, 2)
        return s
def rutulio_turis(r):
    if r <0:
        return 'spindulys neigiamas'
    else:
        v= round(4/3*3.14*r*r*r, 2)
        return v
def pavirsiaus_plotas(r):
    if r < 0:
        return 'spindulys neigiamas'
    else:
        Spav=round(4*3.14*r*r, 2)
        return Spav
    
#  funkcija, skirta sudėtinių srašų (nested list) plokštinimui (flatten):
#  tarkim, duodami duomenys [1,2,[2,4,5],6,7] ---> rezultatas ---> 1,2,2,4,5,6,7
# Parašyti naudojantis tik ciklus ir if'us, ištestuoti pateikiant įvairius duomenis

def flatten(x):
    ats=[]
    for i in x:
        if isinstance(i, list):
            for j in i:
                ats.append(j)
        else:
            ats.append(i)
    return ats
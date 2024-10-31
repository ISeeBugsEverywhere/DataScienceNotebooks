# MyPy nstaliavimas:
# /bin/python3 -m pip install mypy --break-system-packages

# MyPy naudojimas kodo patikrinimui:
# /bin/python3 -m mypy 2024-10-31_duom_tipai.py

def suma(a:str|int,b:str|int):
    print(a+b)
suma(22,33)
suma('22','33')
# suma('22',33) # TypeError: can only concatenate str (not "int") to str

def sfunkcija(s:str):
    s.islower()
    print(s)
sfunkcija('abc')
# sfunkcija(999) # AttributeError: 'int' object has no attribute 'islower'
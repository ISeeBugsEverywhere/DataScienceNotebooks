# MyPy nstaliavimas:
# /bin/python3 -m pip install mypy --break-system-packages

# MyPy naudojimas kodo patikrinimui:
# /bin/python3 -m mypy 2024-10-31_duom_tipai.py

################################################Ę

def suma(a:str|int,b:str|int):
    print(a+b)

suma(22,33)
suma('22','33')
# suma('22',33) # TypeError: can only concatenate str (not "int") to str

################################################

def sfunkcija(s:str):
    s.islower()
    print(s)

sfunkcija('abc')
# sfunkcija(999) # AttributeError: 'int' object has no attribute 'islower'

################################################

#$ /bin/python3 -m mypy 2024-10-31_duom_tipai.py
# 2024-10-31_duom_tipai.py:10: error: Unsupported operand types for + ("str" and "int")  [operator]
# 2024-10-31_duom_tipai.py:10: error: Unsupported operand types for + ("int" and "str")  [operator]
# 2024-10-31_duom_tipai.py:10: note: Both left and right operands are unions
# Found 2 errors in 1 file (checked 1 source file)

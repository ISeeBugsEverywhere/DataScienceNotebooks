# Užduotis 1: Funkcija, kuri tikrina, ar skaičius yra nelyginis
def nelyginis(x:int) -> bool:
    '''
    >>> nelyginis(1)
    True
    >>> nelyginis(2)
    False
    >>> nelyginis('5')
    Traceback (most recent call last):
    TypeError: not all arguments converted during string formatting
    >>> nelyginis()
    Traceback (most recent call last):
    TypeError: nelyginis() missing 1 required positional argument: 'x'
    '''
    if x %2 == 1:
        return True
    else:
        return False
    
    
# Užduotis 2: Funkcija, kuri tikrina, ar skaičius yra teigiamas
def teigiamas(x:int|float) -> bool:
    '''
    >>> teigiamas(15)
    True
    >>> teigiamas(-6)
    False
    >>> teigiamas(0)
    False
    >>> teigiamas('a')
    Traceback (most recent call last):
    TypeError: '>' not supported between instances of 'str' and 'int'
    >>> teigiamas ()
    Traceback (most recent call last):
    TypeError: teigiamas() missing 1 required positional argument: 'x'
    '''
    if x > 0:
        return True
    else:
        return False
    
    
    
# Užduotis 3: Funkcija, kuri tikrina, ar skaičius yra neigiamas
def neigiamas(x:int|float) -> bool:
    '''
    >>> neigiamas(15)
    False
    >>> neigiamas(-6)
    True
    >>> neigiamas(0)
    False
    >>> neigiamas('a')
    Traceback (most recent call last):
    TypeError: '<' not supported between instances of 'str' and 'int'
    >>> neigiamas()
    Traceback (most recent call last):
    TypeError: neigiamas() missing 1 required positional argument: 'x'
    '''
    if x < 0:
        return True
    else:
        return False
    
    
# Užduotis 4: Funkcija, kuri tikrina, ar tekstas yra tuščias
def tuscias(x:None) -> bool:
    '''
    >>> tuscias('')
    True
    >>> tuscias(5)
    False
    >>> tuscias('asd')
    False
    >>> tuscias()
    Traceback (most recent call last):
    TypeError: tuscias() missing 1 required positional argument: 'x'
    '''
    if x == '':
        return True
    else:
        return False
# Užduotis 5: Funkcija, kuri tikrina, ar tekstas prasideda tam tikra raide

def raide(txt:str, r:str) -> bool:
    '''
    >>> raide('Labas', 'l')
    False
    >>> raide('Labas', 'L')
    True
    >>> raide('Labas', 5)
    Traceback (most recent call last):
    TypeError: startswith first arg must be str or a tuple of str, not int
    >>> raide(524554, 'a')
    Traceback (most recent call last):
    AttributeError: 'int' object has no attribute 'startswith'
    '''
    if txt.startswith(r):
        return True
    else:
        return False
# Užduotis 6: Funkcija, kuri suranda pateikto skaičių sąrašo vidurkį (len, sum naudoti viduje)

def sarasas(lst:list) -> float:
    '''
    >>> sarasas([3, 4,5])
    4.0
    >>> sarasas([0])
    0.0
    >>> sarasas(['3', 4 ,5])
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    >>> sarasas([])
    Traceback (most recent call last):
    ZeroDivisionError: division by zero
    '''
    suma = sum(lst)
    ilgis = len(lst)
    vid = suma/ilgis
    return vid

# Funkcija grąžina didžiausią sąrašo elementą.
def did(lst:list) -> float:
    '''
    >>> did([3,6.0,0])
    6.0
    >>> did([3,7,0])
    7
    >>> did([3,'7',0])
    Traceback (most recent call last):
    TypeError: '>' not supported between instances of 'str' and 'int'
    >>> did([])
    Traceback (most recent call last):
    ValueError: max() iterable argument is empty
    '''
    return max(lst)

# Funkcija apverčia duotą eilutę.

def back(string:str) -> str:
    '''
    >>> back('Hello')
    'olleH'
    >>> back('He ll')
    'll eH'
    >>> back(55544)
    Traceback (most recent call last):
    TypeError: 'int' object is not subscriptable
    '''
    return string[::-1]

# Funkcija apskaičiuoja faktorialą.

def factorial(n):
    '''
    >>> factorial(5)
    120
    >>> factorial(6.0)
    Traceback (most recent call last):
    TypeError: 'float' object cannot be interpreted as an integer
    >>> factorial(-5)
    Traceback (most recent call last):
    ValueError: Factorial is not defined for negative numbers
    >>> factorial('a')
    Traceback (most recent call last):
    TypeError: n must be an integer
    '''
    if isinstance(n, str):
        raise TypeError('n must be an integer')
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Funkcija grąžina Fibonacci seką iki n-tosios reikšmės.

def fib(k):
    '''
    >>> fib(7)
    [0, 1, 1, 2, 3, 5, 8]
    >>> fib(0)
    []
    >>> fib('as')
    Traceback (most recent call last):
    TypeError: 'str' object cannot be interpreted as an integer
    '''

    a, b = 0, 1
    s = []
    for i in range(k):
        s.append(a)
        a, b = b, a+b
    return s






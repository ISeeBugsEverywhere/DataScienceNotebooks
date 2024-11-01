import typing as T
def add(x:str, y:str) -> T.Any:    
    return x + y


print(add(5,5))
print(add(5.0,5.0))
print(add('5','5'))

# python -m mypy mypy_demo.py

# python3 -m doctest -v  Notebooks/dctTestt.py
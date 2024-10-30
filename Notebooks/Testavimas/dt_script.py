import doctest

def add(x:int|float,y:int|float):
    """Adds two digits and return a result

    Args:
        x (int|float): int or float
        y (int|float): int or float

    Returns:
        int|float: result
    doctests:
    
    >>> add(6,5)
    11
    >>> add(7,3)
    10
    >>> add('a'+7)
    Traceback (most recent call last):
    TypeError: can only concatenate str (not "int") to str
    """
    return x + y


# doctest.run_docstring_examples(add, globs=globals(), verbose=True)

if __name__ == "__main__":
    doctest.testmod(verbose=True, report=True, globs=globals())
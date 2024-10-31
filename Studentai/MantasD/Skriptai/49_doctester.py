import doctest

def add(x, y):
    '''sums up two digits
    >>> add(1,2)
    3
    >>> add(5,-4)
    1
    >>> add(0,0)
    0
    >>> add(5,'5')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    '''
    return x + y

if __name__ == '__main__':
    doctest.testmod(verbose=True, globs=globals(), report=True)
import doctest

def add(x, y):
    '''
    sum two digits
    >>> add(1,2)
    3
    >>> add(5, -4)
    1
    >>> add(0,0)
    0
    >>> add(5, '5')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    '''
    return x+y


def divide(x, y):
    '''
    >>> divide(2,1)
    2.0
    >>> divide(1,2)
    0.5
    '''
    return x/y

# if __name__ == '__main__':
#     doctest.testmod(verbose=True, globs=globals(), report=True)
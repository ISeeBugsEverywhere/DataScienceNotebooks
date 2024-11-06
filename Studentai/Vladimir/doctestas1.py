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

def is_odd(number):
    """
    >>> is_odd(3)
    True
    >>> is_odd(4)
    False
    """

    return number % 2 != 0

def is_positive(number):
    """
    If a number is pos.
    
    >>> is_positive(5)
    True
    >>> is_positive(-5)
    False
    """

    return number > 0

def is_negative(number):
    """
    If a number is neg.
    
    >>> is_negative(-8)
    True
    >>> is_negative(7)
    False
    """

    return number < 0

def is_empty(text):
    """
    If a string is empty.
    
    >>> is_empty("")
    True
    >>> is_empty("Thursday")
    False
    """
    return text == ''

def starts_with(text, letter):
    """
    >>> starts_with("knife", "k")
    True
    >>> starts_with("laptop", "t")
    False
    """
    return text.startswith(letter)

def average(numbers):
    """
    >>> average([1, 2, 3, 4, 5])
    3.0
    >>> average([100, 200, 300])
    200.0
    """

    return sum(numbers) / len(numbers)

def max_in_list(numbers):
    """
    >>> max_in_list([1, 2, 3, 4])
    4
    >>> max_in_list([-1, -2, -3, -4, -5])
    -1
    """
    return max(numbers)

def reverse(text):
    """
    >>> reverse("laptop")
    'potpal'
    >>> reverse("top")
    'pot'
    """

    return text[::-1]

def factorial(n):
    """
    >>> factorial(0)
    1
    >>> factorial(6)
    720
    """

    s = 1
    for i in range(1,n+1):
        s=s*i
    return s

def fibonacci(k):
    """
    >>> fibonacci(8)
    [0, 1, 1, 2, 3, 5, 8, 13]
    
    """
    
    
    a, b = 0, 1
    s = []
    for i in range(k):
        s.append(a)
        a, b = b, a+b
    return s
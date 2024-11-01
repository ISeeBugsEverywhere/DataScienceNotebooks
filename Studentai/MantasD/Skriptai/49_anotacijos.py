import typing as T
def add(x:str, y:str) -> T.Any:
    return x + y


# print(add(5,5))
# print(add(5.0,5.0))
# print(add('5','5'))

def do(x:T.Iterable) -> None:
    for i in x:
        print(i)
    pass

do([1,2,3])
do('ABC')
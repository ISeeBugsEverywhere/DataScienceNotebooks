import pandas as pd
import numpy as np

# from typing import * #negražu, bet susikeliame visus tipus
#  visgi geriau
import typing as T

#  rašome funkciją:
def addDigits(x:float, y:float) -> float:
    r:float = x + y
    return r

ats = addDigits(1,2)
print(ats)
ats = addDigits('2','2')
print(ats)

def so_text(text:str):
    text.capitalize()
    pass

def doGoodWork(df:pd.DataFrame) -> np.ndarray:
    r : np.ndarray = df.iloc[:,1].values
    return r
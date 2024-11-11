def add(x, y):
    return x+y

def multiply(x, y):
    return x * y

def minus(x, y):
    return x - y

import math
def sqrroot(x, y):
    return x ** (1/2)


def unique_values(lst):
    """
    
    """
    return list(set(lst))

def remove_negatives(lst):
    """
    
    """
    return [x for x in lst if x >= 0]

def count_occurrences(lst):
    """
    
    """
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    return counts

def merge_unique(list1, list2):
    """
    
    """
    return list(set(list1 + list2))

def duplicates(lst):
    """
    
    """
    counts = count_occurrences(lst)
    return [item for item, count in counts.items() if count > 1]

def circle_area(radius):
    """
    
    """
    return math.pi * radius ** 2

def sphere_volume(radius):
    """
    
    """
    return (4/3) * math.pi * radius ** 3

def sphere_surface_area(radius):
    """
    
    """
    return 4 * math.pi * radius ** 2



import sqlite3
import pandas as pd

def car_data(conn):
    df = pd.read_sql_query("select brand, price from car_listings", conn)
    
    df['price'] = df['price'].str.replace(' ', '').str.replace('€', '').astype(float)
    return df

def top_5_brands(conn):
    df = car_data(conn)
    top_5 = df['brand'].value_counts().nlargest(5).index.tolist()
    return top_5


def avg_price_top_5_brands(conn):
    df = car_data(conn)
    top_5 = top_5_brands(conn)
    
    avg_prices = df[df['brand'].isin(top_5)].groupby('brand')['price'].mean().to_dict()
    return avg_prices
import random as r
import string

def str_random(*,len=10) -> str:
    if len <= 0:
        raise ValueError('len attr must be positive')
    return ''.join(r.choices(string.ascii_lowercase,k=len))



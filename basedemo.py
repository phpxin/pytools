# -*- coding: utf-8 -*-


val = 100
val_str = '%d' %val 
print val_str

val2 = 100.56
val2_str = '%lf' %val2
print val2_str


def parseInt(_num_str):
    
    _num_str = _num_str.strip()
    
    num = -1

    try:
        num = int(_num_str)
    except ValueError:
        num = -1
        pass
    
    return num

str1 = '10011  '
a = parseInt(str1)
print a
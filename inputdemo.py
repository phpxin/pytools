# -*- coding: utf-8 -*-


def func1():
    return 'hello'

while True:
    a = ''
    try:
        a = input()
        print a
        
    except Exception:
        print '输入错误'
    
    if a == 'q':
        break
    
    pass


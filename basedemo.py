# -*- coding: utf-8 -*-

num = [0,1,2,3,4]

print len(num)
num.remove(1)

print len(num)
print num[1]


exit()

str1 = "查看地图"

str1.encode('utf-8')

print str1

exit()

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
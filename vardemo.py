# -*- coding: utf-8 -*-

'''
b = 1
print 'b id is ', id(b) # b id is  34899544
b = 2
print 'b id is ', id(b) # b id is  34899520
maptest = dict()
print 'dict id is ', id(maptest)    # dict id is  40449160
maptest = dict()
print 'dict id is ', id(maptest)    # dict id is  40449432

exit()
'''

a = 1

map1 = dict()

map1['name'] = 'lx'

def change():
    global a  #   引用外部变量地址，这里对a修改，外部会修改
    print 'inside a id is ', id(a) , ' a is ', a
    a = 2
    global map1
    map1 = dict()
    map1['name'] = 'lucy'
    print 'inside a change id is ', id(a), ' a is ', a
    print 'inside map1 change id is ', id(map1), ' name is ', map1['name']
    return


print 'outside a id is ', id(a) , ' a is ', a
print 'outside map1 id is ', id(map1), ' name is ', map1['name']

change()

print 'outside a id is ', id(a), ' a is ', a
print 'outside map1 id is ', id(map1), ' name is ', map1['name']

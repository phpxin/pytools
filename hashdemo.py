# -*- coding: utf-8 -*-
import hashlib

persons = ['lx', 'lucy', 'jack']

persons_hash = []


for _item in persons :
    m2 = hashlib.md5()   
    m2.update(_item)
    hashstr = m2.hexdigest().upper()
    persons_hash.append(hashstr)
    pass

my = 'lx1'
m2 = hashlib.md5()   
m2.update(my)
sign = m2.hexdigest().upper()

exist = False

try:
    _index = persons_hash.index(sign)
    print '在位置 ' + ('%d' %_index) + ' 找到'
    exist = True
except ValueError:
    # 如果值不存在则会抛出这个异常
    print '未找到 ' + my
    exist = False

if exist :
    print my + ' 存在列表' 
else :
    print my + ' 不存在列表'

    


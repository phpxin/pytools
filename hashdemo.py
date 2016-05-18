# -*- coding: utf-8 -*-
import hashlib


m2 = hashlib.md5()
m2.update('lx')         
print m2.hexdigest()

m2.update('lb')         #每次update 会把这个字符串追加到需要生成的字符串末尾，所以hashlib.md5()每次必须重新声明
print m2.hexdigest()

m3 = hashlib.md5()
m3.update('lb')
print m3.hexdigest()

print hashlib.md5().update('lb').hexdigest()

exit()

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

    


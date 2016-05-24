# -*- coding: utf-8 -*-
'''
正则表达式
'''

import re

target_str = '\
    <img src="http://maps.google.cn/maps/api/staticmap?zoom=12&size=270x180&markers=icon:http://static.qyer.com/images/place5/icon_mapno_big.png|35.715038,139.796799&sensor=false">\
    <img src="http://maps.google.cn/maps/api/staticmap?zoom=12&size=270x180&markers=icon:http://static.qyer.com/images/place5/icon_mapno_big.png|35.7138,13.796799&sensor=false">\
    '
reg_str = "http\:\/\/maps\.google\.cn.*?\|(.*?)\,(.*?)\&sensor\=false"

f_iter = re.finditer(reg_str, target_str, re.I)
print f_iter
for item in f_iter :
    print item.group()
    print item.groups()
    pass

'''
<callable-iterator object at 0x0000000002184588>
http://maps.google.cn/maps/api/staticmap?zoom=12&size=270x180&markers=icon:http://static.qyer.com/images/place5/icon_mapno_big.png|35.715038,139.796799&sensor=false
('35.715038', '139.796799')
http://maps.google.cn/maps/api/staticmap?zoom=12&size=270x180&markers=icon:http://static.qyer.com/images/place5/icon_mapno_big.png|35.7138,13.796799&sensor=false
('35.7138', '13.796799')
'''

f_all = re.findall(reg_str, target_str, re.I)
print f_all

'''
[('35.715038', '139.796799'), ('35.7138', '13.796799')]
'''

exit()

pattern = re.compile(reg_str, re.IGNORECASE|re.MULTILINE)

print pattern

searchobj = pattern.search(target_str)
print searchobj

if searchobj :
#     print searchobj
    print searchobj.group()
    print searchobj.groups()
else:
    print 'no match'

matchobj = pattern.match(target_str)
#print matchobj # None
if matchobj:
    print matchobj
else:
    print 'no match'

target_str2 = 'http://maps.google.cn/maps/api/staticmap?zoom=12&size=270x180&markers=icon:http://static.qyer.com/images/place5/icon_mapno_big.png|35.715038,139.796799&sensor=false'
pattern2 = re.compile(reg_str)
matchobj2 = pattern2.match(target_str2)
if matchobj2 :
    print matchobj2
    print matchobj2.group()
    print matchobj2.groups()
    
else:
    print 'no match'


'''
#  测试1
s = 'aaaa111bbbdddd222211aaacc2200'


p = re.compile("\d+")
m = p.match(s)
print p
'''

'''
m = re.match('\d+', s)
print m
'''

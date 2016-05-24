# -*- coding: utf-8 -*-

'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''

'''
str_unicode = u'你好世界'
print str_unicode

dict1 = {'k':u'你好世界'}
print dict1 # {'k': u'\u4f60\u597d\u4e16\u754c'}

dict2 = {'k':'你好世界'}
print dict2 # {'k': '\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c'}
'''



str1 = "你好世界"
str1 = str1.decode('utf-8')
dict3 = {'k':str1}  # {'k': u'\u4f60\u597d\u4e16\u754c'}     将ascii字符串解码为unicode字符
print dict3

str2 = u"你好师姐"
#str2 = str2.encode('gbk')   # {'k': '\xc4\xe3\xba\xc3\xca\xa6\xbd\xe3'}    编码成ascii字符，两字节为一汉字
str2 = str2.encode('utf-8')   # {'k': '\xe4\xbd\xa0\xe5\xa5\xbd\xe5\xb8\x88\xe5\xa7\x90'}    编码成ascii字符，三字节为一汉字
dict4 = {'k':str2}
print dict4

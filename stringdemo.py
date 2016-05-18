# -*- coding: utf-8 -*-
from _codecs import decode

a = "aaaa'aaaaa"

a = a.replace("'", "\'")

print a



exit()

str1 = decode(u'\u5580\u5e03\u5c14\xa0\xa0')

print str1
exit()

dictstr = {'url': [u'http://place.qyer.com/kabul/'], 'en': [u'Kabul'], 'name': [u'\u5580\u5e03\u5c14\xa0\xa0', u'\r\n                        '], 'img': [u'http://pic1.qyer.com/album/user/331/55/QkpURx8AaA/index/cover']}



print dictstr

exit()


country = 'http://place.qyer.com/afghanistan/'
country = country.strip('/') + '/1000'
print country
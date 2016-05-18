# -*- coding: utf-8 -*-

'''
fp = open('./qy_countrys.html');

html = fp.readlines();

print "total " ,  len(html) , " lines \nparseing ..."
#print html;

'''
from urllib2 import urlopen


response = urlopen('http://localhost/Demos/qy_countrys.html')
#print request.read()

asia = response.selector.xpath('//*[@id="Asialist"]').extract()
print asia
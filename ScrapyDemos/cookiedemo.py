# -*- coding: utf-8 -*-
import urllib2
from test.test_mimetools import mimetools
from httplib import HTTPConnection
import httplib
from Cookie import BaseCookie, SimpleCookie
from _cffi_backend import string


'''
GET /poi/V2MJYFFvBzZTZQ/ HTTP/1.1
Host: place.qyer.com
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36
Referer: http://place.qyer.com/singapore/alltravel/
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
Cookie: _guid=808cd39f-041d-f9b4-2787-fe51360d00ed; isnew=1463377186956; isDoLogin=828; _isNeverShowBigTip=true; qy_topad=1; PHPSESSID=efc4faea421e361ffc2e6e5c8d3d2d77; __utmt=1; city_browse=a%3A3%3A%7Bi%3A0%3Bi%3A62%3Bi%3A1%3Bi%3A6794%3Bi%3A2%3Bi%3A9201%3B%7D; _session=1463450681820; __utma=253397513.1948428908.1463377179.1463381477.1463450682.4; __utmb=253397513.46.9.1463454493151; __utmc=253397513; __utmz=253397513.1463377179.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)

'''



conn = httplib.HTTPConnection('localhost')
conn.request('GET', '/info.php', '', {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"})  #, body, headers

response = conn.getresponse(True)

cookie = response.getheader('Set-Cookie', '')

print cookie
print response.read()
print '\n' 

req_cookie = []

cookieObj = SimpleCookie()
cookieObj.load(cookie)

for i in cookieObj.iteritems() :
    req_cookie.append(i[1].key + "=" + i[1].value)

req_cookie = "; ".join(req_cookie)   

print req_cookie, '\n'

conn2 = httplib.HTTPConnection('localhost')
conn2.request('GET', '/arrdemo.php', '', {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                                         "Cookie": req_cookie})

response = conn2.getresponse(True)

print response.read(), '\n'




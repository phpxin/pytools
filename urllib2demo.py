# -*- coding: utf-8 -*-
import urllib2

# urllib2.urlopen(url[, data[, timeout[, cafile[, capath[, cadefault[, context]]]]]) 

# fp = urllib2.urlopen('http://localhost/pydemo.php', "name=lixin&age=23")
# print fp.read()

# class urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable]) 



req = urllib2.Request('http://localhost/pydemo.php', "name=lixin111&age=23")
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')
req.add_header('Uthing-Data', 'ios; 4.4.2; 4.1.1')
# req.

fp = urllib2.urlopen(req) 

# urllib2.

# ss = req.get_header('User-Agent')
# print ss

print fp.read() 




'''

opener = urllib2.build_opener()
opener.add_handlers = [
                       ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36') ,
                       ('Uthing-Data', 'ios; 4.4.2; 4.1.1')
                       ]

opener.open('http://localhost/pydemo.php', "name=bbqq&age=23", 60) 


'''
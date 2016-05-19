# -*- coding: utf-8 -*-
import httplib
from urllib import urlencode

params = urlencode({'page': 100, 
                    'type': 'city', 
                    'pid': 6343,
                    'sort':0,
                    'subsort':'all',
                    'isnominate':-1,
                    'haslastm':'false',
                    'rank':0})

headers = {"Content-type": "application/x-www-form-urlencoded", 
           "Accept": "text/plain"}

conn = httplib.HTTPConnection('place.qyer.com')
s = conn.request('POST', '/poi.php?action=list_json', params, headers)

response = conn.getresponse(True)
print response.read()

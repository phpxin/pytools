# -*- coding: utf-8 -*-
import json
'''
li = []

json_li = json.dumps(li)
print json_li

exit()
'''
li = [
        {'k':'name', 'v':"lx's".replace("'", '')},
        {'k':'age', 'v':23}
      ]

print li

json_li = json.dumps(li)        # 编码成json
print json_li

li2 = json.loads(json_li)       # 解码json串
print li2

for item in li2:
    print item['k'] , '=', item['v']

exit()

# json美化
jsonobj = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
s = json.dumps(jsonobj, sort_keys=True, indent=4, separators=(',', ': '))
print s
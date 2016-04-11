# -*- coding: utf-8 -*-
import json


jsonobj = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')


s = json.dumps(jsonobj, sort_keys=True, indent=4, separators=(',', ': '))


print s
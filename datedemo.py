# -*- coding: utf-8 -*-
import time
import datetime

print time.strftime('%Y-%m-%d %H:%M:%S')

print time.strftime('%m%d')


dt = datetime.datetime(2006, 6, 14) 
print dt.date()

print time.ctime(1461317076)


print int(time.time())
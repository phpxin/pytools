# -*- coding: utf-8 -*-
import random
import time
import datetime


numbs = list()

for i in range(1000):
    numbs.append(random.randrange(0, 10000))
    pass

start = time.time()
print time.strftime('%Y-%m-%d')
print 'start at ' , start
#datetime.
print numbs
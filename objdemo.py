# -*- coding: utf-8 -*-
import string

#a = 'aaa\nbbb'


'''
a = 3.1415926
s = '%f' %a
print s     #3.141593
s2 = '%.2f' %a
print s2    #3.14
'''


s = '3.14'
a = string.atof(s)
print a




'''
from time import ctime,sleep

def funcTest(func):
    def wrappedFunc():
        t_start = ctime()
        ret = func()
        t_end = ctime()
        print 'exec ', t_start , ' - ' , t_end , ' time .'
        return ret
    
    return wrappedFunc


@funcTest
def foo():
    sleep(1)
    print 'hahahaha'
    return

foo()


'''




'''
class demo:
    def __init__(self, age):
        self.age = age
        return
    
    def say(self):
        print 'my age is ', self.age
        return
    
    @staticmethod
    def run():
        print 'i`m running'
        return
    pass


d = demo(21)
d.say()

demo.run()

'''
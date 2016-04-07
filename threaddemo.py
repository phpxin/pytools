# -*- coding: utf-8 -*-
import thread

thisexit = False

def thr_callback(name,age):
    global thisexit
    print 'name is ', name, ' age is ', age
    
    thisexit = True
    thread.exit_thread()
    return

# thread.start_new_thread(thr_callback, tuple(('lx', 27)))
thread.start_new_thread(thr_callback, tuple(), dict({'name':'lx', 'age':27}))

while not thisexit :
    pass



# -*- coding: utf-8 -*-

from socket import socket
from _socket import AF_INET, SOCK_STREAM
from common import config
import thread

'''
多线程 Echo 服务器
cd C:\Users\Administrator\hd_workspace\pythondemos
'''

close_serv = False

def new_thread(conn,ok):
    global close_serv
    while True:
        try:
            data = conn.recv(1024)
        except Exception as e:
            print "exception: {}".format(e)
            break
    
        if not data:
            print 'data is null'
        
        if data == 'exit':
            break
        
        if data == 'close_serv':
            print 'close server command is called'
            close_serv = True
        
        print 'data is ', data 
        
        conn.sendall('echo : ' + data)
    
    print 'prepare close connection and exit thread'
    conn.close()
    thread.exit()
    pass

serv = socket(AF_INET, SOCK_STREAM)
if serv==0 :
    print 'create socket failed'
    exit
    pass
    
serv.bind((config.HOST, config.PORT))

serv.listen(5)


while not close_serv:

    conn, addr = serv.accept()
    
    print 'connect by ', addr 
    
    if close_serv:
        break
    
    try:
        thread.start_new_thread(new_thread, (conn,False))
    except Exception as e:
        print "exception: {}".format(e)
        break
    
    
    pass

serv.close()

print 'socket server is closed .'
    

    
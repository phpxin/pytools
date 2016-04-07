# -*- coding: utf-8 -*-

import socket
import common.config


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((common.config.HOST, common.config.PORT))

while True:
    istr = ''
    istr = raw_input()      #raw_input 读入字符串，input 
    
    if istr == 'exit':
        break
    
    s.sendall(istr)
    data = s.recv(1024)
    print 'Received', repr(data)

s.close()
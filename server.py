#!/usr/bin/python
#*-* coding: utf-8*-*

from socket import *
s=socket(AF_INET,SOCK_STREAM)
s.bind(('',8282))
s.listen(1)
print ('connect waiting.....')
conn, addr = s.accept()
print ('connected by',addr)

start_string = '잘받아라 '


while 1:
        data = conn.recv(4096)
        if not data:
                break
        print ('recive_data:',data)
        conn.send(start_string.encode() + data)

conn.close()
s.close()
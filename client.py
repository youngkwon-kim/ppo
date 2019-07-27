#!/usr/bin/python
#*-* coding: utf-8 *-*
from socket import *

HOST='127.0.0.1'

c = socket(AF_INET, SOCK_STREAM)
print ('connecting....')
c.connect((HOST,8282))
print ('ok')
while 1:
        data = input('문장을 입력해주세요 : ')
        data = data + "<End>"
        if data:
                c.send(data.encode())
        else:
                continue
        rcdata = c.recv(2048)
        dd = rcdata.decode('utf-8')
        print ('recive_data : ',dd)
c.close()
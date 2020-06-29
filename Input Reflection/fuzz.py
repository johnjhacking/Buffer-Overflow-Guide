#!/usr/bin/python
from __future__ import print_function
import sys, socket
from time import sleep

buffer = "A" * 100

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('10.0.0.71',31337))

                s.send((buffer + '\n'))
                s.close()
                sleep(1)
                buffer = buffer + "A"*100

        except:
                print("Fuzzing crashed at %s bytes" % str(len(buffer)))

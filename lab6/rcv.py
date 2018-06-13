#!/usr/bin/python3

from socket import *
from string import *

# Create socket and bind to address
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(("", 1964))

# Receive messages
while True:
    data, addr = UDPSock.recvfrom(1964)
    if not data:
        print("Program has exited!")
        break
    else:
        print(addr[0], data.decode())
# end while

UDPSock.close()

#!/usr/bin/python3

import socket


def snd(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(data, ('255.255.255.255', 1964))
    s.close()


# end def

# Send messages

while True:
    data = input('>>')
    if not data:
        break
    else:
        snd(data.encode())
    # end if
# end while

from threading import Thread
import time
import random
import sys
import socket
import string


class Node(Thread):

    def __init__(self, n):
        self.n = n
        Thread.__init__(self)

    def run(self):
        # for i in range(20):
        #     time.sleep(random.random())
        #     print(self.n, end="")
        #     sys.stdout.flush()
        if self.n == 0:

            def snd(data):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.sendto(data, ('255.255.255.255', 1964))
                s.close()

            # end def

            # Send messages

            while True:
                data = input()
                if not data:
                    break
                else:
                    snd(data.encode())
        else:

            # Create socket and bind to address
            UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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


w1 = Node(0)
w2 = Node(1)

w1.start()
w2.start()

w1.join()
w2.join()
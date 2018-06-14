from threading import Thread
import time
import sys
import random


def printxy(x, y, s):
    print("\033[" + str(y + 1) + ";" + str(x + 1) + "f" + s)


printxy(1, 2, "xd")

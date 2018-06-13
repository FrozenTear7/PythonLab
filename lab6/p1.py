import os
import re
import time
import sys

lifeline = re.compile(r"(\d) received")
report = ("No response", "Partial Response", "Alive")

print(time.ctime())

for host in range(50, 70):
    ip = "192.168.1." + str(host)
    pingaling = os.popen("ping -q -c2 " + ip, "r")
    print("Status from ", ip, end='')
    sys.stdout.flush()
    while True:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(lifeline, line)
        if igot:
            print(" is ", report[int(igot[0])])

print(time.ctime())

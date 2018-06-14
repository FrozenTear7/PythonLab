# Author: Paweł Mendroch

import yaml
from socket import *
from tkinter import *
from tkinter.ttk import *

# set IP and PORT
UDP_IP = '255.255.255.255'
UDP_PORT = 2018


# return yaml from the file
def getYamlData():
    with open('test.yaml', 'r', encoding='utf-8') as stream:
        return yaml.load(stream)


data = getYamlData()

# open tkinter window
window = Tk()
window.title('Virtual remote')

tab_control = Notebook(window)

# iterate through rooms from yaml data
for room in data:
    # for each room iterate through room's items and create a tab
    for roomName in room:
        tab = Frame(tab_control)
        tab_control.add(tab, text=roomName)

        j = 0
        # for each item create an entry of item's description and buttons ON / OFF to send UDP
        for item in room[roomName]:
            lbl1 = Label(tab, text=room[roomName][item])
            lbl1.grid(column=0, row=j)


            def sendOn():
                MESSAGE = 'on ' + item
                sock = socket(AF_INET, SOCK_DGRAM)
                sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                sock.sendto(bytes(MESSAGE, 'utf-8'), (UDP_IP, UDP_PORT))


            def sendOff():
                MESSAGE = 'off ' + item
                sock = socket(AF_INET, SOCK_DGRAM)
                sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                sock.sendto(bytes(MESSAGE, 'utf-8'), (UDP_IP, UDP_PORT))


            btn = Button(tab, text='ON', command=sendOn)
            btn.grid(column=1, row=j)
            btn = Button(tab, text='OFF', command=sendOff)
            btn.grid(column=2, row=j)

            j += 1

tab_control.pack(expand=1, fill='both')

window.mainloop()

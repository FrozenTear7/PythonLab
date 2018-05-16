import socket
import time
import datetime
from xml.dom import minidom

buf = []


def get_meteo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("meteo.ftj.agh.edu.pl", 80))
    s.send(b"GET /meteo/meteo.xml\n")
    d = s.recv(1024).decode()
    s.close()
    return d


def parse_xml(data):
    t = {}
    xmldoc = minidom.parseString(data)
    meteo = xmldoc.getElementsByTagName("meteo")[0]
    for d in meteo.childNodes:
        for c in d.childNodes:
            if c.nodeType == minidom.Node.ELEMENT_NODE:
                t[c.nodeName] = c.childNodes[0].nodeValue.split()[0]
    return t


def get_temp():
    return float(parse_xml(get_meteo())["ta"])


def avg(f):
    def newElem():
        x = f()
        buf.append(x)
        if len(buf) > 5:
            buf.pop(0)
        s = 0
        for i in buf:
            s += i
        return s / len(buf)

    return newElem()


while True:
    t = get_temp()
    t2 = avg(get_temp)
    f = open("data.txt", "a")
    f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    f.write(" - {0:4.1f}, avg - {1:6.2f}\n".format(t, t2))
    f.close()
    time.sleep(60)

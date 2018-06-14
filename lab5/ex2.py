from matplotlib import pylab

l = []

f = open("data.txt", "r")

for x in f:
    l.append(float(x.split()[0]))

f.close()

pylab.plot(l)
pylab.savefig("wykres.png")
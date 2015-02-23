import numpy as np
import subprocess
from random import *
from time import sleep

class grapher(object):
    np = __import__('numpy')
    subprocess = __import__('subprocess')
    graphOutput = []
    x = []
    y = []    
    graphSize = 30

    def __init__(self, y):
        #self.gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #gnuplot.stdin.write("set term dumb 79 25\n")
        #gnuplot.stdin.write("plot '-' using 1:2 title 'Line1' with linespoints \n")
        for i in range(self.graphSize):
            self.x.append(i)
        #print self.x
        self.y = y
        self.update(self.x,self.y)
        self.graphOutput = self.getGraph()

    def update(self, x, y):
#        print self.x
        self.gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.gnuplot.stdin.write("set term dumb 150 25\n")
        self.gnuplot.stdin.write("plot '-' using 1:2 title 'Line1' with linespoints \n")
        for i,j in zip(x,y):
            self.gnuplot.stdin.write("%f %f\n" % (i,j))    
        self.gnuplot.stdin.write("e\n")
        self.gnuplot.stdin.flush()
        i = 0
        output = []
        while self.gnuplot.poll() is None:
            output.append(self.gnuplot.stdout.readline())
            i+=1
            if i == 24:
                break
        self.graphOutput = output
#        print self.x

    def getGraph(self):
#        print self.x
        return self.graphOutput

    def getValues(self):
#        print self.x
        return zip(self.x,self.y)

    def append(self, yVal):
        #print "t"
#        print(len(self.x))
#        print(len(self.y))
#        print self.y
        if len(self.x) == len(self.y):
            tempX = self.x
            tempY = self.y

            self.y = np.delete(self.y, 0)

            #del self.y[0]
            self.y = np.append(self.y, yVal)
        else:
            if len(self.x) > len(self.y):
                self.y = np.append(self.y, yVal)
#        self.y = np.append(self.y, yVal)
#        print self.x
#        print self.y
        self.update(self.x, self.y)        

y=[0,1]
grapher = grapher(y)
graph = grapher.getGraph()
for line in graph:
    print line
for i in range(5000):
    grapher.append(randrange(-10,10))
    graph = grapher.getGraph()
    for line in graph:
        print line
    sleep(.01)
    

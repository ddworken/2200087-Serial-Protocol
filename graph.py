import numpy as np
import subprocess


class grapher(object):
    np = __import__('numpy')
    subprocess = __import__('subprocess')
    graphOutput = []
    x = []
    y = []

    def __init__(self, x, y):
        #self.gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #gnuplot.stdin.write("set term dumb 79 25\n")
        #gnuplot.stdin.write("plot '-' using 1:2 title 'Line1' with linespoints \n")
        self.updateGraph(x,y)
        self.graphOutput = self.getGraph()
        self.x = x
        self.y = y
#        print self.graphOutput

    def updateGraph(self, x, y):
        self.gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.gnuplot.stdin.write("set term dumb 79 25\n")
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

    def getGraph(self):
        return self.graphOutput

    def graphAppend(self, xVal, yVal):
        #self.x.append(xVal)
        self.x = np.append(self.x, xVal)
        self.y = np.append(self.y, yVal)
        self.updateGraph(self.x, self.y)


x=np.linspace(0,2*np.pi,10)
y=np.sin(x)
grapher = grapher(x,y)
graph = grapher.getGraph()
for line in graph:
    print line
grapher.graphAppend(1,2)
graph = grapher.getGraph()
for line in graph:
    print line

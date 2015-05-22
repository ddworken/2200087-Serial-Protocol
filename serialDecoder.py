import numpy as np
import subprocess
from random import *
from time import sleep
import serial
import argparse
import sys

class grapher(object):
    np = __import__('numpy')
    subprocess = __import__('subprocess')
    graphOutput = [] 					#a list of strings to store the graph in
    x = []						#a list to store 100 most recent X values in
    y = []    						#a list to sore 100 most recent Y values in
    graphSize = 100					#an integer defining the maximum number of data points to track
    							#set graphSize to the number of seconds of data you want displayed * 10 (b/c serial sends values at 10 hz)
    def __init__(self, y):
        for i in range(self.graphSize):
            self.x.append(i)
        self.y = y
        self.update(self.x,self.y)
        self.graphOutput = self.getGraph()
        
    def update(self, x, y, label='DMM'):									#reimplementation of update method to allow setting label
        self.x = x
        self.y = y
        self.gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.gnuplot.stdin.write("set term dumb 150 25\n")
        self.gnuplot.stdin.write("plot '-' using 1:2 title '" + label + "' with linespoints \n")
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


    def getGraph(self):					#return a list of lines that when printed out show a graph
        return self.graphOutput

    def getValues(self):				#return a list of x,y value pairs (that are currently on the graph)
        return zip(self.x,self.y)

    def append(self, yVal):				#append a yValue to the graph
        if len(self.x) == len(self.y):			#if we already graphSize variables, then delete the oldest value and add the newest
            tempX = self.x
            tempY = self.y
            self.y = np.delete(self.y, 0)
            self.y = np.append(self.y, yVal)
        else:
            if len(self.x) > len(self.y):
                self.y = np.append(self.y, yVal)
        self.update(self.x, self.y)  

    def appendWithLabel(self, yVal,label):
        if len(self.x) == len(self.y):
            tempX = self.x
            tempY = self.y
            self.y = np.delete(self.y, 0)
            self.y = np.append(self.y, yVal)
        else:
            if len(self.x) > len(self.y):
                self.y = np.append(self.y, yVal)
        self.update(self.x, self.y, label)
      

def getArrFromStr(serialData): #converts serial data to an array of strings each of which is a binary representation of a single byte
    output = []
    inputList = serialData.split(" ")
    for value in inputList:
        binStr = bin(int(value, base=16))[2:] #The [2:] removes the first 2 characters so as to trim off the 0b
        for i in range(8-len(binStr)):#we add enough 0s to the front in order to make it 8 bytes (since bin() trims off zeros in the start)
            binStr = '0' + binStr
        output.append(binStr)
    return output

def processDigit(digitNumber, binArray):
    decimalPointBool = False
    digitValue = -1 #Allows easy detection of failed digit detection
    bin = []
    if digitNumber == 4:
        bin.append(binArray[2][::-1]) #reverse it because we want to start with bit 0, not bit 7
        bin.append(binArray[3][::-1]) #reverse it because we want to start with bit 0, not bit 7
    if digitNumber == 3:
        bin.append(binArray[4][::-1]) #reverse it because we want to start with bit 0, not bit 7
        bin.append(binArray[5][::-1]) #reverse it because we want to start with bit 0, not bit 7
    if digitNumber == 2:
        bin.append(binArray[6][::-1]) #reverse it because we want to start with bit 0, not bit 7
        bin.append(binArray[7][::-1]) #reverse it because we want to start with bit 0, not bit 7
    if digitNumber == 1:
        bin.append(binArray[8][::-1]) #reverse it because we want to start with bit 0, not bit 7
        bin.append(binArray[9][::-1]) #reverse it because we want to start with bit 0, not bit 7
    digitDict = {}
    digitDict['A'] = int(bin[0][0]) #Creates a dictionary where the key;s follow the protocol description in readme.md
    digitDict['F'] = int(bin[0][1])
    digitDict['E'] = int(bin[0][2])
    digitDict['B'] = int(bin[1][0])
    digitDict['G'] = int(bin[1][1])
    digitDict['C'] = int(bin[1][2])
    digitDict['D'] = int(bin[1][3])
    digitValue = getCharFromDigitDict(digitDict) #passes the digit dict to getCharFromDigitDict to decode what the value is
    decimalPointBool = bool(int(bin[0][3])) #checks if there should be a decimal point
    if digitNumber == 4: #if it is digit 4, a decimal point actually means MAX not decimal point (see readme.md for full description of protocol)
        decimalPointBool = False
    return (decimalPointBool, digitValue) #Returns a tuple containing both whether or not to include a decimal point and the digit on the display

def getCharFromDigitDict(digitDict): #Returns a char based off of the digitDictionary sent to it
    if is9(digitDict):
        return 9
    if is8(digitDict):
        return 8
    if is7(digitDict):
        return 7
    if is6(digitDict):
        return 6
    if is5(digitDict):
        return 5
    if is4(digitDict):
        return 4
    if is3(digitDict):
        return 3
    if is2(digitDict):
        return 2
    if is1(digitDict):
        return 1
    if is0(digitDict):
        return 0
    if isC(digitDict):
        return 'C'
    if isF(digitDict):
        return 'F'
    if isE(digitDict):
        return 'E'
    if isP(digitDict):
        return 'P'
    if isN(digitDict):
        return 'N'
    if isL(digitDict):
        return 'L'

#All of these is*(digitDict) methods are essentially implementing a bitmask to convert a series of bits into characters or numbers
#While this is a horrible format, it works and is unlikely to be changed as switching to a more traditional bitmask is not that advantageous

def isE(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 0 and digitDict['C'] == 0 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False

def isN(digitDict):
    if digitDict['A'] == 0 and digitDict['F'] == 0 and digitDict['G'] == 1 and digitDict['B'] == 0 and digitDict['C'] == 1 and digitDict['D'] == 0 and digitDict['E'] == 1:
        return True
    return False

def isL(digitDict):
    if digitDict['A'] == 0 and digitDict['F'] == 1 and digitDict['G'] == 0 and digitDict['B'] == 0 and digitDict['C'] == 0 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False

def isP(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 1 and digitDict['C'] == 0 and digitDict['D'] == 0 and digitDict['E'] == 1:
        return True
    return False

def isF(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 0 and digitDict['C'] == 0 and digitDict['D'] == 0 and digitDict['E'] == 1:
        return True
    return False

def isC(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 0 and digitDict['B'] == 0 and digitDict['C'] == 0 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False

def is9(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 1 and digitDict['E'] == 0:
        return True
    return False

def is8(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False

def is7(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 0 and digitDict['G'] == 0 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 0 and digitDict['E'] == 0:
        return True
    return False

def is6(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 0 and digitDict['C'] == 1 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False

def is5(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 0 and digitDict['C'] == 1 and digitDict['D'] == 1 and digitDict['E'] == 0:
        return True
    return False

def is4(digitDict):
    if digitDict['A'] == 0 and digitDict['F'] == 1 and digitDict['G'] == 1 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 0 and digitDict['E'] == 0:
        return True
    return False

def is3(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 0 and digitDict['G'] == 1 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 1 and digitDict['E'] == 0:
        return True
    return False

def is2(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 0 and digitDict['G'] == 1 and digitDict['B'] == 1 and digitDict['C'] == 0 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False

def is1(digitDict):
    if digitDict['A'] == 0 and digitDict['F'] == 0 and digitDict['G'] == 0 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 0 and digitDict['E'] == 0:
        return True
    return False

def is0(digitDict):
    if digitDict['A'] == 1 and digitDict['F'] == 1 and digitDict['G'] == 0 and digitDict['B'] == 1 and digitDict['C'] == 1 and digitDict['D'] == 1 and digitDict['E'] == 1:
        return True
    return False


def strToFlags(strOfBytes): #Checks all possible flags that might be needed and returns a list containing all currently active flags
    flags = []
    binArray = getArrFromStr(strOfBytes)
    for index,binStr in enumerate(binArray):
        binArray[index] = binStr[::-1]
    if binArray[0][2] == '1':
        flags.append('AC')
    #if binArray[0][1] == '1': ###Don't display this because it will always be on since whenever we are getting input, it will be on.
    #   flags.append('SEND')
    if binArray[0][0] == '1':
        flags.append('AUTO')
    if binArray[1][3] == '1':
        flags.append('CONTINUITY')
    if binArray[1][2] == '1':
        flags.append('DIODE')
    if binArray[1][1] == '1':
        flags.append('LOW BATTERY')
    if binArray[1][0] == '1':
        flags.append('HOLD')
    if binArray[10][0] == '1':
        flags.append('MIN')
    if binArray[10][1] == '1':
        flags.append('REL DELTA')
    if binArray[10][2] == '1':
        flags.append('HFE')
    if binArray[10][3] == '1':
        flags.append('Percent')
    if binArray[11][0] == '1':
        flags.append('SECONDS')
    if binArray[11][1] == '1':
        flags.append('dBm')
    if binArray[11][2] == '1':
        flags.append('n (1e-9)')
    if binArray[11][3] == '1':
        flags.append('u (1e-6)')
    if binArray[12][0] == '1':
        flags.append('m (1e-3)')
    if binArray[12][1] == '1':
        flags.append('VOLTS')
    if binArray[12][2] == '1':
        flags.append('AMPS')
    if binArray[12][3] == '1':
        flags.append('FARADS')
    if binArray[13][0] == '1':
        flags.append('M (1e6)')
    if binArray[13][1] == '1':
        flags.append('K (1e3)')
    if binArray[13][2] == '1':
        flags.append('OHMS')
    if binArray[13][3] == '1':
        flags.append('Hz')
    return flags

def strToDigits(strOfBytes): #converts a string of space separated hexadecimal bytes into numbers following the protocol in readme.md
    binArray = getArrFromStr(strOfBytes) #Create an array of the binary values from those hexadecimal bytes
    digits = ""
    for number in reversed(range(1,5)): #reversed rabge so that we iterate through values 4,3,2,1 in that order due to how serial protocol works (see readme.md)
        out = processDigit(number,binArray)
        if out[1] == -1:
            print("Protocol Error: Please start an issue here: https://github.com/ddworken/2200087-Serial-Protocol/issues and include the following data: '" + strOfBytes + "'")
            exit(1)
        if out[0] == True: #append the decimal point if the decimalPointBool in the tuple is true
            digits += "."
        digits += str(out[1])
    minusBool = bool(int(binArray[0][::-1][3])) #following the serial protocol, calculate whether or not a negative sign is needed
    if minusBool:
        digits = '-' + digits
    return digits

def mainLoop(args):
    if len(args.port) == 1:
    	ser = serial.Serial(port=args.port[0], baudrate=2400, bytesize=8, parity='N', stopbits=1, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False)
    	global grapher 
	grapher = grapher([0])
	if args.csv:
	    print args.port[0] + ','
	if not args.csv:
	    print "| " + args.port[0] + " |"
    	while(True):
            chunk = getSerialChunk(ser)
            if args.graph:
	    	try:
	            floatVal = float(strToDigits(chunk))
                    grapher.appendWithLabel(floatVal, ' '.join(strToFlags(chunk)))
                    graph = grapher.getGraph()
                    for line in graph:
                        print line
                except:
		    print strToDigits(chunk)[-1]
		    try:
		    	if strToDigits(chunk)[-1] == 'C' or strToDigits(chunk)[-1] == 'F':
			    floatVal = float(strToDigits(chunk)[0:-1])
                	    grapher.appendWithLabel(floatVal, ' '.join(strToFlags(chunk)))
                	    graph = grapher.getGraph()
                	    for line in graph:
                	    	print line
		    except:
		        pass
	    else:
		if args.csv:
		    if not args.quiet:
                    	print strToDigits(chunk) + ' ' + ' '.join(strToFlags(chunk)) + ","
		    if args.quiet:
		    	print strToDigits(chunk) + ","
		if not args.csv:
		    if not args.quiet:
                        print "| " + strToDigits(chunk) + ' ' + ' '.join(strToFlags(chunk)) + " |"
                    if args.quiet:
                        print "| " + strToDigits(chunk) + " |"
    if len(args.port) > 1:
	if args.graph:
	    print "This program does not support graphing two multimeters at the same time. "
	else:
	    serialPorts = []
	    for portNum in range(len(args.port)):
		serialPorts.append(serial.Serial(port=args.port[portNum], baudrate=2400, bytesize=8, parity='N', stopbits=1, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False))
	    if not args.csv:
		sys.stdout.write("| ")
	    for index,port in enumerate(args.port):
		sys.stdout.write(port),		#We have to use sys.stdout.write() so that it doesn't print a new line after each time we write data
		if args.csv:
		    if index != len(args.port)-1: 	#So that it doesn't print a , after the last element
		    	sys.stdout.write(","),
	    	if not args.csv:
		    sys.stdout.write(" | ")
	    sys.stdout.write("\n")		#So of course that means we have to print a new line so it still is a csv
	    while True:
		data = []
		for ser in serialPorts:
		    chunk = getSerialChunk(ser)
		    if not args.quiet:
			data.append(strToDigits(chunk) + ' ' + ' '.join(strToFlags(chunk)))
		    if args.quiet:
			data.append(strToDigits(chunk))
		if not args.csv:
		    sys.stdout.write("| ")
		for index,datum in enumerate(data):
		    sys.stdout.write(datum)
		    if args.csv:
		    	if index != len(data)-1: 	#So that it doesn't print a , after the last element
		    	    sys.stdout.write(",")
		    if not args.csv:
			sys.stdout.write(" | ")
		sys.stdout.write("\n")

def getSerialChunk(ser):
    while True:
        chunk = []
        for i in range(14):
            chunk.append(ser.read(1).encode('hex'))
        if chunk[0][0] != '1':
            startChunk = []
            endChunk = []
            for index,byte in enumerate(chunk):
                if byte[0] == '1':
                    startChunk = chunk[index:]
                    endChunk = chunk[:index]
                    chunk =  startChunk + endChunk
        return " ".join(chunk)

if __name__ == '__main__': #Allows for usage of above methods in a library
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", help="Use this argument if you want to display a graph. ", action="store_true")
    parser.add_argument("-p", "--port", nargs='*', help="The serial port to use", default="/dev/ttyUSB0")
    parser.add_argument("-q", "--quiet", help="Use this argument if you only want the numbers, not the description. ", action="store_true")
    parser.add_argument("-c", "--csv", help="Use this argument to enable csv output", action="store_true")
    args = parser.parse_args()
    mainLoop(args) #Call the mainLoop method with a list containing serial data

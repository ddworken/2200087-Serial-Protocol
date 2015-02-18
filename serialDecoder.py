#/bin/python

from bitstring import BitArray

def getArrFromStr(serialData):
    output = []
    inputList = serialData.split(" ")
    for index,value in enumerate(inputList):
        inputList[index] = '0x' + value
    for value in inputList:
        output.append(BitArray(hex=value).bin)
    return output

def processDigit(digitNumber, binArray):
    decimalPointBool = False
    digitValue = -1
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
    digitDict['A'] = int(bin[0][0])
    digitDict['F'] = int(bin[0][1])
    digitDict['E'] = int(bin[0][2])
    digitDict['B'] = int(bin[1][0])
    digitDict['G'] = int(bin[1][1])
    digitDict['C'] = int(bin[1][2])
    digitDict['D'] = int(bin[1][3])
    digitValue = getIntFromDigitDict(digitDict)
    decimalPointBool = bool(int(bin[0][3]))
    if digitNumber == 4:
        decimalPointBool = False
    return (decimalPointBool, digitValue)

def getIntFromDigitDict(digitDict):
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

def strToDigits(strOfBytes):
    binArr = getArrFromStr(strOfBytes)
    digits = ""
    for number in reversed(range(1,5)):
        out = processDigit(number,binArr)
        if out[0] == True:
            digits += "."
        digits += str(out[1])
    return digits
def mainLoop(inputs):
    for item in inputs:
        print strToDigits(item)

if __name__ == '__main__':
    inputs = ["12 20 37 4D 5A 67 77 8F 93 AE B0 C0 D2 E0","12 20 37 4D 55 6B 73 8E 97 A8 B0 C0 D0 E0"]
    mainLoop(inputs)

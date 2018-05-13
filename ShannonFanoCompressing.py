import numpy
from bitarray import bitarray
from bitstream import BitStream
import pickle
import struct
import bitstring
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def bubbleSort(array1,array2): #Sorting Algorithm to Descending Order
    size = len(array1)
    
    for i in range(0,size-1):
        swap = True
        for j in range(0,size-1-i):
            if array1[j] > array1[j+1]:
                
                temp1 = array1[j]
                array1[j] = array1[j+1]
                array1[j+1] = temp1
                
                temp2 = array2[j]
                array2[j] = array2[j+1]
                array2[j+1] = temp2
                
                swap = False

        if swap:    break
    
    array1 = array1[::-1]
    array2 = array2[::-1]

    return array1,array2

def readFile(filename):
    file = open(filename, 'r')
    
    c = []
    p = []

    while True:
        char = file.read(1)
        if not char: break
        
        if char not in c:
            c.append(char)
            p.append(int(1))
        else:   
            p[c.index(char)] += 1

    file.close()

    p,c = bubbleSort(p,c)

    r = [''] * len(p)

    r = shannanFano(p,c,r)

    return p,c,r

def shannanFano(p,c,r):
    size = len(p)
    print(size)
    if size == 1:
        return r[0]
    else:
        mid = numpy.sum(p) / 2
        div = 1
        
        for i in range(2,size):
            if(numpy.sum(p[0:i]) < abs(mid - numpy.sum(p[0:div]))):
                div = i
            else:
                break
   
        for k in range(0,div):
            if r[k] != '':
                r[k] = r[k] + '0' 
            else:
                r[k] = '0b0'
        
        for j in range(div,size):
            if r[j] != '':
                r[j] = r[j] + '1'
            else:
                r[j] = '0b1'

        return numpy.append(shannanFano(p[0:div],c[0:div],r[0:div]),shannanFano(p[div:size],c[div:size],r[div:size]))

def toCode(r):
    stream = bitarray()
    for i in range(0,len(r)):
        tempStream = BitStream()
        
        if ',' in r[i]:
            temp = r[i].split(',')
        else:
            temp = r[i]
        
        if temp == 'True':
            tempStream.write(True,bool)
        elif temp == 'False':
            tempStream.write(False,bool)
        else:
            for j in range(0,len(temp)):
                tempStream.write(str2bool(temp[j]),bool)
        
        stream = numpy.append(stream,tempStream)

    return stream

def compressFile(filename,c,r):
    file = open(filename, 'r')
    stream = bitstring.BitString()
    
    while True:
        char = file.read(1)
        if not char: break   
        #stream = numpy.append(stream,s[c.index(char)])
        stream.insert(r[c.index(char)])
    
    
    path = filename.split('.')[0]+'.bnr'
    outputFile = open(path,"wb")
    stream.tofile(outputFile)

    outputFile.close()
    file.close()

    return stream

''' not used

def byteWriter(bitStr, outputFile):
    bitStream = BitStream()
    bitStream = bitStr
    print(type(bitStream))
    while len(bitStream) > 8: # write byte(s) if there are more then 8 bits
        byteStr = bitStream[:8]
        bitStream = bitStream[8:]
        outputFile.write(chr(int(byteStr, 2)))
    else:
        outputFile.write(str(int(bitStream,2)))
    outputFile.close()

'''

if len(sys.argv) != 2:
    sys.stderr.write("Please enter the filename to compress!")
    sys.exit(1)

filename = sys.argv[-1]
p,c,r = readFile(fileName)
stream = compressFile(fileName,c,r)
print(stream)

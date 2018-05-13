import numpy
from bitarray import bitarray
from bitstream import BitStream
import pickle
import struct
import bitstring
import sys

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

    return p,c

def haufmannCompressing(filename):
    freq_list, char_list = readFile(filename)
    char_list_artif = char_list
    code_list = [''] * len(freq_list)
    
    char_list_artif, code_list = haufmannCoding(freq_list, char_list, code_list, char_list_artif)
    ''' to Control : PASSED '''
    for i in range(len(char_list_artif)):
        print(char_list_artif[i] + " : " + code_list[i])

    compressFile(filename, char_list_artif, code_list)

    

def haufmannCoding(freq_list, char_list, code_list, char_list_artif): 
    freq_list, char_list = bubbleSort(freq_list, char_list)
    last_elem = len(freq_list) - 1
    
    if last_elem == 0:
        return char_list_artif, code_list
    
    for char in char_list[last_elem]:
        code_list[char_list_artif.index(char)] = '1' + code_list[char_list_artif.index(char)]
    
    for char in char_list[last_elem -1]:
        code_list[char_list_artif.index(char)] = '0' + code_list[char_list_artif.index(char)] 
    
    ''' add last two char and freq '''
    freq_list[last_elem -1], char_list[last_elem -1] = freq_list[last_elem] + freq_list[last_elem -1], char_list[last_elem] + char_list[last_elem -1] 
    
    ''' won't use last elements anymore '''
    freq_list, char_list = freq_list[0:last_elem], char_list[0:last_elem]
    
    return haufmannCoding(freq_list, char_list, code_list, char_list_artif)

def compressFile(filename, char_list, code_list):
    for i in range(len(code_list)):
        code_list[i] = '0b' + code_list[i]
        
    file = open(filename, 'r')
    stream = bitstring.BitString()
    
    while True:
        char = file.read(1)
        if not char: break   
        stream.insert(code_list[char_list.index(char)])
    
    
    path = filename.split('.')[0]+'.bnr'
    outputFile = open(path,"wb")
    stream.tofile(outputFile)

    outputFile.close()
    file.close()

    return stream

if len(sys.argv) != 2:
    sys.stderr.write("Please enter the filename to compress!")
    sys.exit(1)
    
filename = sys.argv[-1]
print(filename)
haufmannCompressing(filename)





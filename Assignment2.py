# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:19:25 2021

@author: franc
"""
from nltk.stem.porter import *
stemmer = PorterStemmer()
import sys
import time

#read term-docID pair as a list
def readTerm(file):
    with open(file, encoding='UTF-8') as f:
        read_data=[i.split(',') for i in f.readlines()] 
    for term in read_data:                             
        term[1]=int(term[1].replace('\n',''))
    result=[tuple(i) for i in read_data]
    return result

#turn term-docID list into a dictionary
def buildInvert(file):
    termList=readTerm(file)
    invIn={}
    for term in termList:
        if term[0] not in invIn:
            invIn[term[0]]=[term[1]]
        else:
            invIn[term[0]].append(term[1])
    return invIn

#write to file
def writeInd(inv, file):
    with open(file, 'a+', encoding='UTF-8') as f:
        for key in inv:
            f.write(key + ':' + ','.join(map(str, inv[key]))+'\n')
    return
#read from file
def readInd(file):
    with open(file, encoding='UTF-8') as f:
        read_data=[i.split(':') for i in f.readlines()]
    readDict={}
    for item in read_data:
        readDict[item[0]]=item[1]
    return readDict
    
#Split the query into list of terms
def parseQ(query):
    return query.split()

#Stem the query terms and find the intersection
def andSearch(query, inv):
    parsed=parseQ(query)
    stemmed=[]
    for item in parsed:
        stemmed.append(stemmer.stem(item))
    result = inv.get(stemmed[0],[])
    for key in stemmed:
        if result == []:
            return result
        result = sorted(list(set(result) & set(inv[key])))
    return result

def orSearch(query, inv):
    parsed=parseQ(query)
    stemmed=[]
    for item in parsed:
        stemmed.append(stemmer.stem(item))
    result = set()
    for key in stemmed:
        result = result | set(inv[key])
    return sorted(list(result))

def notSearch(query, inv):
    parsed=parseQ(query)
    stemmed=[]
    for item in parsed:
        stemmed.append(stemmer.stem(item))
    fileSet = set()
    for key in inv:
        fileSet.add(set(inv[key]))
    for key in stemmed:
        fileSet.remove(set(inv[key]))
    return sorted(list(fileSet))

def compress(data):
    dictString=''
    newInd=[]
    for key,value in data.items():
        newInd.append(tuple([len(dictString), value]))
        dictString+=key
    return dictString, newInd

def decompress(dictString, newInd):
    invIn={}
    for i in range(len(newInd)):
        if not i == len(newInd)-1:
            invIn[dictString[newInd[i][0]:newInd[i+1][0]]]=newInd[i][1]
        else:
            invIn[dictString[newInd[i][0]:-1]]=newInd[i][1]
    return invIn

file='E:\\Courses\\CI Info Retrival\\finalTerms.txt'
outfile='E:\\Courses\\CI Info Retrival\\Inverted.txt'
compressed='E:\\Courses\\CI Info Retrival\\Compressed.txt'
termList=readTerm(file)
start = time.process_time()
invIn=buildInvert(file)
invDone = time.process_time()
#writeInd(invIn, outfile)
#readInd(outfile)
query='clinton obama'
result=orSearch(query,invIn)
searchDone = time.process_time()

a,b=compress(invIn)
compressDone = time.process_time()
restore=decompress(a,b)
decomDone = time.process_time()
with open(compressed, 'a+', encoding='UTF-8') as f:
    f.write(a)
    f.write(str(b))
    
print(str(sys.getsizeof(a)) + '  dict string')
print(str(sys.getsizeof(b)) + '  compressed list')
print(str(sys.getsizeof(invIn)) + '  inverted index')

print(str(invDone-start) + 'time to build')
print(str(searchDone-invDone) + 'time to search')
print(str(compressDone-searchDone) + 'time to compress')
print(str(decomDone-compressDone) + 'time to decompress')

import re, math, collections, itertools, os
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk import precision
from nltk import recall
from mongodb.mongodao import Mongodao
from nltk.corpus import stopwords


Y_FILE = os.path.join('polarityData', 'y.txt')
R_FILE = os.path.join('polarityData', 'r.txt')
D_FILE = os.path.join('polarityData', 'd.txt')
K_FILE = os.path.join('polarityData', 'k.txt')
ALL_FILE = [Y_FILE, R_FILE, D_FILE, K_FILE]

def writeToFile(list):
    
    pos = 0
    index = 0 
    fh = open(ALL_FILE[pos], 'w')      
    for b in list:
        if index !=0 and index % 3000 == 0:
            pos += 1
            if pos >= 4:
                break
            else:
                fh = open(ALL_FILE[pos], 'w')  
        fh.write('%s' % b.encode('utf-8'))
        fh.write('\n')
        index += 1

def splitPosNeg(filename):
    with open(filename, 'r') as fh:
        for line in fh:

if __name__ == "__main__":
    '''
    mongodao = Mongodao()
    list = mongodao.get_all_tweets()
    writeToFile(list)
    '''
    
    
       

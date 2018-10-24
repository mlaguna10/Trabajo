#-*- coding: utf-8 -*-

#https://pmoracho.github.io/blog/2017/01/04/NLTK-mi-tutorial/
#http://liceu.uab.cat/~joaquim/language_technology/NLP/PLN_analisis.html

import nltk
from nltk.corpus import treebank
#from nltk.book import *
from urllib2 import Request
from nltk import word_tokenize
import datetime
from nltk import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from pattern.es import suggest
from chardet import detect
import glob
import os
import re

well_spell_words = []
words = []

#mira si hay dos palabras juntas
def split_words(text):
    c = False
    a = []
    b = []
    for i in range(len(text)):
        if(text[i].isupper() or c):
            b.append(text[i])
            c = True
        else:
            a.append(text[i])
    return u''.join(a),u''.join(b)

def fix_words(words):
    for i in range(len(words)):
        word, val = suggest(words[i])[0]
        #if(val>=0.8 and word!=''):
        well_spell_words.append(word)
        #else:
        #    well_spell_words.append(0)

filepath = str(glob.glob('*.txt')).split("]")[0]
filepath = filepath.split("[")[1]
filepath = filepath.split("'")[1]
with open(filepath, 'r') as myfile:
    sentence=myfile.read().replace('\n', '')

#os.system("rm " + filepath)

tokens = nltk.word_tokenize(sentence)
text = nltk.Text(tokens)

for i in range(len(tokens)):
    #tratamiento de las palabras
    words = split_words(tokens[i].decode('utf-8'))
    fix_words(words)

#deja únicamente las diferentes a 0.
#falta mejorar el filtro
print filter(lambda a: a!=0, well_spell_words)

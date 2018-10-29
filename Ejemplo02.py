# -*- coding: utf-8 -*-
# coding: utf-8

#https://pmoracho.github.io/blog/2017/01/04/NLTK-mi-tutorial/
#http://liceu.uab.cat/~joaquim/language_technology/NLP/PLN_analisis.html

import sys
import nltk
from nltk.corpus import treebank
from nltk.metrics import edit_distance
from urllib2 import Request
from nltk import word_tokenize
import datetime
import unicodecsv as csv
from nltk import FreqDist
import codecs
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from pattern.es import suggest
from chardet import detect
import glob
from difflib import SequenceMatcher
import os
import re

well_spell_words = []
words = []
sentence=[]
text = []
confidence = []
height = []
width = []
texto = []

def getindices(s):
    z = []
    for i in range(len(s)):
        z.append([i for i, c in enumerate(s[i]) if c.isupper()])
    return z

def split_words(text):
    words = []
    for i in range(len(text)):
        indices = getindices(text)
        for j in range(len(indices)):
            s = indices[j]
            if(len(s)==1 and indices[0]!=0):
                a, b = text[i].split(text[i][s[0]])
                b = list(b)
                b.insert(0, str(text[i][s[0]]))
                words.append(a)
                words.append(''.join(b))
            else:
                words.append(text[i])
    return words

def fix_words(words, conf):
    s=0
    sentence = []
    #print words, conf
    for i in range(len(words)):
        if(conf[i]==1):
            word, val = suggest(words[i].lower())[0]
            if(val>=0.6):
                if(words[i].isupper()):
                    word=word.upper()
                elif(words[i][0].isupper()):
                    word=word[0].upper() + word[1:]
                sentence.append(word.encode('utf8'))
            else:
                sentence.append(words[i])
        else:
            sentence.append(words[i])
    return sentence

def good_words_filter(words):
    s=0
    conf = []
    for i in range(len(words)):
        if(words[i] in dictionary):
            if(dictionary.get(words[i])>=80):
                conf.append(0)
            else:
                conf.append(1)
        else:
            conf.append(1)

    return words, conf

if len(sys.argv) < 2:
    print('Usage: python Ejemplo02.py archivo_a_corregir.txt archivo_datos.csv')
    sys.exit(1)

#el primer argumento es el archivo a corregir
filepath = sys.argv[1]
with codecs.open(filepath, 'r', encoding='utf8') as myfile:
    sentence.append(myfile.readlines())#.replace('\n',"")
myfile.close()

#el segundo argumento el csv
filepath = sys.argv[2]
with codecs.open(filepath) as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        confidence.append(line[-2][:].replace(" ",""))
        height.append(line[-3][:].replace(" ",""))
        width.append(line[-4][:].replace(" ",""))
        text.append(line[-1][:].replace(" ",""))
    confidence.pop(0)
    height.pop(0)
    width.pop(0)
    text.pop(0)
    confidence = list(map(int, confidence))
    height = list(map(int, height))
    width = list(map(int, width))
    text = list(map(unicode,text))
    dictionary = dict(zip(text,confidence))
tsvfile.close()

#os.system("rm " + filepath)

for i in range(len(sentence[0])):
    if(sentence[0][i] == "\n"):
        texto.append(u"\n")
    else:
        words = nltk.word_tokenize(sentence[0][i])
        words, conf = good_words_filter(words)
        words = fix_words(words, conf)
        if(sentence[0][i-1]!="\n"):
            texto.append(u"\n")
            texto.append(words)
        else:
            texto.append(words)

for i in range(len(texto)):
    if(i==0):
        file = codecs.open("texto_corregido.txt", "w", encoding='utf-8')
        if(texto[i]=="\n"):
            file.write(u"\n")
        else:
            nombre = u' '.join(texto[i])
            file.write(nombre)
    else:
        file = codecs.open("texto_corregido.txt", "a", encoding='utf-8')
        if(texto[i]=="\n"):
            file.write(u"\n")
        else:
            z=texto[i]
            for i in range(len(z)):
                z[i] = z[i].decode('utf8')
            nombre = u' '.join(z)
            file.write(nombre)
file.close()

filepath = 'texto_corregido.txt'
with codecs.open(filepath, 'r', encoding='utf8') as myfile:
    well_spell_words.append(myfile.readlines())
myfile.close()

palabra = raw_input("Inserte la palabra que desea buscar en la imagen:")
for i in range(len(well_spell_words[0])):
    words = nltk.word_tokenize(well_spell_words[0][i])
    for j in range(len(words)):
        if(palabra == words[j]):
            print "si"

# -*- coding: utf-8 -*-
# coding: utf-8

#https://pmoracho.github.io/blog/2017/01/04/NLTK-mi-tutorial/
#http://liceu.uab.cat/~joaquim/language_technology/NLP/PLN_analisis.html

import sys
import nltk
import numpy as np
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
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

well_spell_words = []
words = []
sentence=[]
text = []
confidence = []
height = []
width = []
x = []
y = []
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

def unir(a,b,c,d):
    r = []
    for i in range(len(a)):
        r.append([a[i], b[i], c[i] + a[i], d[i] + b[i]])
    return r

def fix_words(words, conf):
    s=0
    c=False
    d=False
    sentence = []
    for i in range(len(words)):
        if(conf[i]==1):
            word, val = suggest(words[i].lower())[0]
            if(val>=0.6):
                if(words[i].isupper()):
                    word=word.upper()
                elif(words[i][0].isupper()):
                    word=word[0].upper() + word[1:]
                sentence.append(word.encode('utf8'))
            #corrección de dos palabras
            # elif(i+1!=len(words)):
            #     r = words[i] + words[i+1]
            #     word, val = suggest(r.lower())[0]
            #     if(val>=0.6):
            #         if(words[i].isupper()):
            #             word=word.upper()
            #         elif(words[i][0].isupper()):
            #             word=word[0].upper() + word[1:]
            #         sentence.append(word.encode('utf8'))
            #         c=True
            #     else:
            #         if(c):
            #             c=False
            #             sentence.append(words[i+1])
            #             d = True
            #         else:
            #             if(d):
            #                 d=False
            #             else:
            #                 sentence.append(words[i])
            else:
                sentence.append(words[i])
        else:
            sentence.append(words[i])
    return sentence

def buscar(words, word):
    for i in range(len(words)):
        a,b = words[i].split(" ")
        if(a==word):
            return b

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
        text.append(line[-1][:].replace(" ",""))
        confidence.append(line[-2][:].replace(" ",""))
        height.append(line[-3][:].replace(" ",""))
        width.append(line[-4][:].replace(" ",""))
        y.append(line[-5][:].replace(" ",""))
        x.append(line[-6][:].replace(" ",""))
    confidence.pop(0)
    height.pop(0)
    width.pop(0)
    text.pop(0)
    x.pop(0)
    y.pop(0)
    confidence = list(map(int, confidence))
    height = list(map(int, height))
    width = list(map(int, width))
    x = list(map(int, x))
    y = list(map(int, y))
    text = list(map(unicode,text))
    coord = unir(x,y,width,height)
    positions = dict(zip(text, coord))
    dictionary = dict(zip(text,confidence))
tsvfile.close()

#imagen a modificar
imagepath = sys.argv[3]

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
            nombre = u' '.join(z)
            file.write(nombre)
file.close()

filepath = 'texto_corregido.txt'
with codecs.open(filepath, 'r', encoding='utf8') as myfile:
    well_spell_words.append(myfile.readlines())
myfile.close()

with codecs.open(filepath, 'r', encoding='utf8') as myfile:
    data = myfile.read()
myfile.close()

#https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html qué es cada nomenclatura
text = word_tokenize(str(data))
s = nltk.pos_tag(text)
critical_words = []
for i in range(len(s)):
    a, b = s[i]
    if(b=='NNS' or b == 'NNP'):
        critical_words.append(a)

palabra = raw_input("Inserte la palabra que desea buscar en la imagen:")
for i in range(len(well_spell_words[0])):
    words = nltk.word_tokenize(well_spell_words[0][i])
    for j in range(len(words)):
        if(palabra.lower() == words[j].lower()):
            x1,y1,x2,y2 = positions[words[j]]
            source_img = Image.open(imagepath).convert("RGB")
            draw = ImageDraw.Draw(source_img)
            draw.line(((x1, y1), (x2, y1)), fill="red",width=2)
            draw.line(((x1, y2), (x2, y2)), fill="red",width=2)
            draw.line(((x1, y1), (x1, y2)), fill="red",width=2)
            draw.line(((x2, y1), (x2, y2)), fill="red",width=2)
            source_img.save("image_changed.jpg", "JPEG")

            file = codecs.open("coordinates.txt", "w", encoding='utf-8')
            file.write("Palabra buscada: " +str(palabra) + ". " + "x1: " + str(x1) + " " + "y1: " + str(x2) + " " + "x2: " + str(x2) + " " + "y2: " + str(y2) + " " + "\n")
            if(words[j] in critical_words):
                with codecs.open("nltk_dict.txt", 'r', encoding='utf8') as myfile2:
                    tipo = buscar(myfile2.readlines(),words[j].lower())
                myfile2.close()
                file.write(u"La palabra buscada está asociada a la clase: " + str(tipo) + "\n")
            file.write("Nombre de la imagen modificada: " + imagepath)
            file.close()

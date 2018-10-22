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
import glob
import os

#url = "http://www.gutenberg.org/cache/epub/41575/pg41575.txt"
#response = request.urlopen(url)
#raw = response.read().decode('utf8')

##print(datetime.datetime.now(),"Tipo:");
##print(datetime.datetime.now(),type(raw))

##print(datetime.datetime.now(),"Len:");
##print(datetime.datetime.now(),len(raw))

##print(datetime.datetime.now(),"Raw:");
##print(datetime.datetime.now(),raw[:75])

#tokens = word_tokenize(raw)

filepath = str(glob.glob('*.txt')).split("]")[0]
filepath = filepath.split("[")[1]
filepath = filepath.split("'")[1]
with open(filepath, 'r') as myfile:
    sentence=myfile.read().replace('\n', '')

#os.system("rm " + filepath)

# extract productions from three trees and induce the PCFG
#print("Induce PCFG grammar from treebank data:")

productions = []
#etiquetas de los diferentes corpus predeterminados
#item = treebank._fileids[0]
#la 0 tiene las palabras: Pierre Vinken 61 years old will join the board as a nonexecutive director Nov. 29

#for tree in treebank.parsed_sents(item)[:3]:
	#tree.draw()
	#transformacion sobre el árbol Chomsky, Markovian, etc...
	#tree.collapse_unary(collapsePOS = False)
	#tree.chomsky_normal_form(horzMarkov = 2)

	#productions += tree.productions()

#estos token ya son del texto, no del predeterminado. Es dividir el texto por palabras.
tokens = nltk.word_tokenize(sentence)#unicode(sentence, "utf-8")

#literalmente el texto.
text = nltk.Text(tokens)

#se encarga de dar el diccionario del texto.
#print(datetime.datetime.now(),"Diccionario:");
#se encarga de quitar los sufijos de las palabras
#spanish_stemmer = SnowballStemmer('spanish')
#print(datetime.datetime.now(),spanish_stemmer.stem("Hola como estas"))

#busca el set de sinónimos de la palabra y permite empezar a acceder a todas sus caracteristicas-
# syn = wordnet.synsets(tokens[2])
# print syn
#print(datetime.datetime.now(),syn[0].definition())
#syn[0].definition()

#Infinitivo del verbo (working)
#stemmer = PorterStemmer()
#print(datetime.datetime.now(),stemmer.stem('working'))

#el #Tipo de tokens
#print(datetime.datetime.now(),type(tokens))

#Longitud de los tokens
#print(datetime.datetime.now(),len(tokens))

#Primeros 10 tokens.
#print(datetime.datetime.now(),tokens[:10])

#"Separacion por Parrafos:");
#print(sent_tokenize(sentence))#unicode(sentence, "utf-8")

#"Separacion por palabras:");
#print(word_tokenize(sentence))#(unicode(sentence, "utf-8")

#"Sintaxis:");
#tagged = nltk.pos_tag(tokens)

#"Entities:");
#entities = nltk.chunk.ne_chunk(tagged)
#print(datetime.datetime.now(),entities[50])

#dibujar árbol
# a=list[entities]
# t = treebank.parsed_sents('wsj_0001.mrg')[0]
# t.draw()
#Ordenar alfabéticamente.
#print(datetime.datetime.now(),sorted(set(text)))

#Búsqueda de patrones
#print(datetime.datetime.now(),text.findall("<un>(<.*>)<especial>"))

#Concordancia de la palabra "red"
#print tokens[1]
#print(text.concordance(tokens[1], lines=5))
print suggest(tokens[1])

#Concordancia de la palabra (red) (primeras 5)
#print(datetime.datetime.now(),text.concordance("red", width=30, lines=5))

#Unidades fraseológicas de dos o más palabras que se usan muy habitualmente combinadas
#print(datetime.datetime.now(),text.collocations(10))

#Palabras que aparecen en los mismos contexto de una palabra específica (learning)
#print(datetime.datetime.now(),text.similar("red"))

#Palabra que sólo aparece una vez dentro de un contexto (primeras 20)
#frecuencia de una palabra en especifico
#fdist1 = FreqDist(text)
#print(datetime.datetime.now(),fdist1.hapaxes()[:20])

#Palabras más comunes (red, neurona)
# print(datetime.datetime.now(),text.common_contexts(["red"]))

#Palabras más comunes
# fdist1a = FreqDist(text)
# print([i for i in fdist1a.most_common(1000) if len(i[0]) > 5])

#text.dispersion_plot(["Learning", "datos", "aprendizaje", "ejemplo", "neurona", "red"])

#Este es un dato muy lindo que podemos calcular muy fácilmente sobre cualquier texto.
#La riqueza léxica representa la variedad de términos usados en un texto con relación a la cantidad total, la fórmula

# def riqueza_lexica(text):
#     return len(set(text)) / len(text)
#
# print riqueza_lexica(sentence)

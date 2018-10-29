import numpy as np
import unicodecsv as csv
import codecs

words = []
filepath = 'dict.txt'
with codecs.open(filepath, 'r', encoding='utf8') as myfile:
    words.append(myfile.readlines())
myfile.close()

file = codecs.open("dict2.txt", "w", encoding='utf-8')
for i in range(len(words[0])):
    print words[0][i].replace(" ","")
    file.write(words[0][i].replace(" ",""))
file.close()

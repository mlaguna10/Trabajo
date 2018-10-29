#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import sys
import unicodecsv as csv
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdf2image
from PIL import Image
import cv2
import time
import pytesseract
import matplotlib.pyplot as plt

def rutas(files):
    for i in range(len(files)):
        pdf_name = files[i].split("]")[0]
        files[i] = pdf_name
    return files

def conversion(pdf_name, quality, dir):
    pdf_name = os.getcwd() + "/" + dir + "/" + pdf_name
    start = time.time()
    image = pdf2image.convert_from_path(pdf_name, dpi=quality)
    a = 0
    for x in image:
        z1 = str(a) + ".jpg"
        x.save(z1, 'JPEG')
        a+=1

    end = time.time()
    return end-start, a

def tesseract(a):
    temp = np.arange(a)
    data = []
    start = time.time()
    for i in temp:
        z1 = str(i) + ".jpg"
        data.append(pytesseract.image_to_data(Image.open(z1)).split("\n"))
        os.system("rm " + z1)
    end = time.time()
    return (end-start)/len(data), data

def analisis(path, data):
    confidence = []
    height = []
    width = []
    text = []
    start = time.time()
    index = 0
    for i in data:
        with open("outputbase"+ str(index) + ".tsv", 'w') as tsvfile:
            tsvoutput = csv.writer(tsvfile, delimiter=" ")
            for val in i:
                tsvoutput.writerow(val)

        with open("outputbase"+ str(index) + ".tsv") as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for line in tsvreader:
                confidence.append(line[-2][:].replace(" ",""))
                height.append(line[-3][:].replace(" ",""))
                width.append(line[-4][:].replace(" ",""))
                text.append(line[-1][:].replace(" ",""))

            #quita los titulos de las listas
            confidence.pop(0)
            height.pop(0)
            width.pop(0)
            text.pop(0)
            confidence = list(map(int, confidence))
            height = list(map(int, height))
            width = list(map(int, width))
            text = list(map(unicode,text))
            weight = [a*b for a,b in zip(height,width)]
            values = [a*b for a,b in zip(weight,confidence)]

            #este paso de aquí es importante porque por algún motivo el último dato de la columna confidence
            #se trunca con el último dato de la columna text, entonces toca devolverlo a su sitio.
            if index==len(data)-1:
                temp = text[-1]
                text[-1] = u''
                confidence[-1] = temp

            #aquí se obtiene el valor de la legibilidad del documento, se hace con el módelo
            #propuesto  donde cada blob aporta de acuerdo a su peso de confidence.
            long=0
            sum=0
            for i in range(len(confidence)):
                if(confidence[i]!=-1 and text[i]!=''):
                    long+=1.0
                    sum+=confidence[i]
            if(long==0):
                t=0.0
            else:
                t=sum/long
            #os.system("rm outputbase"+str(index)+".tsv")
            confidence = []
            height = []
            width = []
            text=[]

            escritura(path, index, t)
            index+=1
    end = time.time()
    return end-start

def escritura(path, index, t):
    file = open("porcentajes_legibilidad"+path+".txt", "a")
    file.write('La legibilidad de la imagen' + " " +  str(index+1) + " " + 'es: ' + str('%.2f' % t) + "%" + "\n")
    file.close()

t_conversion,t_tesseract,t_analisis = 0,0,0
fn = sys.argv[1]
if os.path.exists(fn):
    dir = os.path.basename(fn)
    calidad_dpi=200

    for folder, sub_folders, files in os.walk(dir):
        archivos = rutas(files)

    for i in range(len(files)):
        #el valor de 200 es el valor del dpi (calidad de la imagen) que se le pasa al convertidor de pdf a jpg.
        #con dpi de 100 se obtienen resultados más rápidos, pero con porcentajes notablemente más bajos.
        t_conversion, a = conversion(files[i],calidad_dpi, dir)
        t_tesseract, data = tesseract(a)
        file = open("porcentajes_legibilidad" + files[i] + ".txt", "w")
        file.write("El documento analizado fue: " + files[i] + "\n")
        file.close()
        t_analisis = analisis(files[i],data)
        file = open("porcentajes_legibilidad" + files[i] + ".txt", "a")
        file.write("El tiempo de conversión del pdf a jpg es de: " + str(t_conversion) + " s."+ "\n")
        file.write("El tiempo de procesamiento de tesseract por cada imagen es de: " + str(t_tesseract) + " s."+ "\n")
        file.write("El tiempo de analisis total es de: " + str(t_analisis) + " s."+ "\n")
        file.write("El valor de calidad dpi utilizado fue de: " + str(calidad_dpi) + ".")
        file.close()

else:
    print "La carpeta: " + fn + " especificada no existe."

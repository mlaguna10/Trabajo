import cv2
import sys
import pytesseract
import datetime
import os
import numpy as np

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print('Usage: python Ejemplo01.py image.jpg C:\TEMP')
    sys.exit(1)

  imPath = sys.argv[1]
  output_dir = sys.argv[2]

  config = ('-l eng --oem 1 --psm 3')
  img = cv2.imread(imPath, cv2.IMREAD_COLOR)

  file_name = os.path.basename(imPath).split('.')[0]
  file_name = file_name.split()[0]

  output_path = os.path.join(output_dir, file_name)
  if not os.path.exists(output_path):
        os.makedirs(output_path)
  save_path = os.path.join(output_path, file_name + "_filter_1.jpg")
  cv2.imwrite(save_path, img)

  text = pytesseract.image_to_string(img, config=config)
  print words = pytesseract.image_to_data(img, config=config)
  file = open("texto_" + str(imPath) + ".txt", "w")
  file.write(u''.join(text).encode('utf-8'))
  file.close()

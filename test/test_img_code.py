#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-26 下午5:43
# @Description:

import pytesseract
from PIL import Image


# pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# text = pytesseract.image_to_string(Image.open('E://figures/other/poems.jpg'))
img = Image.open('/home/wytheli/Pictures/image2.png')
print(img)
text = pytesseract.image_to_string(img, lang='eng')
print(text)

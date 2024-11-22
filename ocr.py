import cv2
import numpy as np
import pytesseract
import json
import sys
import os
from ktpocr import KTPOCR
import json
import mysql.connector


def read_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)

    result = pytesseract.image_to_string(threshed, lang="eng")

    final = []

    for word in result.split("\n"):
        if "”—" in word:
            word = word.replace("”—", ":")

        if "NIK" in word:
            nik_char = word.split()
        if "?" in word:
            word = word.replace("?", "7")

        final.append(word)
    return final


def ocr_result():
    ktppath = "uploads\image.png"

    if os.path.exists(ktppath):
        img = cv2.imread(ktppath)
        ocr_data = read_image(img)
        with open("data.json", "w") as outfile:
            json.dump(ocr_data, outfile)
        print("Data extracted and saved in 'data.json'")
    else:
        print("Invalid path. Please provide a valid path to the image.")

    return ocr_data

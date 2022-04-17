import pytesseract as pt
from PIL import Image
import csv
import serial
import time
import cv2
import numpy as np
import pyrebase
import firebase
from textblob import TextBlob

config={
   // <Firebase credential data>
}

firebase=pyrebase.initialize_app(config)
storage=firebase.storage()

import time

vid=cv2.VideoCapture(1)

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
timesplit=current_time.split(':')
curhr=timesplit[0]
with open('timetable.csv', mode ='r')as file: 
      
  # reading the CSV file 
  csvFile = csv.reader(file) 
    
  # displaying the contents of the CSV file 
  for lines in csvFile:                   
      
        timest=lines[0]
        timehr=timest.split(':')
        if timehr[0]==curhr:
            print(lines[2])
            subject=lines[2]

arduino = serial.Serial(port='COM9', baudrate=9600, timeout=.1)
doc=subject+'.txt'
print(doc)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    data = arduino.readline()
    return data

while True:
    res=write_read('')
    if(res==b'on\r\n'):
        print("ON")
        while True:
            ret, frame = vid.read()
  
    # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite('feedfin.png',frame)
                break
        img = cv2.imread('feedfin.png')
        cv2.imshow("original",img)
        cropped=img[385:440,0:640]
        cv2.imshow("cropped",cropped)
        cv2.imwrite('cropped.png',cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img_object = Image.open('cropped.png')
img_text = pt.image_to_string(img_object)
print("working")
print(img_text)
with open(doc, "a") as file_object:    
    file_object.write("\n"+img_text)

storage.child(doc).put(doc)

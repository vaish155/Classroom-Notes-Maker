
"""
Requires:
- Python 3
- pip install opencv-python
- pip install pytesseract
- download Tesseract-OCR data
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import pytesseract as pt
# Path of working folder on Disk
src_path = "image/"

import docx
doc=docx.Document('me.docx')

# Tessdata path
#os.environ['TESSDATA_PREFIX'] = 'C:\Program Files\Tesseract-OCR\tessdata'
os.environ['TESSDATA_PREFIX'] =r'C:\Users\Lenovo\Desktop\python projects\handwritingdetectn\tessdata'

pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import pyrebase
import firebase

config={
    "apiKey": "AIzaSyAFcaRZCduSRhya710Dc_A7No8Me-EHsno",
    "authDomain": "arithmenia.firebaseapp.com",
    "projectId": "arithmenia",
    "storageBucket": "arithmenia.appspot.com",
    "messagingSenderId": "897754555141",
    "appId": "1:897754555141:web:b4c168262756d88f3f0d6c",
    "measurementId": "G-WDWMFGCX14",
    "databaseURL": "https://arithmenia-default-rtdb.firebaseio.com/"
}

firebase=pyrebase.initialize_app(config)
storage=firebase.storage()


def is_valid_expression(number1, number2, operator, result):
    number1 = int(number1)
    number2 = int(number2)
    result = int(result)
    if operator == '-':
        return number1 - number2 == result
    if operator == '+':
        return number1 + number2 == result
    if operator == 'x' or operator == '*':
        return number1 * number2 == result
    if operator == ":" or operator == "/":
        return number1 / number2 == result

def get_string(img_path, tub_kernel):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones(tub_kernel, np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel, iterations=2)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", gray)

    #  Apply threshold to get image with only black and white
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    _, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", gray)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

    return result

cp = cv2.VideoCapture(1)
while(True):
    #time.sleep(5)
    camera, frame = cp.read()
    
    if frame is not None:
        cv2.imshow("Frame", frame)
        
    q = cv2.waitKey(1)
    if q==ord("q"):
        cv2.imwrite('feedfin.png',frame)
        

        break
img = cv2.imread('feedfin.png')
cv2.imshow("original",img)
cropped=img[375:475,0:640]
cv2.imshow("cropped",cropped)
cv2.imwrite('image/cropped.png',cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()


print('--- Start recognize match ---')
img_path = src_path + "form7.png"

# Extract text from image
result = get_string(img_path, (2, 3)).strip()

# Try one more
if not result or len(result.split(" ")) < 5:
    result = get_string(img_path, (1, 3))

# Try one more
if not result or len(result.split(" ")) < 5:
    result = get_string(img_path, (4, 3))

print("Text result:")
print(result)

print("----- extract expression -------")
# Split using space
data = result.strip().split(" ")
"""print(data)

print(data[0])"""
"""if(data.count('=')<1):
    print("Word")
    img_object = Image.open(img_path)
    img_text = pt.image_to_string(img_object)
    print(img_text)
    with open("maths.txt", "a") as file_object:    
        file_object.write("\n"+img_text)
else:"""
image_1 = Image.open('image/thres.png')
im_1 = image_1.convert('RGB')
im_1.save('fin1.pdf')
storage.child('fin1.pdf').put('fin1.pdf')
    
"""print(data[1])
print(data[2])
print(data[3])
print(data[4])

if is_valid_expression(data[0], data[2], data[1], data[4]):
    print("Correct")
else:
    print("Incorrect")

print("------ Done -------")"""
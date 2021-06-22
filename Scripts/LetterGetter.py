# This file:
#  Screenshot the game board
#  Crop every letter tile into 7x8=56 individual letters
#  Return a graph that contains all of the letters connected to each other as necessary
#  Called by WordGen.py, which will take this graph and determine the best words to attempt
from os import name
import time
# import pyautogui
from PIL import Image
import os.path, sys
import csv
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from collections import namedtuple
from PIL import Image, ImageDraw

# Defs
Node = namedtuple('Node', 'nodeId value edges')
# reader = csv.reader(locationsFile, skipinitialspace=True)
# locations = [[float(row[0]), float(row[1]), float(row[2]), float(row[3])] for row in reader]
testArray = ['s','a','b','m','a','qu','t','o','qu','e','a','o','a','i','e','d','f','u','r','z','m','p','m','p','e','u','n','l','d','o','s','u','m','i','y','o','b','e','p','h','b','r','e','u','d','a','g','n','o','i','f','a']
graphMapping = {
    0:[1,7,8],
    1:[0,2,8,9],
    2:[1,3,9,10],
    3:[2,4,10,11],
    4:[3,5,11,12],
    5:[4,6,12,13],
    6:[5,13,14],
    7:[0,8,15],
    8:[0,1,9,16],
    9:[1,2,8,10,16,17],
    10:[2,3,9,11,17,18],
    11:[3,4,10,12,18,19],
    12:[4,5,11,13,19,20],
    13:[5,6,12,14,20,21],
    14:[6,13,21],
    15:[7,8,16,22,23],
    16:[8,9,15,17,23,24],
    17:[9,10,16,18,24,25],
    18:[10,11,17,19,25,26],
    19:[11,12,18,20,26,27],
    20:[12,13,19,21,27,28],
    21:[13,14,20,28,29],
    22:[15,23,30],
    23:[15,16,22,24,30,31],
    24:[16,17,23,25,31,32],
    25:[17,18,24,26,32,33],
    26:[18,19,25,27,33,34],
    27:[19,20,26,28,34,35],
    28:[20,21,27,29,35,36],
    29:[21,28,36],
    30:[22,23,31,37,38],
    31:[23,24,30,32,38,39],
    32:[24,25,31,33,39,40],
    33:[25,26,32,34,40,41],
    34:[26,27,33,35,41,42],
    35:[27,28,34,36,42,43],
    36:[28,29,35,43,44],
    37:[30,38,45],
    38:[30,31,37,39,43,46],
    39:[31,32,38,40,46,47],
    40:[32,33,39,41,47,48],
    41:[33,34,40,42,48,49],
    42:[34,35,41,43,49,50],
    43:[35,36,42,44,50,51],
    44:[36,43,51],
    45:[37,38,46],
    46:[38,39,45,47],
    47:[39,40,46,48],
    48:[40,41,47,49],
    49:[41,42,48,50],
    50:[42,43,49,51],
    51:[43,44,50]
}

locationsFile = '../BookwormLetterLocationsRELATIVE.csv'
outputDestination = '../Letters'
testFile = '../Images/TestBoard.png'
testLetterCrops = '../TestCroppedLetters'

# Screenshot board

def getGameBoard():
    # TODO
    return Image.open(testFile)

# Loop over letter zones to make 52 images for the graph
def genLetterCrops(im):
    for i, location in enumerate(locations[1:]):
        imCrop = im.crop(location[0], location[1], location[2], location[3])
        imCrop.save(outputDestination + str(i) + '_.png', quality=100)

#  Function is good
def processNormalTile(img_grey):
    # specify circle parameters: centre ij and radius
    (x,y) = img_grey.shape
    (ci,cj) = (int(x/2), int(y/2))
    cr=int(y*.5*.7)

    # Min the value outside the letter radius
    maxPix = img_grey.max()
    for i in range(x):
        for j in range(y):
            if np.sqrt((i-ci)**2+(j-cj)**2) > cr:
                img_grey[i][j] = maxPix
    
    # ret,thresh_binary_inv = cv2.threshold(z,127,255,cv2.THRESH_BINARY)
    image_from_array = Image.fromarray(img_grey)
    # cv2.imshow("normal", img_grey)
    # cv2.waitKey(0)
    #We can send the array directly to OCR, but I like to see the image.
    text = pytesseract.image_to_string(image_from_array, lang='eng', config='--psm 10')
    return text.upper()

# In Progress
def processFireTile(img_color, img_grey):
    # specify circle parameters: centre ij and radius
    (x,y) = img_grey.shape
    (ci,cj) = (int(x/2), int(y/2))
    cr=int(y*.5*.65)


    # img = cv2.medianBlur(img_grey,15)
     # define range of black color in HSV
    lower_val = np.array([0,0,0])
    upper_val = np.array([179,255,127])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(img_color, lower_val, upper_val)
    # invert mask to get black symbols on white background
    mask_inv = cv2.bitwise_not(mask)
    # Min the value outside the letter radius
    maxPix = mask_inv.max()
    for i in range(x):
        for j in range(y):
            if np.sqrt((i-ci)**2+(j-cj)**2) > cr:
                mask_inv[i][j] = maxPix
    text = pytesseract.image_to_string(mask_inv, lang='eng', config='--psm 10')
    cv2.imshow(text, mask_inv)
    cv2.waitKey(0)

    # img = cv2.boxFilter(img_color,-1, (15,15), normalize = True)


   
    
    # th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    # image_from_array = Image.fromarray(th3)
    # #We can send the array directly to OCR, but I like to see the image.
    # start_time = time.time()
    # text = pytesseract.image_to_string(img, lang='eng', config='--psm 10')
    # cur_time = time.time()
    # cv2.imshow(text, th3)
    # cv2.waitKey(0)
    # print("OCR took {} seconds.".format((cur_time-start_time)))
    return text.upper()

# In Progress
def processGreenTile(img, img_grey):
    # specify circle parameters: centre ij and radius
    (x,y) = img_grey.shape
    (ci,cj) = (int(x/2), int(y/2))
    cr=int(y*.5*.7)

    # Min the value outside the letter radius
    maxPix = img_grey.max()
    for i in range(x):
        for j in range(y):
            if np.sqrt((i-ci)**2+(j-cj)**2) > cr:
                img_grey[i][j] = maxPix
    
    # ret,thresh_binary_inv = cv2.threshold(z,127,255,cv2.THRESH_BINARY)
    image_from_array = Image.fromarray(img_grey)
    # cv2.imshow("normal", img_grey)
    # cv2.waitKey(0)
    #We can send the array directly to OCR, but I like to see the image.
    text = pytesseract.image_to_string(image_from_array, lang='eng', config='--psm 10')
    return text.upper()

# In Progress
def processGoldTile(img, img_grey):
    # specify circle parameters: centre ij and radius
    (x,y) = img_grey.shape
    (ci,cj) = (int(x/2), int(y/2))
    cr=int(y*.5*.7)

    # Min the value outside the letter radius
    maxPix = img_grey.max()
    for i in range(x):
        for j in range(y):
            if np.sqrt((i-ci)**2+(j-cj)**2) > cr:
                img_grey[i][j] = maxPix
    
    # ret,thresh_binary_inv = cv2.threshold(z,127,255,cv2.THRESH_BINARY)
    image_from_array = Image.fromarray(img_grey)
    # cv2.imshow("normal", img_grey)
    # cv2.waitKey(0)
    #We can send the array directly to OCR, but I like to see the image.
    text = pytesseract.image_to_string(image_from_array, lang='eng', config='--psm 10')
    return text.upper()

def processImg(img):
    image = cv2.imread(img)
    gray_image = cv2.imread(img, 0)

    zColor = np.array(image)
    z = np.array(gray_image)

    (x,y) = gray_image.shape

    bgX = int(.2*x)
    bgY = int(.2*y)
    bgColor = zColor[bgX,bgY, :]
    # print(bgColor, img.split('_')[1].split('.png')[0])

    # Determine type of tile:
    ratio = float(bgColor[2]/bgColor[1])
    # Fire
    if ratio > 1.29:
        print("See as Fire")
        text = processFireTile(zColor, z)
        print('Should have been: {}, got {}'.format(img.split('_')[0], text))
    # Normal
    elif ratio > 1.15:
        print("See as Normal")
        text = processNormalTile(z)
    # Gold
    elif ratio > 0.95:
        print("See as Gold")
        text = processGoldTile(zColor, z)
    # Green
    else:
        print("See as Green")
        text = processGreenTile(zColor, z)

    return text

# Loop over the letter images, use OpenCV to read the letter
def genLetterArray(lettersPath):
    letters = []
    for filename in os.listdir(lettersPath):
        # Reading picture with opencv
        img = lettersPath + '/' + filename
        text = processImg(img)
        if filename.split('_')[0].upper() != text:
            # print('Should have been: {}, got {}'.format(filename.split('_')[0], text))
            print(filename)

        letters.append(text)
    # return letters
    return testArray

# Generate a graph from an array of letters
def generateGraph(array):
    graph = {} 
    for i, node in enumerate(array):
        graph[i] = Node(
        nodeId = i,
        value = node,
        edges = graphMapping[i]
    )
    # print(graph)
    return graph


def main():
    # im = getGameBoard()
    # genLetterCrops(im)
    print('getting letters...')
    letters = genLetterArray(testLetterCrops)
    # print('generating graph...')
    graph = generateGraph(letters)
    # print('returning graph...')
    return graph

# # im = getGameBoard()
# # genLetterCrops(im)
# print('getting letters...')
# letters = genLetterArray(testLetterCrops)
# print('generating graph...')
# graph = generateGraph(letters)
# print('returning graph...')

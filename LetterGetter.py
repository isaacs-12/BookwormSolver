# This file:
#  Screenshot the game board
#  Crop every letter tile into 7x8=56 individual letters
#  Return a graph that contains all of the letters connected to each other as necessary
#  Called by WordGen.py, which will take this graph and determine the best words to attempt
from os import name
# import pyautogui
from PIL import Image
import os.path, sys
import csv
import cv2
import numpy as np
import pytesseract
from collections import namedtuple

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
    36:[28,2935,43,44],
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

# locationsFile = 'C:\Users\Isaac\Documents\BookwormSolver\BookwormLetterLocationsPIXEL.csv'
# outputDestination = 'C:\Users\Isaac\Documents\BookwormSolver\Letters'
thresholdOutputDestination = 'Letters'
# testFile = 'C:\Users\Isaac\Documents\BookwormSolver\TestBoard.png'
testLetterCrops = 'TestCroppedLetters'

# Screenshot board

# def getGameBoard():
#     # TODO
#     return Image.open(testFile)

# # Loop over letter zones to make 56 images for the graph
# def genLetterCrops(im):
#     for i, location in enumerate(locations[1:]):
#         imCrop = im.crop(location[0], location[1], location[2], location[3])
#         imCrop.save(outputDestination + str(i) + '_.png', quality=100)

def processImg2(img):
    # first multiplied by themselves four times to crank up contrast, 
    # and then pixels are considered "dark" if their value is less than 1/6 of the brightest pixel of the tile.
    print("Filename: {}".format(img))
    pic = cv2.imread(img)
    a = np.array(pic)
    ones = np.ones((len(a), len(a[0]), 3))
    pic1=pic**4
    pic1=pic1.astype('uint8')           
    cv2.imshow("image", pic1)
    cv2.waitKey(0)

    ones[0][0][0]=np.array(pic1)[0][0][0].max()*ones[0][0][0]
    ones[0][0][1]=np.array(pic1)[0][0][1].max()*ones[0][0][1]
    ones[0][0][2]=np.array(pic1)[0][0][2].max()*ones[0][0][2]
    

    pic1=pic1.astype('uint8')           
    cv2.imshow("image", np.array(pic1)[0])
    cv2.waitKey(0)

    return pic1


def processImg1(img):
    # Reading picture with opencv
    print("Filename: {}".format(img))
    pic = cv2.imread(img)
    text = pytesseract.image_to_string(pic)
    print('1 Read: {}'.format(text))
    
    # grey-scale the picture
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(pic)
    print('2 Read: {}'.format(text))
    
    # Do dilation and erosion to eliminate unwanted noises
    kernel = np.ones((1, 1), np.uint8)
    pic = cv2.dilate(pic, kernel, iterations=20)
    pic = cv2.erode(pic, kernel, iterations=20)
    text = pytesseract.image_to_string(pic)
    print('3 Read: {}'.format(text))
    
    #  threshold applying to get only black and white picture 
    pic = cv2.adaptiveThreshold(pic, 300, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    text = pytesseract.image_to_string(pic)
    print('4 Read: {}'.format(text))

    return pic
# Loop over the letter images, use OpenCV to read the letter
def genLetterArray(lettersPath):
    letters = []
    for filename in os.listdir(lettersPath):
        # Reading picture with opencv
        img = lettersPath + '/' + filename
        # pic1 = processImg1(img)
        pic2 = processImg2(img)
        print('Should have been: {}'.format(filename.split('_')[0]))

        # # Write the image for later recognition process 
        # cv2.imwrite(thresholdOutputDestination + str(i) + "threshold.png", pic)
        
        # # Character recognition with tesseract
        # final = pytesseract.image_to_string(Image.open(thresholdOutputDestination + str(i) + "threshold.png"))
        # print('Letter {index}: {value}'.format(str(i). final))
        # letters.append(final)
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



# im = getGameBoard()
# genLetterCrops(im)
print('getting letters...')
letters = genLetterArray(testLetterCrops)
graph = generateGraph(letters)
# return graph

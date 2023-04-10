import cv2

import matplotlib.pyplot as plt
import numpy as np

DEBUG = False

FILE_PATH = 'hsv.png'
FORMAT_STRING = "{0:>10} {1:>4} {2:>4} {3:>4} {4:>4} {5:>4} {6:>4}"

def noChange(a):
    pass
def t2Change(a):
    diff = cv2.getTrackbarPos("HueDiff", "Parameters")
    cv2.setTrackbarPos("hue1", "Parameters", a- diff)
def diffChange(a):
    h1 = cv2.getTrackbarPos("hue1", "Parameters")
    diff = cv2.getTrackbarPos("HueDiff", "Parameters")
    cv2.setTrackbarPos("hue2", "Parameters", h1+ diff)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 400)
cv2.createTrackbar("hue1", "Parameters", 0, 255, diffChange)

cv2.createTrackbar("HueDiff", "Parameters", 10, 100, diffChange)
cv2.createTrackbar("hue2", "Parameters", 10, 255, t2Change)



cv2.createTrackbar("sat1", "Parameters", 100, 255, noChange)
cv2.createTrackbar("value1", "Parameters", 20, 255, noChange)
cv2.createTrackbar("sat2", "Parameters", 255, 255, noChange)
cv2.createTrackbar("value2", "Parameters", 255, 255, noChange)
f = open("config", "r")
L = []
line =f.readline().split()
print(FORMAT_STRING.format(*line))
line =f.readline().split()
print(FORMAT_STRING.format(*line))
color, h1, h2, s1, s2, v1, v2 = line
h1 , h2, s1, s2, v1, v2 = [ int(x) for x in [h1, h2, s1, s2, v1, v2] ] 
cv2.setTrackbarPos("hue1", "Parameters", h1)
# cv2.setTrackbarPos("hue2", "Parameters", t2)
cv2.setTrackbarPos("HueDiff", "Parameters", h2-h1)
if not DEBUG:
    cam = cv2.VideoCapture(0)
while True:
    
    hue1 = cv2.getTrackbarPos("hue1", "Parameters")
    hue2 = cv2.getTrackbarPos("hue2", "Parameters")
    sat1 = cv2.getTrackbarPos("sat1", "Parameters")
    value1 = cv2.getTrackbarPos("value1", "Parameters")
    sat2 = cv2.getTrackbarPos("sat2", "Parameters")
    value2 = cv2.getTrackbarPos("value2", "Parameters")
    if (DEBUG):
        object = cv2.imread(FILE_PATH)
    else:
        ret, object = cam.read()
        if not ret:
            print("failed to grab frame")
            break
    og = object.copy()
    object = cv2.cvtColor(object, cv2.COLOR_BGR2HSV)
    light_color = (hue1, sat1, value1)
    dark_color = (hue2, sat2, value2)
    mask = cv2.inRange(object, light_color, dark_color)
    result = cv2.bitwise_and(og, og, mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours)>0):
        rect = cv2.minAreaRect(contours[0])
        center = [int(x) for x in rect[0]]
        # og = cv2.drawContours(og, contours, -1, (0,255,0), 3)
        # og = cv2.circle(og, (center), radius=5, color=(100, 100, 100), thickness=5)
        topP = [x -5 for x in center]
        botP = [x + 5 for x in center]
        og = cv2.circle(og, (topP), radius=2, color=(100, 100, 100), thickness=1)
        og = cv2.circle(og, (botP), radius=2, color=(100, 100, 100), thickness=1)
    
    cv2.imshow("test",og)
    cv2.imshow("mask",mask)
    cv2.imshow("segmentation",result)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        cv2.destroyAllWindows()
        break
    
    if(cv2.waitKey(1) & 0xFF == ord('\r')):
        print(light_color, dark_color)
        h1 = cv2.getTrackbarPos("hue1", "Parameters")
        h2 = cv2.getTrackbarPos("hue2", "Parameters")
        s1 = cv2.getTrackbarPos("sat1", "Parameters")
        s2 = cv2.getTrackbarPos("sat2", "Parameters")
        v1 = cv2.getTrackbarPos("value1", "Parameters")
        v2 = cv2.getTrackbarPos("value2", "Parameters")

        print("edited \n" + FORMAT_STRING.format(color, h1, h2, s1, s2, v1, v2))
        temp = " ".join([color, str(h1), str(h2), str(s1), str(s2), str(v1), str(v2), "\n"])

        L.append(temp)
        line =f.readline().split()
        if len(line) == 0:
            f.close()

            file1 = open('config1.txt', 'w')
            file1.writelines(L)
            file1.close()
            
            break
        print(FORMAT_STRING.format(*line))
        color, h1, h2, s1, s2, v1, v2 = line
        h1 , h2, s1, s2, v1, v2 = [ int(x) for x in [h1, h2, s1, s2, v1, v2] ] 
        cv2.setTrackbarPos("hue1", "Parameters", h1)
        # cv2.setTrackbarPos("hue2", "Parameters", t2)
        cv2.setTrackbarPos("HueDiff", "Parameters", h2-h1)
        cv2.setTrackbarPos("sat1", "Parameters", s1)
        cv2.setTrackbarPos("value1", "Parameters", v1)

        cv2.setTrackbarPos("sat2", "Parameters", s2)
        cv2.setTrackbarPos("value2", "Parameters", v2)

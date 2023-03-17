import cv2

import matplotlib.pyplot as plt
import numpy as np
def noChange(a):
    pass
def t2Change(a):
    diff = cv2.getTrackbarPos("difference", "Parameters")
    cv2.setTrackbarPos("threshold1", "Parameters", a- diff)
def diffChange(a):
    t1 = cv2.getTrackbarPos("threshold1", "Parameters")
    diff = cv2.getTrackbarPos("difference", "Parameters")
    cv2.setTrackbarPos("threshold2", "Parameters", t1+ diff)


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("threshold1", "Parameters", 0, 255, diffChange)

cv2.createTrackbar("difference", "Parameters", 10, 100, diffChange)
cv2.createTrackbar("threshold2", "Parameters", 10, 255, t2Change)



cv2.createTrackbar("threshold3", "Parameters", 100, 255, noChange)
cv2.createTrackbar("threshold4", "Parameters", 20, 255, noChange)
f = open("config", "r")
L = []
line =f.readline() 
print(line)
color, t1, t2 = line.split()
t1 , t2 = int(t1), int(t2)
cv2.setTrackbarPos("threshold1", "Parameters", t1)
# cv2.setTrackbarPos("threshold2", "Parameters", t2)
cv2.setTrackbarPos("difference", "Parameters", t2-t1)
while True:
    
    threshold1 = cv2.getTrackbarPos("threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("threshold2", "Parameters")
    threshold3 = cv2.getTrackbarPos("threshold3", "Parameters")
    threshold4 = cv2.getTrackbarPos("threshold4", "Parameters")
    object = cv2.imread('hsv.png')
    og = object.copy()
    object = cv2.cvtColor(object, cv2.COLOR_BGR2HSV)
    light_color = (threshold1, threshold3, threshold4)
    dark_color = (threshold1+ threshold2, 255, 255)
    mask = cv2.inRange(object, light_color, dark_color)
    result = cv2.bitwise_and(og, og, mask=mask)
    cv2.imshow("test",og)
    cv2.imshow("segmentation",result)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        cv2.destroyAllWindows()
        break
    if(cv2.waitKey(1) & 0xFF == ord('\r')):
        print(light_color, dark_color)
        t1 = cv2.getTrackbarPos("threshold1", "Parameters")
        t2 = cv2.getTrackbarPos("threshold2", "Parameters")
        temp = " ".join([color, str(t1), str(t2), "\n"])
        print("edited", temp)
        L.append(temp)
        line =f.readline() 
        print(line)
        if len(line) == 0:
            f.close()

            file1 = open('config1.txt', 'w')
            file1.writelines(L)
            file1.close()
            break
        color, t1, t2 = line.split()
        t1 , t2 = int(t1), int(t2)
        cv2.setTrackbarPos("threshold1", "Parameters", t1)
        # cv2.setTrackbarPos("threshold2", "Parameters", t2)
        cv2.setTrackbarPos("difference", "Parameters", t2-t1)

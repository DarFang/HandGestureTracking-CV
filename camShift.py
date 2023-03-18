import numpy as np
import cv2 as cv
import argparse
from CSTracker import CSTracker as cst
# parser = argparse.ArgumentParser(description='This sample demonstrates the meanshift algorithm. \
#                                               The example file can be downloaded from: \
#                                               https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
# parser.add_argument('image', type=str, help='path to image file')
# args = parser.parse_args()
# cap = cv.VideoCapture(args.image)
# # take first frame of the video
# ret,frame = cap.read()
# # setup initial location of window
# x, y, w, h = 300, 200, 100, 50 # simply hardcoded the values

numPoints = 2
def draw_point(event, x, y, flags, param):
   global Input, arrPoints
   if event == cv.EVENT_LBUTTONDOWN:
      Input = cv.circle(Input, (x,y), radius=5, color=(0, 0, 255), thickness=-1)
      arrPoints.append(np.array([x,y]))


cam = cv.VideoCapture(0)
arrPoints = []
while True:
    # read frame
    ret, frame = cam.read()
    cv.imshow("test", frame)
    k = cv.waitKey(1)
    if k%256 == 27:
    # ASCII:ESC pressed, exit
        print("Escape hit, closing...")
        break
ret, Input = cam.read()
cv.namedWindow("test")
cv.setMouseCallback("test", draw_point)
while len(arrPoints)<numPoints:
    # dIm[dIm>=80] = 255
    cv.imshow("test", Input)
    k = cv.waitKey(1)
    if k%256 == 27:
        break

t1 = cst("red", [*arrPoints[0], *arrPoints[1]],(180,255,255),  frame)
while(1):
    ret, frame = cam.read()
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        t1.updatePoints(hsv)
        frame = t1.drawPoly(frame)
        frame = t1.drawPt(frame, True)
        cv.imshow("frame", frame)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
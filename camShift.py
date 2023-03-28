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

numTrackers = 11
def draw_point(event, x, y, flags, param):
   global Input, arrPoints
   if event == cv.EVENT_LBUTTONDOWN:
      Input = cv.circle(Input, (x,y), radius=5, color=(0, 0, 0), thickness=-1)
      arrPoints.append(np.array([x,y]))
mirror = 0
SIZESAMPLING = [10, 5, 15, 10, 10, 15, 15, 10, 10, 10, 15]
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 1920  )
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
arrPoints = []
f = open("config1.txt", "r")
IDs = []
global colors 
colors = []
while True:
    line =f.readline().split()
    if len(line) == 0:
        break
    ID, *color = line
    colors.append([int(x) for x in color])
    IDs.append(ID)
while True:
    # read frame
    ret, frame = cam.read()
    if mirror:
        frame = cv.flip(frame, -1)
    cv.imshow("test", frame)
    k = cv.waitKey(1)
    if k%256 == 27:
    # ASCII:ESC pressed, exit
        print("Escape hit, closing...")
        break
    if k == ord('m'):
        mirror = not mirror
ret, Input = cam.read()
if mirror:
    Input = cv.flip(Input, -1)
cv.namedWindow("test")
cv.setMouseCallback("test", draw_point)
# while len(arrPoints)<numTrackers*2:
#     # dIm[dIm>=80] = 255
#     cv.imshow("test", Input)
#     k = cv.waitKey(1)
#     if k%256 == 27:
#         break
#     if k == ord('m'):
#         mirror = not mirror
def CalibrateHand(Input):
    arrPoints = []
    for i in range(numTrackers):
        hue1, hue2, sat1, sat2, value1, value2 = colors[i]
        light_color = (hue1, sat1, value1)
        dark_color = (hue2, sat2, value2)
        object = cv.cvtColor(Input, cv.COLOR_BGR2HSV)
        mask = cv.inRange(object, light_color, dark_color)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv.erode(mask, kernel, iterations=2)
        
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if(len(contours)>0):
            areas = [cv.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            rect = cv.minAreaRect(cnt)
            center = [int(x) for x in rect[0]]
            # og = cv2.drawContours(og, contours, -1, (0,255,0), 3)
            Input = cv.circle(Input, (center), radius=5, color=(100, 100, 100), thickness=5)
            # cv.imshow("test1", Input)
            # cv.imshow("test", mask)
            # cv.waitKey(0)
            arrPoints.append(np.array([x -SIZESAMPLING[i] for x in center])) 
            arrPoints.append(np.array([x +SIZESAMPLING[i] for x in center])) 
        else:
            arrPoints.append(np.array([0,0])) 
            arrPoints.append(np.array([1,1])) 




    # green 31 79 100 20 
    # red 0 10 100 20 
    # ID = ["red1", "orange2","yellow3", "green4", "green2_2m", "blue5", "blue2_3m", "purpB"]
    # calibration = [[0 ,8 ,100 ,20], 
    #                 [10 ,15 ,135 ,20], 
    #                 [20 ,38 ,164 ,20], 
    #                 [43 ,62 ,142 ,20],
    #                 [64, 87, 144, 20], 
    #                 [81, 106, 164, 20], 
    #                 [107, 121, 143, 20], 
    #                 [120, 159, 50, 20]  ]

    # red 0 8 100 20 
    # orange 10 15 135 20 
    # yellow 20 38 164 20 
    # green 43 62 142 20 
    # green2 64 87 144 20 
    # blue 81 106 164 20 
    # blue2 107 121 143 20 
    # purple 120 159 50 20 
    # pink 172 202 100 20 


    hand = []
    for i in range(numTrackers):
        print("ID",IDs[i])
        print(colors[i])
        print([*arrPoints[2*i], *arrPoints[2*i+1]])
        hand.append(cst(IDs[i],[*arrPoints[2*i], *arrPoints[2*i+1]] , colors[i], frame))
    return hand
    # t1 = cst("red1", [*arrPoints[0], *arrPoints[1]],[0,5,180, 20],  frame)
    # t2 = cst("orange2", [*arrPoints[2], *arrPoints[3]],[7,20,180, 20],  frame)
    # t3 = cst("green4", [*arrPoints[4], *arrPoints[5]],[31,79,180, 20],  frame)
    # hand = [t1, t2, t3]
hand = CalibrateHand(Input)
index = 0
while(1):
    ret, frame = cam.read()
    if mirror:
        frame = cv.flip(frame, -1)
    frameC = frame.copy()
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        for t in hand:
            t.updatePoints(hsv)
            frame = t.drawPoly(frame)
            frame = t.drawPt(frame, True)
        frame = cv.line(frame, hand[2].center, hand[6].center, color=(150, 150, 150), thickness=2) 
        midpoint = ((np.array(hand[2].center) + np.array(hand[6].center))/2).astype(int)
        frame = cv.circle(frame, midpoint[:], radius=5, color=(0, 0, 255), thickness=10)


        # dst = cv.warpPerspective(img1, H, (width,height))
        cv.imshow("hist", hand[index%numTrackers].dst)
        cv.imshow("frame", frame)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        if k == ord('m'):
            mirror = not mirror
        if k == ord('a'):
            index = index+1
        if k == ord('c'):
            hand = CalibrateHand(frameC)
        if k == ord('p'):
            while True:
                k = cv.waitKey(0)
                if k == ord('p'):
                    break
                if k == ord('a'):
                    index = index+1
                    cv.imshow("hist", hand[index%numTrackers].dst)

    else:
        break
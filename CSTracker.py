import numpy as np
import cv2 as cv
class CSTracker():
    def __init__(self, ID, pts, color, initFrame):
        self.dst = []
        self.ID = ID
        self.pts = pts
        self.color = color
        print(self.pts)
        x = pts[0]
        y = pts[1]
        w, h = pts[2]-x, pts[3]-y
        self.track_window = (x, y, w, h)
        roi = initFrame[y:y+h, x:x+w]
        hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((color[0], color[2],color[4])), np.array((color[1],color[3],color[5])))
        self.roi_hist = cv.calcHist([hsv_roi],[0],mask,[color[1]- color[0]],[color[0],color[1]])
        # mask = cv.inRange(hsv_roi, np.array((0, 20,100)), np.array((180,255,255)))
        # self.roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv.normalize(self.roi_hist,mask,0,50,cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by at least 1 pt
        self.term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )
        self.center = []
    
    def updatePoints(self, hsv):
        self.dst = cv.calcBackProject([hsv],[0],self.roi_hist,[self.color[0],self.color[1]],1)
        # apply camshift to get the new location
        ret, self.track_window = cv.CamShift(self.dst, self.track_window,self. term_crit)
        # Draw it on image
        self.pts = cv.boxPoints(ret)
        self.pts = np.int0(self.pts)
        self.center = [int(x) for x in ret[0]]

    def drawPoly(self, frame):
        return  cv.polylines(frame,[self.pts],True, color=(0, 0, 0),thickness = 2)
    def drawPt(self, frame, ID = False):
        frame = cv.circle(frame, (self.center), radius=5, color=(100, 100, 100), thickness=5)
        if ID:
            frame = cv.putText(frame, self.ID, (self.center), cv.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1, cv.LINE_AA)
        return frame
    
import numpy as np
import cv2 as cv
class CSTracker():
    def __init__(self, ID, pts, color, initFrame):
        self.dst = []
        self.ID = ID
        self.pts = pts
        print(self.pts)
        x = pts[0]
        y = pts[1]
        w, h = pts[2]-x, pts[3]-y
        self.track_window = (x, y, w, h)
        roi = initFrame[y:y+h, x:x+w]
        hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((color[0], color[2],color[3])), np.array((color[1],255,255)))
        self.roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv.normalize(self.roi_hist,self.roi_hist,0,255,cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by at least 1 pt
        self.term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 3 )
        self.center = []
    
    def updatePoints(self, hsv):
        self.dst = cv.calcBackProject([hsv],[0],self.roi_hist,[0,180],1)
        # apply camshift to get the new location
        ret, self.track_window = cv.CamShift(self.dst, self.track_window,self. term_crit)
        # Draw it on image
        self.pts = cv.boxPoints(ret)
        self.pts = np.int0(self.pts)
        self.center = [int(x) for x in ret[0]]

    def drawPoly(self, frame):
        return  cv.polylines(frame,[self.pts],True, 255,2)
    def drawPt(self, frame, ID = False):
        frame = cv.circle(frame, (self.center), radius=5, color=(0, 0, 255), thickness=-1)
        if ID:
            frame = cv.putText(frame, self.ID, (self.center), cv.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1, cv.LINE_AA)
        return frame
    
import cv2
import numpy as np

from vision.utils import crop_image_vertically, convert_bound_to_percent
from vision.tracker import Tracker

class EyeDetector:
    def __init__(self, frameSize) -> None:
        self.__haarCascade = cv2.CascadeClassifier('vision/data/haarcascade_eye.xml')
        self.__frameSize = frameSize

        self.__kernel = np.ones((5,5),np.uint8)

        self.__rightTracker = Tracker(frameSize)
        self.__leftTracker = Tracker(frameSize)

    def __preprocess(self, upperFaceFrame):
        gray = cv2.cvtColor(upperFaceFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray) 
    
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
        thresh = cv2.erode(thresh, self.__kernel, iterations = 1)

        return gray, thresh

    def find_eyes_with_haar_cascade(self, gray):
        objects = self.__haarCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=9)
        eyes = []
        for eye in objects:
            (x, y, w, h) = eye
            eyes.append((x, y, w, h))

        return eyes
    
    def find_eyes_with_contours(self, thresh):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

        eyes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            xP, yP, wP, hP = convert_bound_to_percent(x, y, w, h, thresh.shape)

            if(wP * hP < 0.0035 or hP / wP > 1.35):
                continue

            centerWP = xP + (wP/2)
            if(centerWP < 0.1 or centerWP > 0.9):
                continue

            eyes.append((x, y, w, h))
        return eyes

    def find_left_manual_eye(self, frameSize):
        height = int(frameSize[0] * 0.8)
        width = int(height)

        x = int(frameSize[1] * 0.2)
        y = int(frameSize[0] * 0.1)

        return (x, y, width, height)
    
    def find_right_manual_eye(self, frameSize):
        height = int(frameSize[0] * 0.8)
        width = int(height)

        x = int(frameSize[1] * 0.8 - width)
        y = int(frameSize[0] * 0.1)

        return (x, y, width, height)
    
    def split_eyes(self, eyes, frameSize):
        left_eyes = []
        right_eyes = []

        for eye in eyes:
            x, y, w, h = eye
            xP, yP, wP, hP = convert_bound_to_percent(x, y, w, h, frameSize)

            if(xP >= 0.5):
                right_eyes.append(eye)
            else:
                left_eyes.append(eye)
        return left_eyes, right_eyes
    
    def combine_eyes(self, eyes):
        eye = eyes[0]

        minX = eye[0]
        minY = eye[1]
        maxX = minX + eye[2]
        maxY = minY + eye[3]

        for (x, y, w, h) in eyes:
            minX = min(minX, x)
            minY = min(minY, y)

            maxX = max(maxX, x + w)
            maxY = max(maxY, y + h)

        return (minX, minY, maxX - minX, maxY - minY)
    
    def average_eyes(self, eye1, eye2, w1=0.5, w2=0.5):
        x = int((eye1[0]*w1 + eye2[0]*w2))
        y = int((eye1[1]*w1 + eye2[1]*w2))

        width = int((eye1[2]*w1 + eye2[2]*w2))
        height = int((eye1[3]*w1 + eye2[3]*w2))

        return (x, y, width, height)

    def detect(self, faceFrame):
        contrast = 2
        brightness = 5

        upperFaceFrame = crop_image_vertically(faceFrame, 0.25, 0.55)
        upperFaceFrame = cv2.convertScaleAbs(upperFaceFrame, alpha=contrast, beta=brightness)

        gray, thresh = self.__preprocess(upperFaceFrame)
        eyes = self.find_eyes_with_haar_cascade(gray) + self.find_eyes_with_contours(thresh)
    
        leftEyes, rightEyes = self.split_eyes(eyes, thresh.shape)

        leftEye = None
        if len(leftEyes) > 0:
            leftEye = self.combine_eyes(leftEyes)    
            #cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)        

        rightEye = None
        if len(rightEyes) > 0:
            rightEye = self.combine_eyes(rightEyes)    
            #cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)     

        (xl, yl, wl, hl) = self.find_left_manual_eye(thresh.shape)
        (xr, yr, wr, hr) = self.find_right_manual_eye(thresh.shape)

        if(leftEye is None):
            leftEye = (xl, yl, wl, hl)
        else:
            leftEye = self.average_eyes((xl, yl, wl, hl), leftEye, 0.75, 0.25)

        if(rightEye is None):
            rightEye = (xr, yr, wr, hr)
        else:
            rightEye = self.average_eyes((xr, yr, wr, hr), rightEye, 0.75, 0.25)

        (xl, yl, wl, hl) = leftEye
        (xr, yr, wr, hr) = rightEye

        (xl, yl, wl, hl) = self.__leftTracker.process(xl, yl, wl, hl)
        (xr, yr, wr, hr) = self.__rightTracker.process(xr, yr, wr, hr)

        #cv2.rectangle(upperFaceFrame, (xl, yl), (xl + wl, yl + hl), (0, 0, 255), thickness=2)  
        #cv2.rectangle(upperFaceFrame, (xr, yr), (xr + wr, yr + hr), (0, 255, 0), thickness=2)   

        """
        for (x, y, w, h) in leftEyes:
            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)

        for (x, y, w, h) in rightEyes:
            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
        """

        cv2.imshow("Upper Face", upperFaceFrame)
        #cv2.imshow("thresh", thresh)
        #cv2.imshow("gray", gray)

        leftEyeFrame = upperFaceFrame[yl:yl+hl, xl:xl+wl]
        rightEyeFrame = upperFaceFrame[yr:yr+hr, xr:xr+wr]



        return leftEyeFrame, rightEyeFrame
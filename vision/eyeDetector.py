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

    def detect(self, faceFrame):
        contrast = 2
        brightness = 5

        upperFaceFrame = crop_image_vertically(faceFrame, 0.25, 0.55)
        upperFaceFrame = cv2.convertScaleAbs(upperFaceFrame, alpha=contrast, beta=brightness)

        gray, thresh = self.__preprocess(upperFaceFrame)
        eyes = self.find_eyes_with_haar_cascade(gray) + self.find_eyes_with_contours(thresh)
    
        leftEyes, rightEyes = self.split_eyes(eyes, thresh.shape)

        if len(leftEyes) > 0:
            leftEye = self.combine_eyes(leftEyes)    
            (x, y, w, h) = leftEye
            (x, y, w, h) = self.__leftTracker.process(x, y, w, h)

            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)        

        if len(rightEyes) > 0:
            rightEye = self.combine_eyes(rightEyes)    
            (x, y, w, h) = rightEye
            (x, y, w, h) = self.__rightTracker.process(x, y, w, h)

            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)     

        """
        for (x, y, w, h) in leftEyes:
            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)

        for (x, y, w, h) in rightEyes:
            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
        """
            

        cv2.imshow("Upper Face", upperFaceFrame)
        #cv2.imshow("thresh", thresh)
        #cv2.imshow("gray", gray)

 
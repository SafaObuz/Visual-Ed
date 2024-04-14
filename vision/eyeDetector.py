import cv2
import numpy as np

from vision.utils import crop_image_vertically, convert_bound_to_percent

class EyeDetector:
    def __init__(self, frameSize) -> None:
        self.__haarCascade = cv2.CascadeClassifier('vision/data/haarcascade_eye.xml')
        self.__frameSize = frameSize

        self.__kernel = np.ones((5,5),np.uint8)

    def detect(self, faceFrame):
        contrast = 2
        brightness = 5

        upperFaceFrame = crop_image_vertically(faceFrame, 0.25, 0.55)
        upperFaceFrame = cv2.convertScaleAbs(upperFaceFrame, alpha=contrast, beta=brightness)
        gray = cv2.cvtColor(upperFaceFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray) 
        eyes = self.__haarCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=9)



        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
        
        
        thresh = cv2.erode(thresh, self.__kernel, iterations = 1)
        contours, hierarchy = cv2.findContours(thresh,  
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)

            xP, yP, wP, hP = convert_bound_to_percent(x, y, w, h, upperFaceFrame.shape)

            if(wP * hP < 0.005):
                continue

            if(wP < 0.1 or wP > 0.9):
                continue

            cv2.rectangle(upperFaceFrame,(x,y),(x+w,y+h),(0,0,255),2)

        for (x, y, w, h) in eyes:
            cv2.rectangle(upperFaceFrame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

        cv2.imshow("Upper Face", upperFaceFrame)
        #cv2.imshow("thresh", thresh)
        #cv2.imshow("gray", gray)

 
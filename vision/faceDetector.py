import cv2
import sys
import math

class FaceDetector:
    def __init__(self, frameSize) -> None:
        self.__haarCascade = cv2.CascadeClassifier('vision/data/haarcascade_frontalface_default.xml')
        self.__frameSize = frameSize

        self.__recentAreaPercent = 0
        self.__recentPos = (0, 0)
        self.__recentSize = (0, 0)
        self.__expectedAreaPercent = 0.1

    def __calculate_scores(self, faces):
        scores = []

        for (x, y, w, h) in faces:  
            self.__recentPos = (x, y)
            self.__recentSize = (w, h)

            aspectRatio = w/h
            if aspectRatio<0.8 or aspectRatio>1.2:
               continue

            areaPercent = (w * h) / (self.__frameSize[0] * self.__frameSize[0])
            score = 0
            
            score += abs(areaPercent - self.__expectedAreaPercent) * 1.5
            score += abs(areaPercent - self.__recentAreaPercent) * 0.5
            score += abs(x - self.__recentPos[0]) * 0.8
            score += abs(y - self.__recentPos[1]) * 0.8

            score = math.log((score * 0.5) + 1, math.e) * 3
            scores.append(score)

        return scores

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.__haarCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=9)

        if(len(faces) == 0):
           x, y = self.__recentPos
           w, h = self.__recentSize

           return (x, y, w ,h)

        scores = self.__calculate_scores(faces)

        bestFace = faces[0]
        minScore = scores[0]

        for t in range(len(scores)):
            if scores[t] < minScore:
                minScore = scores[t]
                bestFace = faces[t]

        return bestFace
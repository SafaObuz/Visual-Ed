import cv2

from vision.camera import Camera
from vision.faceDetector import FaceDetector
from vision.eyeDetector import EyeDetector
from vision.tracker import Tracker

cameraRes = (480, 640)

camera = Camera(cameraRes=cameraRes)

faceDetector = FaceDetector(cameraRes)
EyeDetector = EyeDetector(cameraRes)

tracker = Tracker(cameraRes)

while True:
    frame = camera.get_frame()
    
    face = faceDetector.detect(frame)

    (x, y, w, h) = face
    
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
    #cv2.circle(frame, (x, y), 12, (0,0,255), -1)

    (x, y, w, h) = tracker.process(x, y, w, h)


    faceFrame = frame[y:y+h, x:x+w]
    EyeDetector.detect(faceFrame)

    #cv2.circle(frame, (x, y), 12, (0,255,0), -1)

    #cv2.imshow("Face", faceFrame)

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
    #cv2.imshow('frame', frame)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
camera.close()
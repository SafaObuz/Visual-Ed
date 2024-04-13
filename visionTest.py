import cv2

from vision.camera import Camera
from vision.faceDetector import FaceDetector
from vision.tracker import Tracker

cameraRes = (480, 640)

camera = Camera(cameraRes=cameraRes)
faceDetector = FaceDetector(cameraRes)
tracker = Tracker(cameraRes)

while True:
    frame = camera.get_frame()
    
    face = faceDetector.detect(frame)

    (x,y,w,h) = face
    x, y, w, h = tracker.process(x, y, w, h)

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

    #for (x, y, w, h) in faces:
    #    
 
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
camera.close()
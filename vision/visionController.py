import cv2

from vision.camera import Camera
from vision.faceDetector import FaceDetector
from vision.eyeDetector import EyeDetector
from vision.eyeTracker import EyeTracker

from vision.tracker import Tracker

class VisionController:
    def __init__(self) -> None:
        self.__cameraRes = (480, 640)
        self.__camera = Camera(cameraRes=self.__cameraRes)

        self.__faceDetector = FaceDetector(self.__cameraRes)
        self.__faceTracker = Tracker(self.__cameraRes)

        self.__eyeDetector = EyeDetector(self.__cameraRes)
        self.__leftEyeTracker = EyeTracker()
        self.__rightEyeTracker = EyeTracker()

    def process_step(self):
        try:
            frame = self.__camera.get_frame()
            face = self.__faceDetector.detect(frame)

            (x, y, w, h) = face
            (x, y, w, h) = self.__faceTracker.process(x, y, w, h)

            faceFrame = frame[y:y+h, x:x+w]
            if(faceFrame.shape[0] == 0 or faceFrame.shape[1] == 0):
                print("Couldn't find face!")
                return None
            
            leftEyeFrame, rightEyeFrame = self.__eyeDetector.detect(faceFrame)

            leftEyeResult = self.__leftEyeTracker.track(leftEyeFrame)
            rightEyeResult = self.__rightEyeTracker.track(rightEyeFrame)

            totalResult = leftEyeResult or rightEyeResult
            return totalResult
        except Exception as e:
            print("Error: " + str(e))
            return None

    def process(self, n=40):
        yes = 0
        no = 0

        index = 0
        while index<=n:
            result = self.process_step()
            if result is None:
                continue

            if(result == True):
                yes+=1
            else:
                no+=1
            index+=1

        return yes>no

        

    def close(self):
        cv2.destroyAllWindows()
        self.__camera.close()
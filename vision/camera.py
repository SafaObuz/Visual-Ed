import cv2

class Camera:
    def __init__(self, cameraRes = (640, 480), cameraFPS = 30) -> None:
        self.__cameraRes = cameraRes
        self.__cameraFPS = cameraFPS

        self.__camVideo = cv2.VideoCapture(0, cv2.CAP_V4L2)

        self.__camVideo.set(cv2.CAP_PROP_FPS, self.__cameraFPS)
        self.__camVideo.set(cv2.CAP_PROP_FRAME_WIDTH, self.__cameraRes[0])
        self.__camVideo.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__cameraRes[1])

    def get_frame(self):
        ret, frame = self.__camVideo.read()
        return frame
    
    def close(self):
        self.__camVideo.release()
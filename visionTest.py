import cv2
from vision.visionController import VisionController

visionController = VisionController()

while True:
    visionController.process()
    
visionController.close()
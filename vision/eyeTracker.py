import cv2
import numpy as np
import matplotlib.pyplot as plt

from vision.utils import crop_image_horizontally, crop_image_vertically

class EyeTracker:
    def __init__(self) -> None:
        self.__kernel = np.ones((5,5),np.uint8)

    def compare_two_images(self, src, ref):
        ref = cv2.resize(ref, (src.shape[1], src.shape[0]))
        w, h = ref.shape[1], ref.shape[0]

        diff = cv2.subtract(ref, src)
        cv2.imshow("diff", diff)

        err = np.sum(diff**2)
        mse = err/(float(h*w))

        print(mse)

    def calculate_entropy(self, image):
        hist, _ = np.histogram(image, bins=256, range=(0, 255))
        hist = hist / np.sum(hist)

        entropy = -np.sum(hist * np.log2(hist + 1e-12))
        return entropy
    

    def track(self, eyeFrame):
        if eyeFrame is None:
            return

        #cv2.imshow("EyeFrame", eyeFrame)
    
        gray = cv2.cvtColor(eyeFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray) 
        gray = 255 - gray

        for t in range(200, 250, 3):
            ret,thresh = cv2.threshold(gray, t,255,cv2.THRESH_BINARY)
            entropy = self.calculate_entropy(thresh)
            
            if(entropy <= 0.55):
                break  

        #print(str("Entropy:") + t)
        #cv2.imshow("Thresh-old", thresh)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

        for t in range(1, 20, 1):
            numberOfBoxes = 0
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)

                if(w/h >= 1.2+(t/30)):
                    thresh = cv2.rectangle(thresh, (x, y), (x+w, y+h), (0), -1)
                else:
                    numberOfBoxes+=1 

            if(numberOfBoxes >= 1 and numberOfBoxes <= 3):
                break
        #print("Min Limit Index: " + str(t))

        thresh = cv2.dilate(thresh,self.__kernel, iterations = 1)

        #cv2.imshow("Thresh", thresh)
        cv2.imshow("Eye Gray", gray)

        numOfWhitePixels = np.sum(thresh >= 255)
        whitePixelPercent = numOfWhitePixels / (eyeFrame.shape[0] * eyeFrame.shape[1])

        if(whitePixelPercent>0.065):
            return True
        return False

        """
        eyeFrame = crop_image_vertically(eyeFrame, 0.20, 0.98)
        eyeFrame = crop_image_horizontally(eyeFrame, 0.12, 0.93)

        gray = cv2.cvtColor(eyeFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray) 

        ret,thresh = cv2.threshold(gray, 20,255,cv2.THRESH_BINARY_INV)

        hist = np.sum(gray, axis=0)

        
        plt.plot(hist)
        plt.title('Vertical Histogram')
        plt.xlabel('Column Index')
        plt.ylabel('Sum of Pixel Values')
        #plt.show()
        plt.savefig("hist.png")

        cv2.imshow("Gray", gray)
        cv2.imshow("Thresh", thresh)
        #cv2.imwrite("LeftEye_Up.png", gray)

        """

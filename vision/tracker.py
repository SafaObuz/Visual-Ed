import cv2
import numpy as np

class Tracker:
    def __init__(self, size) -> None:
        # Initialize the Kalman filter with 4 state variables (x, y, width, and height) and 4 measurement variables (x, y, width, height)
        self.__kalman = cv2.KalmanFilter(4, 4)

        # Define the state transition matrix (A)
        self.__kalman.transitionMatrix = np.array([[1, 0, 0.1, 0],
                                                    [0, 1, 0, 0.1],
                                                    [0, 0, 1, 0],
                                                    [0, 0, 0, 1]], np.float32)

        # Define the measurement matrix (H)
        self.__kalman.measurementMatrix = np.eye(4, dtype=np.float32)

        # Define the process noise covariance (Q)
        self.__kalman.processNoiseCov = np.eye(4, dtype=np.float32)
        self.__kalman.processNoiseCov[0,0] = 0.1 # X Pos
        self.__kalman.processNoiseCov[1,1] = 0.1 # Y Pos
        self.__kalman.processNoiseCov[2,2] = 0.05 # Width
        self.__kalman.processNoiseCov[3,3] = 0.05 # Height

        # Define the measurement noise covariance (R)
        self.__kalman.measurementNoiseCov = np.eye(4, dtype=np.float32)
        self.__kalman.measurementNoiseCov[0,0] = 0.008 # X Pos
        self.__kalman.measurementNoiseCov[1,1] = 0.008 # Y Pos
        self.__kalman.measurementNoiseCov[2,2] = 0.01 # Width
        self.__kalman.measurementNoiseCov[3,3] = 0.01 # Height

        # Define the error covariance (P)
        self.__kalman.errorCovPost = np.eye(4, dtype=np.float32)

        # Define the initial state vector
        self.__kalman.statePost = np.zeros((4, 1), dtype=np.float32)

    def process(self, x, y, width, height):
        prediction = self.__kalman.predict()

        measurement = np.array([[np.float32(x)], [np.float32(y)], [np.float32(width)], [np.float32(height)]])
        self.__kalman.correct(measurement)

        estimated_state = self.__kalman.statePost.ravel()
        estimated_x, estimated_y, estimated_width, estimated_height = estimated_state

        return int(estimated_x), int(estimated_y), int(estimated_width), int(estimated_height)


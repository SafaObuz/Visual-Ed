import cv2

def resize_image(frame, percent):
    if percent == 100:
        return frame

    height, width, channels = frame.shape
    aspectRatio = height / width

    newWidth = int(width * (percent/100))
    newHeight = int(newWidth / aspectRatio)

    resized = cv2.resize(frame, (newHeight, newWidth))
    return resized

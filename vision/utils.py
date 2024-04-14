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

def crop_image_vertically(frame, topRatio, bottomRatio):
    topPixels = int(frame.shape[0] * topRatio)
    bottomPixels = int(frame.shape[1] * bottomRatio)

    return frame[topPixels:bottomPixels, 0:frame.shape[1]]

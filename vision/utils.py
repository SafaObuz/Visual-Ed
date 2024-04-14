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

def crop_image_horizontally(frame, leftRatio, rightRatio):
    leftPixels = int(frame.shape[1] * leftRatio)
    rightPixels = int(frame.shape[1] * rightRatio)

    return frame[0:frame.shape[0], leftPixels:rightPixels]

def crop_image_vertically(frame, topRatio, bottomRatio):
    topPixels = int(frame.shape[0] * topRatio)
    bottomPixels = int(frame.shape[0] * bottomRatio)

    return frame[topPixels:bottomPixels, 0:frame.shape[1]]

def convert_bound_to_percent(x, y, width, height, frameShape):
    xPercent = x / frameShape[1]
    yPercent = y / frameShape[0]

    widthPercent = width / frameShape[1]
    heightPercent = height / frameShape[0]

    return xPercent, yPercent, widthPercent, heightPercent
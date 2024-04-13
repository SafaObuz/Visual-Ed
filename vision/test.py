import cv2

camera = cv2.VideoCapture(1)
haarCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = haarCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=9)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



camera.release()
cv2.destroyAllWindows()
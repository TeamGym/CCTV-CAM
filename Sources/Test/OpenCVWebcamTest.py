import cv2
import time

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("[cv2.VideoCapture]: can't open")
    sys.exit()

while True:
    ret, frame = capture.read()

    startTime = time.time()

    if not ret:
        break

    cv2.imshow('webcam', frame)

    endTime = time.time()

    elapsedTime = endTime - startTime
    sleepTime = max(int(33 - elapsedTime / 1000), 0)

    if sleepTime > 0:
        cv2.waitKey(sleepTime)

capture.release()
cv2.destroyAllWindows()

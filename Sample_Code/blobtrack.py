import numpy as np
import argparse
import cv2

# Syntax: python blobtrack.py -v "blank.avi"

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

# if no video, use webcam
if not args.get("video", False):
	nome = 0
else:
	nome = args["video"]

cap = cv2.VideoCapture(nome)

ret, frame = cap.read()
detector = cv2.SimpleBlobDetector_create()


skin_ycrcb_mint = np.array((0, 133, 77))
skin_ycrcb_maxt = np.array((255, 173, 127))

while(cap.isOpened()):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame2 = frame
	
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area > 1000:
            cv2.drawContours(frame2, contours, i, (255, 0, 0), 3)
	
    cv2.imshow('frame',frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

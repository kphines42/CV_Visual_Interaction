import cv2
import numpy as np

def blob(binary_frame,frame):
	
	temp = np.copy(binary_frame)
	_, contours, _ = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for i, c in enumerate(contours):
		area = cv2.contourArea(c)
		if area > 1000:
			cv2.drawContours(frame, contours, i, (255, 0, 0), 3)

	return frame, contours

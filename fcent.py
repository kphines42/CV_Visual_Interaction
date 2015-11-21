import cv2
import numpy as np

def fcent(contours, area_limit):
	#Initialize variable which change with each frame
	objectx = []
	objecty = []
	
	#Find contours around blobs
	for i, c in enumerate(contours):
		area = cv2.contourArea(c)
		if area > area_limit:
			cent = cv2.moments(c)
			temp = cent['m00']
			if not temp == 0:
				cx = int(cent['m10']/cent['m00'])
				cy = int(cent['m01']/cent['m00'])
				objectx.append(cx)
				objecty.append(cy)
	
	return objectx, objecty

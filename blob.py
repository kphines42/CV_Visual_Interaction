#blob.py: Two functions that are the exact same but return different things.
#	[frame, contours] = blob(binary_frame, frame, area_limit)
#	[frame,contours,defects] = blob2(binary_frame,frame,area_limit)

import cv2
import numpy as np

def blob(binary_frame,frame,area_limit):
	
	temp = np.copy(binary_frame)
	_, contours, _ = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contours:
		area = cv2.contourArea(c)
		if area > area_limit:
			hull = cv2.convexHull(c,returnPoints = False)
			defects = cv2.convexityDefects(c,hull)
			
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(c[s][0])
				end = tuple(c[e][0])
				cv2.line(frame,start,end,[0,255,0],2)
	
	return frame, contours

def blob2(binary_frame,frame,area_limit):
	
	temp = np.copy(binary_frame)
	_, contours, _ = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contours:
		area = cv2.contourArea(c)
		if area > area_limit:
			hull = cv2.convexHull(c,returnPoints = False)
			defects = cv2.convexityDefects(c,hull)
			
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(c[s][0])
				end = tuple(c[e][0])
				cv2.line(frame,start,end,[0,255,0],2)
	
	return frame, contours, defects

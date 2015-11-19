#gesture.py: gestures needed to start and stop the function.
#	start = startGest(imageBW, imageContour)
#	stop  = stopGest(imageBW,  imageContour)

import cv2
import numpy as np
import math
#from skin2BW import skin2BW

def start = startGest(imageBW, imageContours):
	#Start by finding the contours
	max_area = -1
    for i in range(len(imageContours)):
        cnt=imageContours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=imageContours[ci]
	
	#Draw a bounding rectangle around the image contour area
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(imageBW,(x,y),(x+w,y+h),(0,0,255),0)
	
	#Find the hull
    #hull = cv2.convexHull(cnt)
    #drawing = np.zeros(imageBW.shape,np.uint8)
    #cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    #cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(imageBW, imageContours, -1, (0,255,0), 3)
	
	#Determine the spaces in between the fingers.
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
			if angle >= 20:
				count_defects += 1
				cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        #cv2.line(imageBW,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count_defects >= 3:
        cv2.putText(img,"Start", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
		start = 1
	else:
		start = 0
	return start
	
def stop = stopGest(imageBW, imageContour):
	#Start by finding the contours
	max_area = -1
    for i in range(len(imageContours)):
        cnt=imageContours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=imageContours[ci]
	
	#Draw a bounding rectangle around the image contour area
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(imageBW,(x,y),(x+w,y+h),(0,0,255),0)
	
	#Find the hull
    #hull = cv2.convexHull(cnt)
    #drawing = np.zeros(imageBW.shape,np.uint8)
    #cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    #cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(imageBW, imageContours, -1, (0,255,0), 3)
	
	#Determine the spaces in between the fingers.
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
			if angle >= 20:
				count_defects += 1
				cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        #cv2.line(imageBW,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count_defects <= 2:
        cv2.putText(img,"Stop", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
		stop = 1
	else:
		stop = 0
	return stop
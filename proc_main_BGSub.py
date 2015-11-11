import numpy as np
import argparse
import cv2
import os
import mahotas as mh
from skin2BW import skin2BW, personalSkin2BW
from findMinMaxSkin import findMinMaxSkin
#from init_func import rmBG, rmFace

def blob(binary_frame,frame):

	_, contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for i, c in enumerate(contours):
		area = cv2.contourArea(c)
		if area > 1000:
			cv2.drawContours(frame, contours, i, (255, 0, 0), 3)

	return frame, contours

	
	
def main():
	


	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help = "path to the (optional) video file")
	args = vars(ap.parse_args())

	fgbg = cv2.createBackgroundSubtractorMOG2()
	
	# if no video, use webcam
	if not args.get("video", False):
		nome = 0
	else:
		nome = args["video"]
	
	cap = cv2.VideoCapture(nome)

	ret, frame = cap.read()

	objectx_old = []
	objecty_old = []
	
	ret, frame = cap.read()
	#binary_frame = skin2BW(frame)
	minSkin,maxSkin = findMinMaxSkin(frame)
	
	#print minSkin
	#print maxSkin
	
	while(cap.isOpened()):

		#ret, frame = cap.read()
		
		fgmask = fgbg.apply(frame)
		masked_frame = cv2.bitwise_and(frame,frame,mask = fgmask)
		binary_frame = personalSkin2BW(masked_frame,minSkin,maxSkin)#skin2BW(frame)
		
		
		frame, contours = blob(binary_frame,frame)

		if not ret == False:
		
			objectx = []
			objecty = []
		
			for i, c in enumerate(contours):
				area = cv2.contourArea(c)

				if area > 1000:
			
					cent = cv2.moments(c)
					temp = cent['m00']
					if not temp == 0:
						cx = int(cent['m10']/cent['m00'])
						cy = int(cent['m01']/cent['m00'])
						#cv2.circle(frame,(cx,cy),5,(0,0,255),-2)
						objectx.append(cx)
						objecty.append(cy)
						#print objectx, objecty
			#os.system("pause")
			
			objectloc = []
			objectval = []
			x = []
			y = []
			
			if not objectx_old == []:
				#print objectx, objecty, objectx_old, objecty_old
				
				for i, j in zip(objectx, objecty):
	
					x_dist = np.array(objectx_old)
					x_dist = x_dist - i
					y_dist = np.array(objecty_old)
					y_dist = y_dist - j
					
					y_dist = np.square(y_dist)
					x_dist = np.square(x_dist)
					
					dist = np.sqrt(x_dist+y_dist)
					minloc = np.argmin(dist)
					minval = dist[minloc]
					objectloc.append(minloc)
					objectval.append(minval)
					x.append(i)
					y.append(j)
			if not objectloc == []:
				co = len(objectloc)
				for i in range(0, co-1):
					if objectval[i] > 2:
						cv2.circle(frame,(x[i],y[i]),5,(0,0,255),-2)
			objectx_old = objectx
			objecty_old = objecty

		else:
			break
		
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		ret, frame = cap.read()
		
	#print "Out of the while loop"
		
	cap.release()
	cv2.destroyAllWindows()

	
	
	
main()

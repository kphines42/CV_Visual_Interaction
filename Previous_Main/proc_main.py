import numpy as np
import argparse
import cv2
import os
import mahotas as mh

def blob(binary_frame,frame):

	_, contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for i, c in enumerate(contours):
		area = cv2.contourArea(c)
		if area > 1000:
			cv2.drawContours(frame, contours, i, (255, 0, 0), 3)

	return frame, contours

def skin2BW(frame):
	imageIn = frame
	imageYCrCb = cv2.cvtColor(imageIn,cv2.COLOR_BGR2YCR_CB) #Cr and Cb are switched

	imageY  = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	imageCr = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	imageCb = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	imageBW = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)

	#Split the channels
	imageY  = cv2.split(imageYCrCb)[0]
	imageCr = cv2.split(imageYCrCb)[1]
	imageCb = cv2.split(imageYCrCb)[2]

	#Filter based on luminescence and chromatic channels
	imageY_S = imageY > 80

	imageCr_S1 = imageCr > 135	
	imageCr_S2 = imageCr < 180
	imageCr_S = imageCr_S1 & imageCr_S2

	imageCb_S1 = imageCb > 85
	imageCb_S2 = imageCb < 135
	imageCb_S = imageCb_S1 & imageCb_S2

	#Boolean matrix of the skin possibilities
	imageBWTemp = imageY_S & imageCr_S
	imageBW = imageBWTemp & imageCb_S
	#imageBW = mh.morph.dilate(imageBW)
	#imageBW = mh.morph.dilate(imageBW)
	#imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.close(imageBW)
	
	#Convert imageBW to uint8
	imageBW = imageBW.astype(int)*255
	imageBW = imageBW.astype(np.uint8)
	
	#Return BW image
	return imageBW
	
	
def main():
	


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

	objectx_old = []
	objecty_old = []
	
	while(cap.isOpened()):

		ret, frame = cap.read()
		
		binary_frame = skin2BW(frame)
		
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

	cap.release()
	cv2.destroyAllWindows()

	
	
	
main()

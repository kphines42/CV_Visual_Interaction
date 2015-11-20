import numpy as np
import argparse
import cv2
import os
import mahotas as mh
from skin2BW import skin2BW, personalSkin2BW
from findMinMaxSkin import findMinMaxSkin, findMinMaxHand
from blob import blob, blob2
import matplotlib.pyplot as plt
from gesture import startGest, stopGest
from trackObj import trackObj,trackObj2

def unique(a):
    a = np.sort(a)
    b = np.diff(a)
    b = np.r_[1, b]
    return a[b != 0]
	
def testGest(gesture_flag,gesture_cnt, cnt):
	if gesture_flag == 1 and gesture_cnt < 10:
		gesture_cnt = gesture_cnt + 1
		gesture_flag = 0
		#print "counting..."
	else:
		gesture_flag = 1
		gesture_cnt = 0
		cnt = 0
		
	
	return gesture_flag, gesture_cnt,cnt

def main():
	
	#Define flags for face detection and background detection
	face_flag  = 0
	bg_flag    = 1
	gest_flag  = 1
	
	#Flags used for collection of data
	start_flag = 0
	stop_flag  = 0
	
	#Set arbitrary limits
	wait_limit = 45 # number of frames before ending action
	area_limit = 500 # pixels squared
	
	#About a delay with a threshold of 50 (intensity)
	fgbg = cv2.createBackgroundSubtractorMOG2(50000,100)
	
	#Parse all of the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help = "path to the (optional) video file")
	args = vars(ap.parse_args())
	
	# if no video, use webcam
	if not args.get("video", False):
		nome = 0
	else:
		nome = args["video"]
	
	# Capture first frame
	
	cap = cv2.VideoCapture(nome)
	ret, frame = cap.read()
	if cap.isOpened():
		print "Success\n"
	else:
		print "Unable to open file/webcam"
		return

	# Create some random colors
	color = np.random.randint(0,255,(100,3))
	
	#Find face if flagged
	if face_flag == 1:
		minSkin,maxSkin = findMinMaxHand(frame)#findMinMaxSkin(frame)
		#print minSkin
		#print maxSkin


	#Initialize arrays, counters, masks, etc
	objectx_old = []
	objecty_old = []
	
	#Starting all of the counters
	ct = 0
	ct1 = 0
	ct2 = 0
	start_cnt = 0
	stop_cnt  = 0
	
	#Creating mask arrays
	sz = np.shape(frame)
	mask = np.zeros(shape=(sz[0],sz[1],3,20), dtype = np.uint8)
	mask_old = np.copy(mask)
	tim = np.zeros(20)
	
	#Loop through each frame
	while(cap.isOpened()):
		
		#If background subtraction is on, do that
		if bg_flag == 1:
			fgmask = fgbg.apply(frame)
			masked_frame = cv2.bitwise_and(frame,frame,mask = fgmask)
		else:
			masked_frame = frame

		#If face detection is on, use personalized skin hue for binary conversion
		if face_flag == 1:
			binary_frame = personalSkin2BW(masked_frame,minSkin,maxSkin)
		#elif gest_flag == 1:
		#	frame = cv2.line(frame,(40,200),(600,200),(0,255,0),2)
		#	crop_img = frame[200:600, 40:600]
		#	binary_frame = skin2BW(crop_img)
		else:
			binary_frame = skin2BW(masked_frame)
		
		#Find blobs in binary image
		if gest_flag == 1:
			__ , contours, contoursOut, defects = blob2(binary_frame,frame,area_limit)
		else:
			frame, contours = blob(binary_frame,frame,area_limit)
		
		#Show binary image
		cv2.imshow('frame',binary_frame)
		
		#Check if a frame was found
		if not ret == False:
						
			if gest_flag == 1:
				if not defects == []:
					if start_flag == 0 and stop_flag == 0:
						print "Looking for start..."
						#cv2.waitKey(10)
						#os.system("pause")
						start_flag = startGest(frame,contoursOut,defects)
						(start_flag,start_cnt,ct2) = testGest(start_flag,start_cnt,ct2)
						stop_flag = 0
						img = frame
					elif start_flag == 1 and ct1<10:
						cv2.putText(frame,"Start",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)
						print "Start"
						ct1 = ct1+1
						ct2 = 0
						stop_flag = 0
						#print "ct1"
						#print ct1
						#cv2.waitKey(27)
						(img,objectx_old,objecty_old,mask,mask_old) = trackObj2(frame,contours,objectx_old,objecty_old,mask,mask_old, area_limit)
						
						
						
					elif start_flag == 1 and ct1 >= 10:
						#Looking for stop...
						#print "Looking for stop ..."
						stop_flag = stopGest(frame,contoursOut,defects)
						(stop_flag,stop_cnt,ct1) = testGest(stop_flag,stop_cnt,ct1)
						#print stop_cnt
						if stop_flag == 1:
							start_flag = 0
							
						(img,objectx_old,objecty_old,mask,mask_old) = trackObj2(frame,contours,objectx_old,objecty_old,mask,mask_old,area_limit)
					
					
					elif stop_flag == 1 and ct2 < 1:
						#Stop Gesture collection
						cv2.putText(frame,"Stop",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)
						print "Stop"
						#start_flag = 0
						ct1 = 0
						ct2 = ct2+1
										
						img = frame
					elif stop_flag == 1 and ct2 >= 10:
						#Clear out all flags after being stopped for X amount of time
						start_flag = 0
						stop_flag  = 0
						ct1 = 0
						ct2 = 0
						
						print "Output mask created. \n"
						mask_output = mask_old
						objectx_old = []
						objecty_old = []
						
						img = frame
				else: #If the defects aren't found, do nothing
					#print "Defects do not exist. \n"
					img = frame
			
			else: #If not using the gestures to start and stop the function...
				#Initialize variable which change with each frame
				(img,objectx_old,objecty_old,mask,mask_old,tim) = trackObj(frame,contours,objectx_old,objecty_old,mask,mask_old,area_limit,tim)

		#If the frame was not found o' so long ago...
		else:
			break
		
		#Increment frame counter
		ct = ct+1
		#Show frame with magic applied
		cv2.imshow('frame',img)
		
		#Check for break code
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		ret, frame = cap.read()
		
	cap.release()
	cv2.destroyAllWindows()

	
	
	
main()

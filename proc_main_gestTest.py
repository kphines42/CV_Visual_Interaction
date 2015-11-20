import numpy as np
import argparse
import cv2
import os
import mahotas as mh
from skin2BW import skin2BW, personalSkin2BW
from findMinMaxSkin import findMinMaxSkin, findMinMaxHand
from blob import blob2
from gesture import startGest, stopGest
import matplotlib.pyplot as plt
from trackObj import trackObj, trackObj2

def unique(a):
    a = np.sort(a)
    b = np.diff(a)
    b = np.r_[1, b]
    return a[b != 0]

def main():
	
	#Define flags for face detection and background detection
	face_flag  = 0
	bg_flag    = 1
	start_flag = 0
	stop_flag  = 0
	
	#Set arbitrary limits
	wait_limit = 45 # number of frames before ending action
	area_limit = 0 # pixels squared
	
	#About a delay with a threshold of 50 (intensity)
	fgbg = cv2.createBackgroundSubtractorMOG2(500,50)
	bgLim = 10000
	
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
	
	bg_cnt = 0
	ct1 = 0
	ct2 = 0
	start_cnt = 0
	stop_cnt  = 0
	
	sz = np.shape(frame)
	mask = np.zeros(shape=(sz[0],sz[1],3,20), dtype = np.uint8)
	mask_old = np.copy(mask)
	tim = np.zeros(20)
	
	#Loop through each frame
	while(cap.isOpened()):
		
		#If background subtraction is on, do that
		if bg_flag == 1:
			#if bg_cnt <= bgLim:
			fgmask = fgbg.apply(frame)
			#bg_cnt = bg_cnt+1;
				#print "Apply BG Sub"
			masked_frame = cv2.bitwise_and(frame,frame,mask = fgmask)
			
		else:
			masked_frame = frame

		#If face detection is on, use personalized skin hue for binary conversion
		if face_flag == 1:
			binary_frame = personalSkin2BW(masked_frame,minSkin,maxSkin)
		#else:
		#	binary_frame = skin2BW(masked_frame)
		
		frame = cv2.line(frame,(40,200),(600,200),(0,255,0),2)
		#crop_img = frame[200:600, 40:600]
		
		binary_frame = skin2BW(frame)
		binary_frame[0:199][:] = 0
		
		cv2.imshow('BW Frame',binary_frame)
		#Find blobs in binary image
		__ , contours, contoursOut, defects = blob2(binary_frame,frame,area_limit)
		
		if not defects == []:
			#print "Defects Exist\n"
			#Check flags to see what text should be displayed...
			if start_flag == 0 and stop_flag == 0:
				#print "Looking for start"
				start_flag = startGest(frame,contoursOut,defects)
				if start_flag == 1 and start_cnt < 10:
					start_cnt = start_cnt+1
					start_flag = 0
				else:
					start_cnt = 0
				stop_flag = 0
			elif start_flag == 1 and ct1<10:
				cv2.putText(frame,"Start", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
				print "Start"
				ct1 = ct1+1
				ct2 = 0	
			elif start_flag == 1 and ct1>=10:
				#print "Looking for stop"
				stop_flag = stopGest(frame,contoursOut,defects)
				if stop_flag == 1 and stop_cnt < 10:
					stop_cnt = stop_cnt+1
					stop_flag = 0
				else:
					stop_cnt = 0
					
				(frame,objectx_old,objecty_old,mask,mask_old) = trackObj2(frame,contours,objectx_old,objecty_old,mask,mask_old,area_limit)
				
			if stop_flag == 1 and ct2 < 10:
				cv2.putText(frame,"Stop", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)			
				print "Stop"
				start_flag = 0
				#Increment frame counter
				ct1 = 0
				ct2 = ct2+1	
			elif stop_flag == 1 and ct2 >= 10:
				start_flag = 0
				stop_flag  = 0
				ct1 = 0
				ct2 = 0
				
				#Clear out all flags after being stopped for X amount of time
				start_flag = 0
				stop_flag  = 0
				ct1 = 0
				ct2 = 0
				
				print "Output mask created. \n"
				mask_output = mask_old
				#print mask_output
				objectx_old = []
				objecty_old = []
						
		else:
			print "Defects do not exist\n"
		#Show frame with magic applied
		cv2.imshow('frame',frame)
		
		#Check for break code
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		ret, frame = cap.read()
		
	cap.release()
	cv2.destroyAllWindows()

	
	
#Execute main function	
main()

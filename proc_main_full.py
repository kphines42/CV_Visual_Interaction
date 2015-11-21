import numpy as np
import argparse
import cv2
import os
import mahotas as mh
from skin2BW import skin2BW, personalSkin2BW
from findMinMaxSkin import findMinMaxSkin, findMinMaxHand
from blob import blob, blob2
from gesture import startGest, stopGest
import matplotlib.pyplot as plt
from build_filters import build_filters
from filt_hist import filt_hist
from coHi3 import coHi3
from fcent import fcent
from objdist import objdist
from prevmap import prevmap
from obj2mask import obj2mask
from addmask2frame import addmask2frame


def main():
	
	#Define flags for face detection and background detection
	face_flag = 0
	bg_flag = 1
	start_flag = 0
	stop_flag  = 0
	
	#Set arbitrary limits
	wait_limit = 500 # number of frames before ending action
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
	
	#Find face if flagged
	if face_flag == 1:
		minSkin,maxSkin = findMinMaxHand(frame)#findMinMaxSkin(frame)
		print minSkin
		print maxSkin
	
	#Initialize arrays, counters, masks, etc
	
	objectx_old = []
	objecty_old = []
	ct = 0
	sz = np.shape(frame)
	mask = np.zeros(shape=(sz[0],sz[1],3,20), dtype = np.uint8)
	mask_old = np.copy(mask)
	mask_out = np.copy(mask)
	tim = np.zeros(20)
	
	#Build filters
	n = 4
	filters = build_filters(n)
	
	#Loop through gestures to store histograms
	ct = 0
	ct1 = 0
	ct2 = 0
	ct3 = 0
	start_cnt = 0
	stop_cnt  = 0
	gest_dir = 'C:\Users\jonat_000\Desktop\ECE5554\project\opencvimplemet\masks'
	path, dirs, files = os.walk(gest_dir).next()
	m = len(files)
	gest = np.zeros([n,m])
	fnome = os.listdir(gest_dir)
	
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
		else:
			binary_frame = skin2BW(masked_frame)
		
		cv2.imshow('BW Frame',binary_frame)
		#Find blobs in binary image
		frame, contours, contoursOut, defects = blob2(binary_frame,frame,area_limit)
		img = np.copy(frame)
		#Show binary image
		#cv2.imshow('frame',binary_frame)
		
		#Check if a frame was found
		if not defects == []:
			#print "Defects Exist\n"
			#Check flags to see what text should be displayed...
			if start_flag == 0 and stop_flag == 0:
				print "Looking for start"
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
				if stop_flag == 1 and stop_cnt < 45:
					stop_cnt = stop_cnt+1
					stop_flag = 0
				else:
					stop_cnt = 0
			
		if start_flag == 1:
			#Find centroids
			objectx, objecty = fcent(contours, area_limit)
			#Calculate distance to each previous object
			objectloc, objectval = objdist(objectx, objecty, objectx_old, objecty_old)
			img = np.copy(frame)
			
			#Check if any objects were found to match previous frame objects
			if not objectloc == []:
				
				#Ensure only one object in current frame is mapped to previous frame object
				objectval2 = prevmap(objectloc, objectval)
				mask, mask_check, tim = obj2mask(objectloc, objectval2, objectx, objecty, objectx_old, objecty_old, mask_old, wait_limit, tim)
				#frame2, mask_all = addmask2frame(mask, frame)
				mask_old = np.copy(mask)
				img = np.copy(frame2)
			
			objectx_old = np.copy(objectx)
			objecty_old = np.copy(objecty)

		if stop_flag == 1:
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
				
			sim, pat = coHi3(m,fnome,gest_dir,mask_all,ct3,0)
			cv2.imshow('Drawn mask',mask_all)
			cv2.imshow('Nearest pattern',pat)
				
			ct3 = ct3+1
			mask_output = mask_old
			objectx_old = []
			objecty_old = []
			
			for i in range(0, 19):
				mask[:,:,:,i] = 0
				mask_old = np.copy(mask)

		ct = ct+1
		#Show frame with magic applied
		
		frame2, mask_all = addmask2frame(mask, frame)
		
		cv2.imshow('frame',frame2)
		cv2.imshow('mask',mask_all)


		#Check for break code
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if cv2.waitKey(1) & 0xFF == ord('s'):
			start_flag = 1
			stop_flag = 0
		if cv2.waitKey(1) & 0xFF == ord('z'):
			start_flag = 0
			stop_flag = 1

		ret, frame = cap.read()
		

		
		
	cap.release()
	cv2.destroyAllWindows()

	
	
	
main()

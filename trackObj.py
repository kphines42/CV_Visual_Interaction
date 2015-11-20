#trackObj.py
#
import numpy as np
import argparse
import cv2
import os
import mahotas as mh
from skin2BW import skin2BW, personalSkin2BW
from findMinMaxSkin import findMinMaxSkin, findMinMaxHand
from blob import blob2
import matplotlib.pyplot as plt

def unique(a):
    a = np.sort(a)
    b = np.diff(a)
    b = np.r_[1, b]
    return a[b != 0]


def trackObj(frame,contours,objectx_old,objecty_old,mask,mask_old,area_limit,tim):
	#sz = np.shape(frame)
	#mask = np.zeros(shape=(sz[0],sz[1],3,20), dtype = np.uint8)
	#tim = np.zeros(20)
	
	# Create some random colors
	color = np.random.randint(0,255,(100,3))
	
		#Set arbitrary limits
	wait_limit = 45 # number of frames before ending action
	
	#print "tracking..."
	
	objectx = []
	objecty = []
	objectloc = []
	objectval = []
	x = []
	y = []
	img = np.copy(frame)

	#Not spaced yet... Find contours around blobs
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
				
	#Check if any objects were found
	if not objectx_old == []:
					
		#Loop through each object in current frame and compute
		#distance to each object in previous frame
		for i, j in zip(objectx, objecty):
			x_dist = np.array(objectx_old)
			x_dist = x_dist - i
			y_dist = np.array(objecty_old)
			y_dist = y_dist - j
					
			y_dist = np.square(y_dist)
			x_dist = np.square(x_dist)
			
			dist = np.sqrt(x_dist+y_dist)
						
			if len(dist) > 0:
				minloc = np.argmin(dist)
				minval = dist[minloc]
				objectloc.append(minloc)
				objectval.append(minval)
				x.append(i)
				y.append(j)
				
	#Check if any objects were found to match previous frame objects
	if not objectloc == []:
		
		#Initialize parameters for loop over individual objects
		mx = np.amax(objectloc)
		mn = np.amin(objectloc)
					
		objs = unique(objectloc)
		vals = np.zeros_like(objs)+999
		locs = np.zeros_like(objs)-1
		co = len(objectloc)
		co2 = len(objs)

		#Ensure at most only 1 current object mapped to previous object
		for i in range(0, co2):
			for j in range(0, co):
				if objs[i] == objectloc[j]:
					if objectval[j] < vals[i]:
						vals[i] = objectval[j]
						locs[i] = j

		objectval2 = np.zeros_like(objectval)-1
		
		#Still matching current objects to previous ones.
		for i in range(0, co2):
			if locs[i] > -1:
				if locs[i] < co2:
					objectval2[locs[i]] = objectval[locs[i]]
					
		#Initialize mask parameters
		img = cv2.add(frame,mask[:,:,:,0])
		mask_check = np.zeros(20)
		frame2 = np.copy(frame)
		
		#Loop through each matched object and add to corresponding mask
		for i in range(0, co):
			if objectval2[i] > -1:
				hihi = 1
										
				a = np.copy(objectx_old[objectloc[i]])
				b = np.copy(objecty_old[objectloc[i]])
				c = np.copy(objectx[i])
				d = np.copy(objecty[i])
						
				dist = abs(((a-c)^2+(b-d)^2)^(1/2))
				mask_check[i] = 1
					
				if dist < 5:
					tim[i] = tim[i]+1
					if tim[i] > wait_limit:
						mask[:,:,:,i] = 0
						tim[i] = 0
						mask_check[i] = 0
				else:
					tim[i] = 0
				temp1 = np.copy(mask_old[:,:,:,objectloc[i]])
				if np.sum(mask[:,:,:,i]) > 0:
				#Connect the dots
					mask[:,:,:,i] = cv2.line(temp1, (a,b),(c,d), color[i].tolist(), 2)
				else:
				#Start point
					mask[:,:,:,i] = cv2.circle(temp1,(a,b),5,color[i].tolist(),-1)
				#Current point/End pointt
				frame2 = cv2.circle(frame2,(a,b),5,color[i].tolist(),-1)
				objectx_old[objectloc[i]] = np.copy(objectx[i])
				objecty_old[objectloc[i]] = np.copy(objecty[i])
					
		#Check if a mask disappeared
		for i in range(0, 19):
			if mask_check[i] == 0:
			#to add: if summing to nonzero, send as an output mask
				mask[:,:,:,i] = 0
			else:
				frame2 = cv2.add(frame2,mask[:,:,:,i])
		
		mask_old = np.copy(mask)
		img = np.copy(frame2)
					
	#I think this else is for the case where there weren't
	#any previous objects.
	else:
		for i in range(0, 19):
			mask[:,:,:,i] = 0
		mask_old = np.copy(mask)

	objectx_old = np.copy(objectx)
	objecty_old = np.copy(objecty)

	return img, objectx_old, objecty_old, mask,mask_old,tim

#Initialize variable which change with each frame
def trackObj2(frame,contours,objectx_old,objecty_old,mask,mask_old,area_limit):
	# Create some random colors
	color = np.random.randint(0,255,(100,3))
	
		#Set arbitrary limits
	wait_limit = 45 # number of frames before ending action

	
	objectx = []
	objecty = []
	objectloc = []
	objectval = []
	x = []
	y = []
	img = np.copy(frame)

	#Not spaced yet... Find contours around blobs
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
				
	#Check if any objects were found
	if not objectx_old == []:
					
		#Loop through each object in current frame and compute
		#distance to each object in previous frame
		for i, j in zip(objectx, objecty):
			x_dist = np.array(objectx_old)
			x_dist = x_dist - i
			y_dist = np.array(objecty_old)
			y_dist = y_dist - j
					
			y_dist = np.square(y_dist)
			x_dist = np.square(x_dist)
			
			dist = np.sqrt(x_dist+y_dist)
						
			if len(dist) > 0:
				minloc = np.argmin(dist)
				minval = dist[minloc]
				objectloc.append(minloc)
				objectval.append(minval)
				x.append(i)
				y.append(j)
				
	#Check if any objects were found to match previous frame objects
	if not objectloc == []:
		
		#Initialize parameters for loop over individual objects
		mx = np.amax(objectloc)
		mn = np.amin(objectloc)
					
		objs = unique(objectloc)
		vals = np.zeros_like(objs)+999
		locs = np.zeros_like(objs)-1
		co = len(objectloc)
		co2 = len(objs)

		#Ensure at most only 1 current object mapped to previous object
		for i in range(0, co2):
			for j in range(0, co):
				if objs[i] == objectloc[j]:
					if objectval[j] < vals[i]:
						vals[i] = objectval[j]
						locs[i] = j

		objectval2 = np.zeros_like(objectval)-1
		
		#Still matching current objects to previous ones.
		for i in range(0, co2):
			if locs[i] > -1:
				if locs[i] < co2:
					objectval2[locs[i]] = objectval[locs[i]]
					
		#Initialize mask parameters
		img = cv2.add(frame,mask[:,:,:,0])
		mask_check = np.zeros(20)
		frame2 = np.copy(frame)
		
		#Loop through each matched object and add to corresponding mask
		for i in range(0, co):
			if objectval2[i] > -1:
				
										
				a = np.copy(objectx_old[objectloc[i]])
				b = np.copy(objecty_old[objectloc[i]])
				c = np.copy(objectx[i])
				d = np.copy(objecty[i])
						
				dist = abs(((a-c)^2+(b-d)^2)^(1/2))
				mask_check[i] = 1
					
				#if dist < 5:
				#	tim[i] = tim[i]+1
				#	if tim[i] > wait_limit:
				#		mask[:,:,:,i] = 0
				#		tim[i] = 0
				#		mask_check[i] = 0
				#else:
				#	tim[i] = 0
				temp1 = np.copy(mask_old[:,:,:,objectloc[i]])
				if np.sum(mask[:,:,:,i]) > 0:
				#Connect the dots
					mask[:,:,:,i] = cv2.line(temp1, (a,b),(c,d), color[i].tolist(), 2)
				else:
				#Start point
					mask[:,:,:,i] = cv2.circle(temp1,(a,b),5,color[i].tolist(),-1)
				#Current point/End pointt
				frame2 = cv2.circle(frame2,(a,b),5,color[i].tolist(),-1)
				objectx_old[objectloc[i]] = np.copy(objectx[i])
				objecty_old[objectloc[i]] = np.copy(objecty[i])
					
		#Check if a mask disappeared
		for i in range(0, 19):
			if mask_check[i] == 0:
			#to add: if summing to nonzero, send as an output mask
				mask[:,:,:,i] = 0
			else:
				frame2 = cv2.add(frame2,mask[:,:,:,i])
		
		mask_old = np.copy(mask)
		img = np.copy(frame2)
					
	#I think this else is for the case where there weren't
	#any previous objects.
	else:
		for i in range(0, 19):
			mask[:,:,:,i] = 0
		mask_old = np.copy(mask)

	objectx_old = np.copy(objectx)
	objecty_old = np.copy(objecty)
	
	
	
	#return the original values
	return img, objectx_old, objecty_old, mask, mask_old
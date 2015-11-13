import numpy as np
import argparse
import cv2
import os
import mahotas as mh
from skin2BW import skin2BW, personalSkin2BW
from findMinMaxSkin import findMinMaxSkin, findMinMaxHand
from blob import blob

def unique(a):
    a = np.sort(a)
    b = np.diff(a)
    b = np.r_[1, b]
    return a[b != 0]

def main():
	


	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help = "path to the (optional) video file")
	args = vars(ap.parse_args())

	#About a 10 second delay with a threshold of 50 (intensity)
	fgbg = cv2.createBackgroundSubtractorMOG2(5000,50)
	
	# if no video, use webcam
	if not args.get("video", False):
		nome = 0
	else:
		nome = args["video"]
	
	cap = cv2.VideoCapture(nome)

	ret, frame = cap.read()

	objectx_old = []
	objecty_old = []
	
	#Unsuccessful attempt at interaction...
	#if nome is 0:
	#	ret, frame = cap.read()
	#	cv2.imshow("First Frame",frame)
	#	print "First frame to be sent to findMinMaxSkin()\n"
	#	print "Press any key to continue... \n"
	#	cv2.waitKey(0)
	#	
	#	retryInitial = raw_input("Would you like a new initial frame? Y/N \n")
	#	if retryInitial is "Y":
	#		print "Please adjust appropriately"
	#		ret,frame = cap.read()
	#		cv2.imshow("New initial frame", frame)

		#binary_frame = skin2BW(frame)
	#	minSkin,maxSkin = findMinMaxSkin(frame)
	#else:
	ret, frame = cap.read()
		#binary_frame = skin2BW(frame)
	minSkin,maxSkin = findMinMaxHand(frame)#findMinMaxSkin(frame)
	
	print minSkin
	print maxSkin
	
	# Create some random colors
	color = np.random.randint(0,255,(100,3))
	
	sz = np.shape(frame)
	mask = np.zeros(shape=(sz[0],sz[1],3,20), dtype = np.uint8)
	#print np.shape(mask)
	#mask = np.zeros_like(frame)
	mask_old = np.copy(mask)
	
	while(cap.isOpened()):
		
		fgmask = fgbg.apply(frame)
		masked_frame = cv2.bitwise_and(frame,frame,mask = fgmask)
		#binary_frame = skin2BW(masked_frame)#personalSkin2BW(frame,minSkin,maxSkin)#skin2BW(frame)
		binary_frame = skin2BW(frame)
		
		
		frame, contours = blob(binary_frame,frame)
		cv2.imshow('frame',binary_frame)
		
		
		if not ret == False:
		
			objectx = []
			objecty = []
		
			for i, c in enumerate(contours):
				area = cv2.contourArea(c)

				if area > 500:
			
					cent = cv2.moments(c)
					temp = cent['m00']
					if not temp == 0:
						cx = int(cent['m10']/cent['m00'])
						cy = int(cent['m01']/cent['m00'])
						#cv2.circle(frame,(cx,cy),5,(0,0,255),-2)
						objectx.append(cx)
						objecty.append(cy)
			
			objectloc = []
			objectval = []
			x = []
			y = []
			
			img = np.copy(frame)
			if not objectx_old == []:
				
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
					#print dist
			if not objectloc == []:
				mx = np.amax(objectloc)
				mn = np.amin(objectloc)
				
				objs = unique(objectloc)
				vals = np.zeros_like(objs)+999
				locs = np.zeros_like(objs)-1
				co = len(objectloc)
				co2 = len(objs)
				
				#print "objectloc =", objectloc, "objectval =", objectval
				
				for i in range(0, co2):
					for j in range(0, co):
						#print "objs = ", objs[i], "objectloc = ", objs[j], "objectval = ", objectval[j], "vals = ", vals
						if objs[i] == objectloc[j]:
							if objectval[j] < vals[i]:
								vals[i] = objectval[j]
								locs[i] = objectloc[j]				
							#print "vals =", vals
				objectval2 = np.zeros_like(objectval)-1
				#print "locs =", locs, "objectval2 =", objectval2, "co2 = ", co2
				
				#os.system("pause")
				
				for i in range(0, co2):
					if locs[i] > -1:
						if locs[i] < co2:
							objectval2[locs[i]] = objectval[locs[i]]
				
				img = cv2.add(frame,mask[:,:,:,0])
				mask_check = np.zeros(20)
				frame2 = np.copy(frame)
				for i in range(0, co-1):
					if objectval2[i] > -1:
						hihi = 1
						#cv2.circle(frame,(x[i],y[i]),5,(0,0,255),-2)
						c = objectx[i]
						d = objecty[i]
						a = objectx_old[objectloc[i]]
						b = objecty_old[objectloc[i]]
						#mask[:,:,3*i:3*i+2] = cv2.line(mask_old[:,:,3*objectloc[i]:3*objectloc[i]+2], (a,b),(c,d), color[i].tolist(), 2)
						#print i, np.shape(mask[:,:,:,i]), np.shape(mask_old[:,:,:,objectloc[i]])
						temp1 = np.copy(mask_old[:,:,:,objectloc[i]])
						#temp = cv2.line(mask_old[:,:,:,objectloc[i]], (a,b),(c,d), color[i].tolist(), 2)
						mask[:,:,:,i] = cv2.line(temp1, (a,b),(c,d), color[i].tolist(), 2)
						#print np.shape(temp)
						#mask = cv2.line(mask_old, (a,b),(c,d), color[i].tolist(), 2)
						frame2 = cv2.circle(frame2,(a,b),5,color[i].tolist(),-1)
						mask_check[i] = 1
					#if mask_old.all() == mask.all():
						#mask = np.zeros_like(frame)
						#mask_old = np.copy(mask)
					#print np.shape(mask[:,:,:,i]), np.shape(img), np.shape(frame2)	
					#print np.shape(mask), np.shape(img)
					#img[:,:,:] = cv2.add(np.array(frame2[:,:,:], dtype=np.uint8),np.array(mask[:,:,:,i], dtype=np.uint8))
					#mask2 = np.copy(mask[:,:,:,i])
					#mask3 = np.copy(mask2[:,:,:])
					#print np.shape(mask3), np.shape(img), np.shape(frame2)
					#img = cv2.add(frame2,mask3)
					frame2 = cv2.add(frame2,mask[:,:,:,i])
					
					
					#cv2.imshow('frame',img)
				for i in range(0, 19):
					if mask_check[i] == 0:
						mask[:,:,:,i] = 0
				
				mask_old = np.copy(mask)
				img = np.copy(frame2)
			objectx_old = objectx
			objecty_old = objecty
			

		else:
			break
		
		#print objectloc, objectval
		cv2.imshow('frame',img)#frame)
		#os.system("pause")
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		ret, frame = cap.read()
		
	cap.release()
	cv2.destroyAllWindows()

	
	
	
main()

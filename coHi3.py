import numpy as np
import cv2
import os
from skimage.measure import structural_similarity as ssim
from PIL import Image, ImageChops

def coHi3(m,fnome,gest_dir,mask,ct2,fl):
	#s = np.zeros(m)
	min_val = np.zeros(m)
	max_val = np.zeros(m)
	min_loc = np.zeros([m,2])
	max_loc = np.zeros([m,2])
	
	dist = np.zeros(m)
	
	for i in range(0,m):
		sum_vec = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
		trim_vec = autocrop(sum_vec,0)
		
		ge = cv2.imread(os.path.join(gest_dir, fnome[i]),0)
		trim_ge = autocrop(ge,0)
		height, width = trim_ge.shape[:2]
		
		scale_vec = cv2.resize(trim_vec,(width,height), interpolation = cv2.INTER_LINEAR)
		se = np.zeros([height*4, width*4])
		se[0:height,0:width] = np.copy(scale_vec)
		#cv2.imshow('mask',scale_vec.astype(np.uint8))
		#cv2.imshow('gest',ge.astype(np.uint8))
		#cv2.waitKey(0)
		#se = cv2.resize(sum_vec,(width*4, height*4), interpolation = cv2.INTER_LINEAR)
		s = cv2.matchTemplate(se.astype(np.uint8),trim_ge.astype(np.uint8),0)
		#cv2.imshow('mask',se
		#min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(s)
		#min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(s)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(s)
		
		#print np.shape(min_val), np.shape(max_val), np.shape(min_loc), np.shape(max_loc)
		x_dist = (min_loc[0]-max_loc[0])
		y_dist = (min_loc[1]-max_loc[1])
		dist[i] = np.sqrt(x_dist*x_dist+y_dist*y_dist)
		#print x_dist, y_dist, dist[i]#(min_loc[0] - max_loc[0])*(min_loc[0] - max_loc[0]), (min_loc[1] - max_loc[1])*(min_loc[1] - max_loc[1])
		#dist[i] = ((min_loc[0]-max_loc[0])^2+(min_loc[1]-max_loc[1])^2)#^(1/2)
		#dist[i] = np.copy(np.sqrt(np.square(min_loc)+np.square(max_loc)))
		w, h = trim_ge.shape[::-1]
		#top_left = max_loc[i,:]
		top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		#print np.shape(se), np.shape(top_left), np.shape(bottom_right)
		cv2.rectangle(se,top_left, bottom_right, 255, 2)
		
		#cv2.imshow('res',se)
		
		
		
		#print min_val, max_val, min_loc, max_loc
		#cv2.waitKey(0)
		#os.system("pause")
		#s[i] = ssim(se, ge)
	
	#print "s = ", s
	print np.amin(dist)
	
	#dist = np.sqrt(np.square(min_loc)+np.square(max_loc))
	
	c = np.argmin(dist)
	
	#print c
	#os.system("pause")
	
	ge = cv2.imread(os.path.join(gest_dir, fnome[c]),0)
	
	if fl == 1:
		cv2.imwrite(os.path.join(gest_dir,"gest-"+str(ct2)+".jpg"),sum_vec)
	return s, ge
	
import numpy as np

def autocrop(image, threshold=0):
	flatImage = image
	assert len(flatImage.shape) == 2
	rows = np.where(np.max(flatImage, 0) > threshold)[0]
	if rows.size:
		cols = np.where(np.max(flatImage, 1) > threshold)[0]
		image = image[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
	else:
		image = image[:1, :1]
	return image

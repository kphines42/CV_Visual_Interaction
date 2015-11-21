import cv2
import numpy as np

def objdist(objectx, objecty, objectx_old, objecty_old):
	objectloc = []
	objectval = []
	#Check if any objects were found
	if not objectx_old == []:
				
		#Loop through each object in current frame and compute distance
		#to each object in previous frame
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
	return objectloc, objectval

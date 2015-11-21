import cv2
import numpy as np

def obj2mask(objectloc, objectval2, objectx, objecty, objectx_old, objecty_old, mask_old, wait_limit, tim):
	mask_check = np.zeros(20)
	mask = np.copy(mask_old)
	#Loop through each matched object and add to corresponding mask
	for i in range(0, len(objectloc)):
		if objectval2[i] > -1:
			
			a = np.copy(objectx_old[objectloc[i]])
			b = np.copy(objecty_old[objectloc[i]])
			c = np.copy(objectx[i])
			d = np.copy(objecty[i])
						
			dist = abs(((a-c)^2+(b-d)^2)^(1/2))
			mask_check[i] = 1
						
			#if dist < 5:
			#	tim[i] = tim[i]+1
			#if tim[i] > wait_limit:
				#mask[:,:,:,i] = 0
			#	tim[i] = 0
			#	mask_check[i] = 0
			#else:
			#	tim[i] = 0
			temp1 = np.copy(mask_old[:,:,:,i])
			if np.sum(mask[:,:,:,i]) > 0:
				#Connect the dots
				mask[:,:,:,i] = cv2.line(temp1, (a,b),(c,d), [255,0,255], 2)
			else:
				#Start point
				mask[:,:,:,i] = cv2.circle(temp1,(c,d),5,[255,0,255],-1)
			#Current point/End point
			#frame2 = cv2.circle(frame2,(c,d),5,color[i].tolist(),-1)
			objectx_old[objectloc[i]] = np.copy(objectx[i])
			objecty_old[objectloc[i]] = np.copy(objecty[i])
	
	return mask, mask_check, tim
	

import cv2
import numpy as np
from coHi3 import coHi3

def addmask2frame(mask, frame):
	frame2 = np.copy(frame)
	mask_all = np.zeros_like(mask[:,:,:,0])
	for i in range(0, 19):
		frame2 = cv2.add(frame2,mask[:,:,:,i])
		mask_all = cv2.add(mask_all,mask[:,:,:,i])
	return frame2, mask_all
	

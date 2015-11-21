import cv2
import numpy as np

def prevmap(objectloc, objectval):
				
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
				
	for i in range(0, co2):
		if locs[i] > -1:
			if locs[i] < co2:
				objectval2[locs[i]] = objectval[locs[i]]
	return objectval2
	
def unique(a):
    a = np.sort(a)
    b = np.diff(a)
    b = np.r_[1, b]
    return a[b != 0]

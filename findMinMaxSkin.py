#function (minSkin,maxSkin) = findMinMaxSkin(frame)
#
#Bring in libraries
import mahotas as mh
import numpy as np
import cv2
from skin2BW import skin2BW

#Function to be sent elsewhere...
#Finds the minimum and the maximum skin values found
#	on the person (YCrCb)
def findMinMaxSkin(inImage):
	binaryIm = skin2BW(inImage)
	
	minSkin = np.zeros((1,3,))
	maxSkin = np.zeros((1,3,))
	
	#Prepare to split the image...
	imageIn = inImage
	imageYCrCb = cv2.cvtColor(imageIn,cv2.COLOR_BGR2YCR_CB) #Cr and Cb are switched

	imageY   = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	maskY 	 = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1],))
	#maskY[:] = np.NAN
	imageCr  = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	maskCr   = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1],))
	imageCb  = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	maskCb   = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1],))
	imageBW  = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)

	#Split the channels
	imageY  = cv2.split(imageYCrCb)[0]
	imageCr = cv2.split(imageYCrCb)[1]
	imageCb = cv2.split(imageYCrCb)[2]
	
	#Create a mask using the binary image
	maskIm = binaryIm*1
	idx   = (maskIm != 0)
	
	maskY[idx] = imageY[idx]
	minSkin[0][0] = np.min(maskY[np.nonzero(maskY)])
	maxSkin[0][0] = np.max(maskY[np.nonzero(maskY)])
	
	maskCr[idx] = imageCr[idx]
	minSkin[0][1]  = np.nanmin(maskCr[np.nonzero(maskCr)])
	maxSkin[0][1]  = np.nanmax(maskCr[np.nonzero(maskCr)])
	
	maskCb[idx] = imageCb[idx]
	minSkin[0][2]  = np.nanmin(maskCb[np.nonzero(maskCb)])
	maxSkin[0][2]  = np.nanmax(maskCb[np.nonzero(maskCb)])
	
	#Output Structure:
	#minSkin = [minY minCr minCb]
	#maxSkin = [maxY maxCr maxCb]
	return minSkin, maxSkin
	
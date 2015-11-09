#function skin2BW.py -f frame
#Bring in libraries
import mahotas as mh
import numpy as np
import cv2

#Function to be sent elsewhere...
#Performs binarization of skin
def skin2BW(frame):
	imageIn = frame
	imageYCrCb = cv2.cvtColor(imageIn,cv2.COLOR_BGR2YCR_CB) #Cr and Cb are switched

	imageY  = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	imageCr = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	imageCb = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)
	imageBW = np.zeros((imageYCrCb.shape[0],imageYCrCb.shape[1]), dtype = imageYCrCb.dtype)

	#Split the channels
	imageY  = cv2.split(imageYCrCb)[0]
	imageCr = cv2.split(imageYCrCb)[1]
	imageCb = cv2.split(imageYCrCb)[2]

	#Filter based on luminescence and chromatic channels
	imageY_S = imageY > 80

	imageCr_S1 = imageCr > 135	
	imageCr_S2 = imageCr < 180
	imageCr_S = imageCr_S1 & imageCr_S2

	imageCb_S1 = imageCb > 85
	imageCb_S2 = imageCb < 135
	imageCb_S = imageCb_S1 & imageCb_S2

	#Boolean matrix of the skin possibilities
	imageBWTemp = imageY_S & imageCr_S
	imageBW = imageBWTemp & imageCb_S
	imageBW = mh.morph.close(imageBW)
	
	#Return BW image
	return imageBW
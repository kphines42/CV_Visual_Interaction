#functions:
#  imageBW = skin2BW(frame)
#  imageBW = personalSkin2BW(frame,minSkin,maxSkin)
#			 min/maxSkin format: [Y Cr Cb]

#Bring in libraries
import mahotas as mh
import numpy as np
import cv2

#Functions to be sent elsewhere...
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
	
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)

	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)

	imageBW = mh.morph.close(imageBW)
	
	#Convert imageBW to uint8
	imageBW = imageBW.astype(int)*255
	imageBW = imageBW.astype(np.uint8)
	
	
	
	#Return BW image
	return imageBW
	
#Performs personal binarization of skin
def personalSkin2BW(frame,minSkin,maxSkin):
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
	imageY_S1 = imageY > minSkin[0][0]
	imageY_S2 = imageY < maxSkin[0][0]
	imageY_S = imageY_S1 & imageY_S2

	imageCr_S1 = imageCr > minSkin[0][1]
	imageCr_S2 = imageCr < maxSkin[0][1]
	imageCr_S = imageCr_S1 & imageCr_S2

	imageCb_S1 = imageCb > minSkin[0][2]
	imageCb_S2 = imageCb < maxSkin[0][2]
	imageCb_S = imageCb_S1 & imageCb_S2

	#Boolean matrix of the skin possibilities
	imageBWTemp = imageY_S & imageCr_S
	imageBW = imageBWTemp & imageCb_S
	
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	imageBW = mh.morph.erode(imageBW)
	
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)
	imageBW = mh.morph.dilate(imageBW)



	#imageBW = mh.morph.close(imageBW)
	
	
	
	#Convert imageBW to uint8
	imageBW = imageBW.astype(int)*255
	imageBW = imageBW.astype(np.uint8)
	
	#Return BW image
	return imageBW

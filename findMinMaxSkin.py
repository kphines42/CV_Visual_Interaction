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
	testMinY = np.min(maskY[np.nonzero(maskY)])
	if testMinY > 80:
		minSkin[0][0] = testMinY
	else:
		minSkin[0][0] = 80
	testMaxY = np.max(maskY[np.nonzero(maskY)])
	if testMaxY < 255:
		maxSkin[0][0] = testMaxY
	else:
		maxSkin[0][0] = 255
	
	maskCr[idx] = imageCr[idx]
	testMinCr = np.nanmin(maskCr[np.nonzero(maskCr)])
	if testMinCr > 135:
		minSkin[0][1]  = testMinCr
	else:
		minSkin[0][1] = 135
	testMaxCr = np.nanmax(maskCr[np.nonzero(maskCr)])
	if testMaxCr < 180:
		maxSkin[0][1]  = testMaxCr
	else:
		maxSkin[0][1] = 180
	
	maskCb[idx] = imageCb[idx]
	testMinCb = np.nanmin(maskCb[np.nonzero(maskCb)])
	if testMinCb > 85:
		minSkin[0][2]  = testMinCb
	else:
		minSkin[0][2] = 85
	testMaxCb = np.nanmax(maskCb[np.nonzero(maskCb)])
	if testMaxCb < 135:
		maxSkin[0][2]  = testMaxCb
	else:
		maxSkin[0][2] = 135
		
	#Output Structure:
	#minSkin = [minY minCr minCb]
	#maxSkin = [maxY maxCr maxCb]
	return minSkin, maxSkin
	
#Finds the minimum and the maximum skin values found
#	on the person (YCrCb) while ignoring the facial colors
def findMinMaxHand(inImage):
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	gray = cv2.cvtColor(inImage,cv2.COLOR_BGR2GRAY)
	
	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),#flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)
	
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.imshow("Faces found", gray)
	cv2.waitKey(0)
	
	binaryIm = skin2BW(inImage)
	
	#Create mask and apply it...
	maskImage = np.ones((inImage.shape[0],inImage.shape[1]), dtype = inImage.dtype)
	
	r = np.max((w,h))/2
	#print r
	#print x+w/2
	#print y+h/2
	for (x, y, w, h) in faces:
		#cv2.circle(maskImage, (x+w/2, y+h/2), (r), (0), -1)
		cv2.rectangle(maskImage, (x, y), (x+w, y+h), (0), -1)

	cv2.imshow("Mask",maskImage*255)
	cv2.waitKey(0)
	
	minSkin = np.zeros((1,3,))
	maxSkin = np.zeros((1,3,))
	
	#Prepare to split the image...
	imageIn = cv2.bitwise_and(inImage,inImage, mask = maskImage)
	cv2.imshow("Mask",imageIn)
	cv2.waitKey(0)
	
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
	testMinY = np.min(maskY[np.nonzero(maskY)])
	if testMinY > 80:
		minSkin[0][0] = testMinY
	else:
		minSkin[0][0] = 80
	testMaxY = np.max(maskY[np.nonzero(maskY)])
	if testMaxY < 255:
		maxSkin[0][0] = testMaxY
	else:
		maxSkin[0][0] = 255
	
	maskCr[idx] = imageCr[idx]
	testMinCr = np.nanmin(maskCr[np.nonzero(maskCr)])
	if testMinCr > 135:
		minSkin[0][1]  = testMinCr
	else:
		minSkin[0][1] = 135
	testMaxCr = np.nanmax(maskCr[np.nonzero(maskCr)])
	if testMaxCr < 180:
		maxSkin[0][1]  = testMaxCr
	else:
		maxSkin[0][1] = 180
	
	maskCb[idx] = imageCb[idx]
	testMinCb = np.nanmin(maskCb[np.nonzero(maskCb)])
	if testMinCb > 85:
		minSkin[0][2]  = testMinCb
	else:
		minSkin[0][2] = 85
	testMaxCb = np.nanmax(maskCb[np.nonzero(maskCb)])
	if testMaxCb < 135:
		maxSkin[0][2]  = testMaxCb
	else:
		maxSkin[0][2] = 135
		
	#Output Structure:
	#minSkin = [minY minCr minCb]
	#maxSkin = [maxY maxCr maxCb]
	return minSkin, maxSkin
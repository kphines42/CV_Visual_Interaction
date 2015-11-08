# Syntax: python skin2Binary.py
# For stationary images...

#Import the appropriate libraries
import numpy as np
import cv2
import pylab
import mahotas as mh
from PIL import Image

#Read in the image...
imageIn = cv2.imread('testImage.jpg') #BGR, not RGB
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

#For debugging purposes
#pylab.imshow(imageBW)
#pylab.gray()
#pylab.show()

imageBWFilt = mh.gaussian_filter(imageBW,8)
imageBWFilt = np.round(imageBWFilt*255)
imageBWFiltInt = imageBWFilt.astype(np.uint8)
#imageBWFiltInt = imageBWFiltInt*255
T = mh.thresholding.otsu(imageBWFiltInt)
imageBWThresh = imageBWFiltInt > T

#For debugging purposes
pylab.imshow(imageBWThresh)
pylab.gray()
pylab.show()
# USAGE python skin2BW_Video.py -v "testVideo.wmv"

# import the necessary packages
import numpy as np
import pylab
import mahotas as mh
import argparse
import cv2

#Parse the inputs...
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

# if no video, use webcam
if not args.get("video", False):
	nome = 0
else:
	nome = args["video"]

cap = cv2.VideoCapture(nome)
capSave = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
	
if cap.isOpened():
	print("Success!\n")
else:
	print("Failure!\n")

#Grab first frame to make certain everything is loaded...
(grabbed, frame) = cap.read()
if not grabbed:
	print("Error loading video!\n")

imageY  = np.zeros((frame.shape[0],frame.shape[1]), dtype = frame.dtype)
imageCr = np.zeros((frame.shape[0],frame.shape[1]), dtype = frame.dtype)
imageCb = np.zeros((frame.shape[0],frame.shape[1]), dtype = frame.dtype)
imageBW = np.zeros((frame.shape[0],frame.shape[1]), dtype = frame.dtype)


# keep looping
while cap.isOpened():
	imageYCrCb = cv2.cvtColor(frame,cv2.COLOR_BGR2YCR_CB) #Cr and Cb are switched

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
	imageBW = imageBW.astype(int)*255
	imageBW = imageBW.astype(np.uint8)
	
	#Smooth image and then threshold again
	#imageBWFilt = mh.gaussian_filter(imageBW,8)
	#imageBWFilt = np.round(imageBWFilt*255)
	#imageBWFiltInt = imageBWFilt.astype(np.uint8)
	#T = mh.thresholding.otsu(imageBWFiltInt)
	#imageBWThresh = imageBWFiltInt > T
	#imageBWThresh = imageBWThresh.astype(int)*255
	#imageBWThresh = imageBWThresh.astype(np.uint8)
		
	#imageBW_E = mh.morph.open(imageBW)#mh.morph.erode(imageBW)
	imageBW_ED = mh.morph.close(imageBW)#mh.morph.dilate(imageBW_E)
	
	
	# show our detected skin
	#imageOut = imageBW
	#imageOut = imageBWThresh
	imageOut = imageBW_ED
	cv2.imshow("Test",imageOut)
	
	#Save the frame to video
	capSave.write(imageOut)
	
	# grab the next frame
	(grabbed, frame) = cap.read()

	# check to see if we have reached the end of the
	# video
	if not grabbed:
		#print("Error loading video!\n")
		break

	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
	
# cleanup the camera and close any open windows
cap.release()
capSave.release()
cv2.destroyAllWindows()
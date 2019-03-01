#import necessary libraries
from pathlib import Path
import sys
import os
import numpy as np
import cv2
import imutils

#save user input path and create save directory
data_path = str(sys.argv[1])
save_path = './detect'
if not os.path.exists(save_path):
	os.makedirs(save_path)

#for each image in the desired path
pathlist = Path(data_path).glob('**/*.jpg')
for path in pathlist:

	#load image and convert to grayscale
	image = cv2.imread(str(path))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#convert image to binary and invert (for contours)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.bitwise_not(thresh)

	#calculate contours
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	N = len(cnts)

	#if no proper contours calculated
	if not N:
		cv2.putText(image, "COULD NOT DETECT", (int(image.shape[1]/2),int(image.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		save_file = save_path + str(path)[len(data_path.strip('./')):]
		cv2.imwrite(save_file,image)

	#else, contour "algorithm" to detect phone
	else:
		cnts_values = np.ones(N)*np.maximum(image.shape[0],image.shape[1])
		for i in range(N):
		    param = cv2.arcLength(cnts[i],True)/4
		    area = np.sqrt(cv2.contourArea(cnts[i]))
		    if (param>10) and (area>10):
		        cnts_values[i] = np.absolute(param-area)/np.minimum(param,area)
		phone = np.argmin(cnts_values)

		#calculate center
		M = cv2.moments(cnts[phone])
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		#draw contour and center on image
		cv2.drawContours(image, [cnts[phone]], -1, (0, 255, 0), 2)
		cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

		#save image to save directory
		save_file = save_path + str(path)[len(data_path.strip('./')):]
		cv2.imwrite(save_file,image)
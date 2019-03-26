#!/usr/bin/python
import twittercred
import os
import time
from TwitterAPI import TwitterAPI
import cv2
import numpy as np


#getting the authentication keys from twitter_credentials
CONSUMER_KEY = twittercred.CONSUMER_KEY
CONSUMER_SECRET = twittercred.CONSUMER_SECRET
ACCESS_TOKEN_KEY = twittercred.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET = twittercred.ACCESS_TOKEN_SECRET

#gets the authentication keys in order to post the photo
api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

#0 is used if there is only one camera connected 
camera = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()


while(True):
		
	if camera.isOpened():
		ret, frame= camera.read()
	else:
		ret = False
		break
	#converts to grey scale
	fgmask = fgbg.apply(frame)
	fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

	#Displaying the frame
	cv2.imshow('temp', frame)
	cv2.imshow('sd', fgmask)

	#takes the photo at q 
	#exits while-loop when the waitkey value is either q or Q
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.imwrite('./random.png', frame)
		break
	difference = cv2.absdiff(frame, fgmask)
	result = np.any(difference)

	while(result):
		cv2.imwrite('./random.png', frame)
		file = open('random.png', 'rb')
		data = file.read()
		#this gets the time and date to post with the picture
		localtime = time.asctime(time.localtime(time.time()))

		#posting the actual photo
		r = api.request('statuses/update_with_media', {'status': localtime}, {'media[]':data})
		time.sleep(.7)


#this releases the capture
camera.release()
cv2.destroyAllWindows



#only runs is the status code is successful / 200
if r.status_code == 200:
	print('SUCCESS')
	os.system('cp random.png random2.png')
	os.remove("random.png")
	os.system('mv random2.png random.png')

#TODO once i get opencv to work and the motion detector, will no longer need to make a copy and rename the file 
#		will only need the remove at that point

#TODO will also need to create a while loop to make sure that this is constantly running

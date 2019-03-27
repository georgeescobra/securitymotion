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
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(500, 16, True)


#checks if the camera was opened or not	
while(camera.isOpened()):
		
	ret, frame = camera.read()

	while ret:
		cv2.imshow('original', frame)
		key = cv2.waitKey(0)

		#converts to grey scale
		fgmask = fgbg.apply(frame)

		#Displaying the frame
		#cv2.imwrite('./media.png', fgmask)

		#takes the photo at q 
		#exits while-loop when the waitkey value is either q or Q
		thresh = cv2.countNonZero(fgmask)
		

		if(thresh > 30):
			cv2.imwrite('./random.png', frame)
			file = open('random.png', 'rb')
			data = file.read()
			#this gets the time and date to post with the picture
			localtime = time.asctime(time.localtime(time.time()))

			#posting the actual photo
			r = api.request('statuses/update_with_media', {'status': localtime}, {'media[]':data})
			time.sleep(.2)

		if (key == ord('q')):
			cv2.imwrite('./random.png', frame)
			file = open('random.png', 'rb')
			data = file.read()
			localtime = time.asctime(time.localtime(time.time()))
			r = api.request('statuses/update_with_media', {'status': localtime}, {'media[]':data})
			break
		# difference = cv2.absdiff(frame, fgmask)
		# result = np.any(difference)


#this releases the capture
camera.release()
cv2.destroyAllWindows()


#only runs is the status code is successful / 200
if r.status_code == 200:
	print('SUCCESS')
	os.system('cp random.png random2.png')
	os.remove("random.png")
	os.system('mv random2.png random.png')

#TODO once i get opencv to work and the motion detector, will no longer need to make a copy and rename the file 
#		will only need the remove at that point

#TODO will also need to create a while loop to make sure that this is constantly running

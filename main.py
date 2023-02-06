'''
References from which I copied the code :)
https://www.section.io/engineering-education/creating-a-hand-tracking-module/
https://google.github.io/mediapipe/solutions/hands

appart from that a special thanks to Chat GPT.

See the Arduino code side by side for better understanding.
'''

import cv2
import mediapipe as mp
import serial
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ser = serial.Serial('/dev/ttyACM0', 115200) # set serial port and baud rate

try:
	while True:
		success, image = cap.read()
		img = np.zeros((480, 640, 3), dtype = np.uint8) # Black output screen
		# if want to see the actual video output change `img` to `image' @ the following
		# places #1, #2, #3

		imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = hands.process(imageRGB)

		if results.multi_hand_landmarks:
			for handLms in results.multi_hand_landmarks:
				for id, lm in enumerate(handLms.landmark):
					h, w, c = image.shape
					cx, cy = int(lm.x * w), int(lm.y *h)
					if id == 9: # This point will be located at the center of your hand
						cv2.circle(img, (cx, cy), 10, (0, 255, 120), cv2.FILLED) #1
						print("Tracking point:", cx, end=" ")
						deg = int(0.287*cx - 1.87) # converting the x-axis values to respective angle
						print("Angle:",deg)
						if deg > 0: # to neglect -ve angle after convertion
							ser.write(bytes(str(deg)+'\0', 'utf-8')) # sending bytes, end with a non-numarical value
				mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #2

		cv2.imshow("Output", img) #3
		cv2.waitKey(1)

except KeyboardInterrupt:
	cv2.destroyAllWindows()
	exit(0)

import cv2
import mediapipe as mp
import serial
import numpy as np
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ser = serial.Serial('/dev/ttyACM0', 115200)

try:
	while True:
		success, image = cap.read()
		img = np.zeros((480, 640, 3), dtype = np.uint8)
		imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = hands.process(imageRGB)

		if results.multi_hand_landmarks:
			for handLms in results.multi_hand_landmarks:
				for id, lm in enumerate(handLms.landmark):
					h, w, c = image.shape
					cx, cy = int(lm.x * w), int(lm.y *h)
					if id == 9:
						cv2.circle(img, (cx, cy), 10, (0, 255, 120), cv2.FILLED)
						print(cx, end=" ")
						deg = int(0.287*cx - 1.87)
						print(deg)
						if deg > 0:
							ser.write(bytes(str(deg)+'\0', 'utf-8'))
				mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

		cv2.imshow("Output", img)
		cv2.waitKey(1)
except KeyboardInterrupt:
	exit(0)

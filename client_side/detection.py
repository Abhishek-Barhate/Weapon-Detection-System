from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import time

# Handles the opencv detection algorithm, saves detected frames and sends alert to the server-side application
class Detection(QThread):

	def __init__(self):
		super(Detection, self).__init__()	
	
	changePixmap = pyqtSignal(QImage)

	# Runs the detection model, evaluates detections and draws boxes around detected objects
	def run(self):
	
		font = cv2.FONT_HERSHEY_PLAIN
		starting_time = time.time()

		self.running = True
		gun_cascade=cv2.CascadeClassifier('guns1.xml')
		# Starts camera
		cap = cv2.VideoCapture(0)
		
		# Detection while loop
		while self.running:
			ret, frame = cap.read()
			if ret:
				height, width, channels = frame.shape
				gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
				gun = gun_cascade.detectMultiScale(gray,1.3,3)
				for(x,y,w,h) in gun:
					rect = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
					cv2.putText(rect, 'Gun', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
					roi_gray=gray[y:y+h,x:x+w]
					roi_color=frame[y:y+h,x:x+w]	
					elapsed_time = time.time() - starting_time

					#Save detected frame every 10 seconds
					if elapsed_time >= 10:
						starting_time = time.time()
						self.save_detection(frame)

				# Showing final result
				rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				bytesPerLine = channels * width
				convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
				p = convertToQtFormat.scaled(854, 640, Qt.KeepAspectRatio)
				self.changePixmap.emit(p)

	# Saves detected frame as a .jpg within the saved_alert folder
	def save_detection(self, frame):
		cv2.imwrite("saved_frame/frame.jpg", frame)
		print('Frame Saved')
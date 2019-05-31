#!/usr/bin/env python
# Import necessary packages
import cv2 
import numpy as np
import rospy
import cv_bridge

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class obj_follower:
	
	def __init__(self):
    		self.bridge = cv_bridge.CvBridge()
    		cv2.namedWindow("window", 1)
    		self.image_sub = rospy.Subscriber('/usb_cam_right/image_raw',Image, self.image_callback)
    		self.cmd_vel_pub = rospy.Publisher('/rawTwist',Twist, queue_size=1)
    		self.twist = Twist()

	def image_callback(self, msg):
		frame = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    		# Convert BGR to HSV
    		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    		# define range of yellow color in HSV
    		lower_yellow = np.array([20,100,100])
    		upper_yellow = np.array([30,255,255])
    		# Threshold the HSV image to get only yellow colors
    		mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    		# Bitwise-AND mask and original image
    		res = cv2.bitwise_and(frame,frame, mask= mask)
    		# Find Contours
    		image, contours, _ = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    		# if object detected find maximum countour
    		if len(contours) > 0 :
        		c = max(contours, key=cv2.contourArea)
        	# Draw bounding rectangle
        	x,y,w,h = cv2.boundingRect(c)
        	cv2.rectangle(res, (x,y), (x+w, y+h), (0,255,0),3)
    		# Display Result
    		cv2.imshow('frame',frame)
    		cv2.imshow('mask',mask)
    		cv2.imshow('res',res)
		h1, w1, d = frame.shape
    		size = (h1*w1)/(w*h)
    		"""
		print(size)
    		# Break on pressing 'q'
    		key = cv2.waitKey(1) & 0xFF
    		if key == ord("q"):
            	break

		# release camera and close all windows
		cap.release()
		cv2.destroyAllWindows()
		"""
		cx = x + w/2
		cy = y + h/2
		err = cx - w1/2
		if(err != 0):
        		errorSign = -err/abs(err)
			if (size > 15 && size < 21):
				self.twist.linear.x = 0.0
          			self.twist.angular.z = float(abs(err))*errorSign / 30
			if (size > 21 && size < 200):
				self.twist.linear.x = 0.9
          			self.twist.angular.z = float(abs(err))*errorSign / 30
			if (size > 200 && size < 1000):
				self.twist.linear.x = 1.5
          			self.twist.angular.z = float(abs(err))*errorSign / 30
			if (size > 1000):
				self.twist.linear.x = 2.0
          			self.twist.angular.z = float(abs(err))*errorSign / 30
			else
				self.twist.linear.x = -0.5

	self.cmd_vel_pub.publish(self.twist)
    	

rospy.init_node('follower')
follower = obj_follower()
rospy.spin()














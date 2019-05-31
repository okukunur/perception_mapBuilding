#!/usr/bin/env python
import cv2 
import numpy as np
import rospy
import cv_bridge

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Obj_follower:
	
	def __init__(self):
    		self.bridge = cv_bridge.CvBridge()
    		self.cmd_vel_pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
		self.scan_sub = rospy.Subscriber('/scan',LaserScan, self.scan_callback)
    		self.image_sub = rospy.Subscriber('/usb_cam_right/image_raw',Image, self.image_callback)
    		self.twist = Twist()

	def scan_callback(self,msg):
	    global closest_range
	    closest_range = min(msg.ranges)
	    if (closest_range < 0.1):
		self.twist.linear.x = 0.0
		self.twist.angular.z = 0.0


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
    		contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    		# if object detected find maximum countour
    		if len(contours) > 0 :
        		c = max(contours, key=cv2.contourArea)
        	# Draw bounding rectangle
        	x,y,w,h = cv2.boundingRect(c)
        	cv2.rectangle(res, (x,y), (x+w, y+h), (0,255,0),3)
    		# Display Result
    		#cv2.imshow('frame',frame)
    		#cv2.imshow('mask',mask)
    		#cv2.imshow('res',res)
		#cv2.waitKey(3)
		h1, w1, d = frame.shape
    		size = (h1*w1)/(w*h)
		#print "square size",(w*h)
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
		print "ratio", size
		cx = x + w/2
		cy = y + h/2
		err = cx - w1/2
		if(err != 0):
        		errorSign = -err/abs(err)
			self.twist.angular.z = float(abs(err))*errorSign / 350
		if (size > 15 and size < 21):
			self.twist.linear.x = 0.0
          			
		if (size > 21 and size < 200 and closest_range >1):
			self.twist.linear.x = 0.5
          			#self.twist.angular.z = float(abs(err))*errorSign / 500
		if (size > 200 and size < 1000 and closest_range >1):
			self.twist.linear.x = 0.7
          			#self.twist.angular.z = float(abs(err))*errorSign / 500
		if (size > 1000 and closest_range >1):
			self.twist.linear.x = 0.9
          			#self.twist.angular.z = float(abs(err))*errorSign / 500
		self.cmd_vel_pub.publish(self.twist)
    	
rospy.init_node('follower')
follower = Obj_follower()
rospy.spin()















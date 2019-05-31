#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import numpy as np
from std_srvs.srv import Empty
import cv2
import cv_bridge


def enter_teleop(req):

	global last_press, state
	state = 'teleop'
	last_press = rospy.Time.now()
	return([])


def image_cb(msg):

        cap = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
	centers = []
	# Read the video
	hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
	# define range of yellow color in HSV
	lower_yellow = np.array([80,72,90])
	upper_yellow = np.array([130,255,255])


	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(cap, cap, mask= mask)
	# Find Contours
	contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# if object detected find maximum contour
	centers = []
	for c in contours:
	    area = cv2.contourArea(c)
	    if area > 10000 :
		x,y,w,h = cv2.boundingRect(c)
		#cv2.rectangle(res, (x,y), (x+w, y+h), (0,255,0),3)
		M = cv2.moments(c)
		cX = int(M['m10'] /M['m00'])
		cY = int(M['m01'] /M['m00'])
		centers.append([cX,cY])
		#print(centers)
	if len(centers) >=2:
	  dx = (centers[0][0] + centers[1][0])/2
	  dy = (centers[0][1] + centers[1][1])/2
	  cv2.circle(res,(dx,dy),10,(0,0,255),-1)
	  msgout.linear.x = np.clip(msgout.linear.x + 0.1, 0, max_speed)
	  msgout.angular.z = np.clip(0.01 * (w / 2 - cx), -2, 2)

	else:
	  msgout.linear.x = np.clip(msgout.linear.x - 0.1, 0, max_speed)
	  msgout.angular.z = np.clip(msgout.angular.z + 0.1, 0, 2)
	  
	# Display Result
	cv2.imshow('frame',cap)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	cv2.waitKey(3) 

if __name__ == "__main__":

	# Global params
	resume_delay = rospy.Duration.from_sec(rospy.get_param("/resume_delay"))
	max_speed = rospy.get_param("/max_speed")

	rospy.init_node('line_nav', anonymous=True)
	bridge = cv_bridge.CvBridge()
	cv2.namedWindow("window", 1)

	rospy.sleep(1)  # sleep to get Time.now() working
	last_press = rospy.Time.now() - resume_delay
	s = rospy.Service('button_press', Empty, enter_teleop)

	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('/right/image_rect_color', Image, image_cb)
	msgout = Twist()

	rospy.spin()

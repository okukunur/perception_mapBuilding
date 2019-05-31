#!/usr/bin/env python
# Intro to Robotics - EE5531 - Spring 2018

import rospy
from sensor_msgs.msg import Image
import cv2
import cv_bridge
import numpy as np
from collections import deque
from geometry_msgs.msg import Twist
import argparse
import time
import math
from sensor_msgs.msg import Joy



##########################
#Tracker Class. Has an init function and a couple callbacks. One for the remote
#and one for the camera.
##############################################
class Tracker:
    def __init__(self):

        #self.image_sb = rospy.Subscriber('/usb_cam_left/image_raw', Image, self.image_callback)
        rospy.Subscriber("/bluetooth_teleop/joy", Joy, self.joy_callback)

        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.twist = Twist()
        self.init_size=0.0
        self.lanefollow = 0   #flag for lane follow
	self.crosskey = 0     #flag for stop line
	self.manualmode = 0
     
	self.count = 0	#counters to filter a little jitter
        self.lin_count = 0	
        self.inital_time = time.time()	#system time
        self.rate_step = 0.005	#rate that velocity ramps
        self.ang_vel_before = 0.0	#stor previous values for filtering
        self.lin_vel_before = 0.0
        self.size_before = 0.0

    ##################################
    # Callback function for remote button input
    # Starts tracking with a circle button stops with an x
    ######################################### 
    def joy_callback(self, data):

        x, circ, sq, tri, L1, R1, share, options, p4, L3, R3, DL, DR, DU, DD = data.buttons
        llr, lud, L2, rlr, rud, R2 = data.axes
	##lane follow
	if (circ == 1):
            rospy.loginfo("Circle Key pressed")
	    self.lanefollow = 1
	    self.crosskey = 0
	    self.manualmode = 0
	
	##Stop line
	if (x == 1):
            rospy.loginfo("Cross key tracking")
	    self.crosskey = 1
	    self.lanefollow = 0
	    self.manualmode = 0

	##Manual mode
	if (L1 == 1):
            rospy.loginfo("Cross key tracking")
	    self.crosskey = 0
	    self.lanefollow = 0
	    self.manualmode = 1
   
	#Prints messages when it is in that state
        if(self.lanefollow):
	    rospy.loginfo("Lane follow behavior running")
	elif(self.crosskey):
	    rospy.loginfo("Stop line behavior running")
	elif(self.manualmode):
	    rospy.loginfo("Manual mode running")		

rospy.init_node('Track_Marker')
Track_Marker = Tracker()
rospy.spin()

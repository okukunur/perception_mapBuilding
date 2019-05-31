#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np
import time


#Pull in parameters
maxSpeed = rospy.get_param("/maxSpeed_stopping") #Max speed
delayT   = rospy.get_param("/delayT")   # Time delay in seconds
distanceD= rospy.get_param("/distanceD")# Distance from wall in meters
g_ranges = []
wallFound = False
stop = 0
timebefore = rospy.Time.from_sec(time.time()).to_sec();
timenow = rospy.Time.from_sec(time.time()).to_sec();
alreadystopped = 0

class Follower:

  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    #cv2.namedWindow("window", 1)
    self.laser = rospy.Subscriber('/scan', LaserScan, self.laser_callback, queue_size=1)
    self.image_sub = rospy.Subscriber('/usb_cam_right/image_raw', 
                                     Image, self.image_callback, queue_size=1)

    #self.image_sub = rospy.Subscriber('/right/image_raw', 
                              #     Image, self.image_callback, queue_size=1)

    #self.laser = rospy.Subscriber('/front/scan', LaserScan, self.laser_callback, queue_size=1)






    self.cmd_vel_pub = rospy.Publisher('/rawTwist',Twist, queue_size=1)
    self.cmd_vel = rospy.Publisher('cmd_vel',Twist, queue_size=1)
    self.twist = Twist()

  def laser_callback(self,msg):
    global g_ranges
    global wallFound
    g_ranges = msg.ranges
    global min_distance
    min_distance = min (msg.ranges)
    if min_distance < 0.5:
        self.twist.linear.x = 0
        self.twist.angular.z = 0
    	self.cmd_vel.publish(self.twist)
	rospy.signal_shutdown("Obstacle detected")
  def image_callback(self,msg):
    global g_ranges
    global wallFound
    global stop
    global timebefore
    global timenow

    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, w, d = image.shape
    search_top = h/2
    search_bot = search_top + 30
    image[0:search_top, 0:w] = 0
    image[:, w-50:w] = 0
    image[:, 0:50] = 0
    ############################################

    lower_yellow = np.array([110,50,50])
    upper_yellow = np.array([130,255,255])
    #lower_yellow = np.array([ 25,  25,  50])
    #upper_yellow = np.array([80, 255, 240])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(image, image, mask=mask)
    """
    cv2.imshow("window", res)
    cv2.imshow("mask", mask)
    cv2.waitKey(3)
    """
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

    ret,thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)

    #cv2.imshow("theshold", thresh1)

    contourslast,hierarchy = cv2.findContours(thresh1.copy(), 1, 2)
    #print len(contourslast)

    areas = [cv2.contourArea(c) for c in contourslast]
    if (len(areas)!=0):
	    max_index = np.argmax(areas)

	    rqd_cntr_area = max(areas)
	    filtered_contours = filter(lambda x: cv2.contourArea(x) >= rqd_cntr_area, contourslast)
	    # Draw final contours
	    final = np.zeros_like(thresh1)
	    cv2.drawContours(final, filtered_contours, -1, 255, -1)

	    #cv2.imshow('Shapes', final)

	    rows,cols = final.shape[:2]
	    [vx,vy,x,y] = cv2.fitLine(contourslast[max_index], cv2.cv.CV_DIST_L2,0,0.01,0.01)
	    #lefty = int((-x*vy/vx) + y)
	    #righty = int(((cols-x)*vy/vx)+y)
	    #cv2.line(final,(cols-1,righty),(0,lefty),(255,255,255),1)
	    #cv2.imshow('final', final)
	    angle = np.arctan(-vy/vx)
	    


	    cv2.waitKey(3)
	    #cv2.destroyAllWindows()

	    #############################################

	    angleerrorsign = angle/abs(angle)

	    #if(angleerrorsign != 0):
	     # self.twist.angular.z = np.clip(0.000001 * float(abs(angle))*angleerrorsign,-0.5,0.5)
	    
	    #self.twist.linear.x = maxSpeed
	    # BEGIN FINDER
	    M = cv2.moments(final)
	    #check the sign of last error

	    #if we are to the left of the line, turn right
	    if M['m00'] > 0:
	      wallFound = True
	      cx = int(M['m10']/M['m00'])
	      cy = int(M['m01']/M['m00'])
	      print"#######################################"
	      print cy
	      #rospy.loginfo(cy)
	      print"#######################################"
	      print h
	      #rospy.loginfo(h)
	      print stop
	      print"#######################################" 

	    if (h-30 < cy < h and stop == 0): #starting for first sight of new line
	      stop = 1
	      timebefore = rospy.Time.from_sec(time.time()).to_sec();
	      self.twist.linear.x = 0
	      #self.twist.linear.x = np.clip(self.twist.linear.x - 0.01, 0, maxSpeed)
	      alreadystopped = 1
	      print "set to 0"

	    if (stop == 1):
	      timenow = rospy.Time.from_sec(time.time()).to_sec();
	      print "printing"
	      print timenow-timebefore
	      print "printed"
	      if (timenow-timebefore < 4.0):
	        self.twist.linear.x = 0
	        #self.twist.linear.x = np.clip(self.twist.linear.x - 0.01, 0, maxSpeed)
		print "waiting"
	      elif (h-50 < cy < h and stop == 1 and timenow-timebefore > 4.0): #dont stop if already stopped for a same line
	        self.twist.linear.x = maxSpeed
	      else:
                #self.twist.linear.x = np.clip(self.twist.linear.x + 0.01, 0, maxSpeed)
	        self.twist.linear.x = maxSpeed
		stop = 0
		print "out of wait"
	    else:
              #self.twist.linear.x = np.clip(self.twist.linear.x + 0.01, 0, maxSpeed)
	      self.twist.linear.x = maxSpeed
    else:
	    self.twist.linear.x = 0
	    #self.twist.linear.x = np.clip(self.twist.linear.x - 0.01, 0, maxSpeed)
	    #self.twist.angular.z = 0.01

    self.cmd_vel_pub.publish(self.twist)
    #cv2.imshow("window", image)
    cv2.waitKey(3)
rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL

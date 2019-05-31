#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
import numpy as np
from std_srvs.srv import Empty
import cv2
import cv_bridge


def enter_teleop(req):
    global last_press, state
    state = 'teleop'
    last_press = rospy.Time.now()
    return([])

def laser_callback(msg):
    global g_ranges
    global wallFound
    g_ranges = msg.ranges
    global min_distance
    min_distance = min (msg.ranges)
    if min_distance < 0.3:
        msgout.linear.x = 0
        msgout.angular.z = 0
    	pub.publish(msgout)
	rospy.signal_shutdown("Obstacle detected")

def image_cb(msg):

    image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([110,50,50])
    upper_yellow = np.array([130,255,255])
    #lower_yellow = np.array([0,0,100])
    #upper_yellow = np.array([100,0,192])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #mask = cv2.erode(mask, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)

    # BEGIN CROP
    area1 = 0
    area2 = 0
    h, w, d = image.shape
    search_top = h*0.6
    search_bot = search_top + 100
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    mask1[0:search_top, 0:w] = 0
    mask1[search_bot:h, 0:w] = 0
    mask1[0:h, 0:w/2] = 0
    mask2[0:search_top, 0:w] = 0
    mask2[search_bot:h, 0:w] = 0
    mask2[0:h, w/2:w] = 0
    res = cv2.bitwise_and(image,image, mask= mask)
    res1 = cv2.bitwise_and(image,image, mask= mask1)
    res2 = cv2.bitwise_and(image,image, mask= mask2)
    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours1, hierarchy1 = cv2.findContours(mask1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours2, hierarchy2 = cv2.findContours(mask2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    cv2.imshow("resmain", res)
    cv2.waitKey(3)

    for c in contours1:
	if (cv2.contourArea(c) > 50):
		area1 = area1 + cv2.contourArea(c)
    for c in contours2:
	if (cv2.contourArea(c) > 50):
		area2 = area2 + cv2.contourArea(c)

    for c in contours:
	if (cv2.contourArea(c) > 20):
		x1,y1,w1,h1 = cv2.boundingRect(c)
		centers.append((x1+w1,y1+h1))
		centers.append((x1,y1))
		#print (centers)
    if (len(centers) != 0):
    	centers = np.asarray(centers)
    	#print (centers[0][0], centers[1][0])
    	print (min(centers[:,0]), min(centers[:,1]), max(centers[:,0]), max(centers[:,1]))
    	cv2.rectangle(res, (min(centers[:,0]),min(centers[:,1])), (max(centers[:,0]),max(centers[:,1])), (0,255,0), -1, 4)
    	cx = (min(centers[:,0]) + max(centers[:,0]))/2
    	cy = (min(centers[:,1]) + max(centers[:,1]))/2
    	cv2.imshow("res", res)
    	cv2.waitKey(3)
	cv2.circle(image, (cx, cy), 20, (0, 0, 255), -1)
	cv2.circle(res, (cx, cy), 20, (0, 0, 255), -1)
	#if ((max(centers[:,0]) - min(centers[:,0])) < 200):
	#    msgout.linear.x = np.clip(msgout.linear.x, min_speed, max_speed)
	#    msgout.angular.z = np.clip(0.08 * (w/2 - (cx - 15)), -0.3, 0.3)
      	if (area1 >= 100 and area2>= 100):
        	msgout.linear.x = np.clip(0.5, 0, max_speed)
        	msgout.angular.z = np.clip(0.002 * (w/2 - (cx+30)), -0.5, 0.5)
	elif (area1 < 100 and area2>= 100):
        	msgout.angular.z = +0.65
	elif (area1 >= 100 and area2< 100):
        	msgout.angular.z = -0.65
	else:
        	msgout.angular.z = 0.65

    else:
        msgout.linear.x = np.clip(msgout.linear.x - 0.01, 0, max_speed)
        msgout.angular.z = 0.0

    #if rospy.Time.now() - last_press > resume_delay:
    pub.publish(msgout)

    #print (centers)
    cv2.imshow("window", image)
    cv2.waitKey(3)


if __name__ == "__main__":

    # Global params
    #resume_delay = rospy.Duration.from_sec(rospy.get_param("/resume_delay"))
    max_speed = rospy.get_param("/maxSpeed")
    min_speed = rospy.get_param("/minSpeed")
    rospy.init_node('line_nav', anonymous=True)
    bridge = cv_bridge.CvBridge()
    g_ranges = []
    wallFound = False
    #cv2.namedWindow("window", 1)

    #rospy.sleep(1)  # sleep to get Time.now() working
    #last_press = rospy.Time.now() - resume_delay
    #s = rospy.Service('button_press', Empty, enter_teleop)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/usb_cam_right/image_raw', Image, image_cb)
    #subleft = rospy.Subscriber('/usb_cam_left/image_raw', Image, image_cb_left)
    laser = rospy.Subscriber('/scan', LaserScan, laser_callback, queue_size=1)
    msgout = Twist()

    rospy.spin()

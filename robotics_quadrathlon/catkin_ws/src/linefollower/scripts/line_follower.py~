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

    image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([110,50,50])
    upper_yellow = np.array([130,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #mask = cv2.erode(mask, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)

    # BEGIN CROP
    h, w, d = image.shape
    search_top = h*0.8
    search_bot = search_top + 100
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    res = cv2.bitwise_and(image,image, mask= mask)
    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for c in contours:
	x1,y1,w1,h1 = cv2.boundingRect(c)
	#cv2.rectangle(res, (x1,y1), (x1+w1, y1+h1), (0,255,0), -1, 4)
	#x_cord = x1+(w1/2)
	#y_cord = y1+(h1/2)
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
    	"""
    	M = cv2.moments(mask)
    	if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
	"""
	if ((max(centers[:,0]) - min(centers[:,0])) < 200):
	   if (max(centers[:,0]) > w/2):
		msgout.linear.x = np.clip(msgout.linear.x - 0.001, min_speed, max_speed)
		msgout.angular.z = np.clip(0.08 * (max(centers[:,0]) - w/2), -0.3, 0.3)
	   elif (max(centers[:,0]) < w/2):
		msgout.linear.x = np.clip(msgout.linear.x - 0.001, min_speed, max_speed)
		msgout.angular.z = np.clip(0.08 * (w / 2 - max(centers[:,0])), -0.3, 0.3)
        
	else:
	    cv2.circle(image, (cx, cy), 20, (0, 0, 255), -1)
            msgout.linear.x = np.clip(msgout.linear.x + 0.001, 0, max_speed)
            msgout.angular.z = np.clip(0.08 * (w / 2  -cx), -0.3, 0.3)

    else:
        msgout.linear.x = np.clip(msgout.linear.x - 0.01, 0, max_speed)
        msgout.angular.z = np.clip(msgout.angular.z - 0.03, 0, 0.3)

    if rospy.Time.now() - last_press > resume_delay:
        pub.publish(msgout)

    else:  # make it 0 for a smooth start
        msgout.linear.x = 0
        msgout.angular.z = 0

    cv2.imshow("window", image)
    cv2.waitKey(3)

if __name__ == "__main__":

    # Global params
    resume_delay = rospy.Duration.from_sec(rospy.get_param("/resume_delay"))
    max_speed = rospy.get_param("/max_speed")
    min_speed = rospy.get_param("/min_speed")
    rospy.init_node('line_nav', anonymous=True)
    bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)

    rospy.sleep(1)  # sleep to get Time.now() working
    last_press = rospy.Time.now() - resume_delay
    s = rospy.Service('button_press', Empty, enter_teleop)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/usb_cam_right/image_raw', Image, image_cb)

    msgout = Twist()

    rospy.spin()

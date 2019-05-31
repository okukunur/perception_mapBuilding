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
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # BEGIN CROP
    h, w, d = image.shape
    search_bot = int(h * 0.9)
    search_top = int(search_bot - h * 0.25)
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    res = cv2.bitwise_and(image,image, mask= mask)
    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for c in contours:
	x1,y1,w1,h1 = cv2.boundingRect(c)

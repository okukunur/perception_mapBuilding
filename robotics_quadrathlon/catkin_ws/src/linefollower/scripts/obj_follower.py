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

    # BEGIN CROP
    h, w, d = image.shape
    search_top = h*0.6
    search_bot = search_top + 30
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0

    M = cv2.moments(mask)
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(image, (cx, cy), 20, (0, 0, 255), -1)
	cv2.circle(mask, (cx, cy), 20, (0, 0, 255), -1)

        msgout.linear.x = np.clip(msgout.linear.x + 0.03, 0, max_speed)
        msgout.angular.z = np.clip(0.01 * (w / 2 - cx -30), -0.5, 0.5)

    else:
        msgout.linear.x = np.clip(msgout.linear.x - 0.03, 0, max_speed)
        msgout.angular.z = np.clip(msgout.angular.z + 0.03, 0, 0.5)

    if rospy.Time.now() - last_press > resume_delay:
        pub.publish(msgout)

    else:  # make it 0 for a smooth start
        msgout.linear.x = 0
        msgout.angular.z = 0

    cv2.imshow("window", image)
    cv2.waitKey(3)
    cv2.imshow("mask", mask)
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
    sub = rospy.Subscriber('usb_cam_right/image_raw', Image, image_cb)
    msgout = Twist()

    rospy.spin()

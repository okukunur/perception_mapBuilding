#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import numpy as np
import cv2
import cv_bridge
from std_msgs.msg import String
from std_srvs.srv import Empty

def enter_teleop(req):
    global last_press, state
    state = 'teleop'
    last_press = rospy.Time.now()
    return([])

def image_cb(msg):

    image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    h, w, d = image.shape

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([71, 76, 0])
    upper_blue = np.array([142, 255, 255])
    line = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((11, 11), np.uint8)
    line = cv2.morphologyEx(line, cv2.MORPH_CLOSE, kernel)
    lineCopy = np.copy(line)

    # BEGIN CROP
    search_bot = int(h * 0.9)
    search_top = int(search_bot - h * 0.25)
    mask = np.zeros((h + 2, w + 2), np.uint8)
    mask[0:search_top, :] = 255
    mask[search_bot:-1, :] = 255
    cv2.floodFill(line, mask, (w / 2, search_bot - 2), 255)
    cv2.imshow("mask", mask)
    cv2.waitKey(3)
    M = cv2.moments(line)
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
	 # make other line blue
        image[:, :, 2] = np.clip(image[:, :, 2].astype('uint8') + line / 5,0, 255).astype('uint8')
	# mark center 
        cv2.circle(image, (cx, cy), 10, (255, 0, 0), -1)  
        cv2.imshow("image", image)
        cv2.waitKey(3)
        wz = - 0.02 * (cx - w / 2)

        msgout.linear.x = np.clip(msgout.linear.x + 0.1, 0, max_speed)
        msgout.angular.z = np.clip(wz, -1.5, 1.5)

    else:
        msgout.linear.x = np.clip(msgout.linear.x - 0.1, 0, max_speed)
        msgout.angular.z = np.clip(msgout.angular.z + 0.1, 0, 1)

    if rospy.Time.now() - last_press > resume_delay:
        pub.publish(msgout)

    else:  # make it 0 for a smooth start
        msgout.linear.x = 0
        msgout.angular.z = 0

    mask_message = bridge.cv2_to_imgmsg(image, encoding="bgr8")
    pub_mask.publish(mask_message)
    image_message = bridge.cv2_to_imgmsg(lineCopy, encoding="passthrough")
    pub_lane.publish(image_message)


if __name__ == "__main__":

    # Global params
    resume_delay = rospy.Duration.from_sec(rospy.get_param("/resume_delay"))
    max_speed = rospy.get_param("/max_speed")
    min_speed = rospy.get_param("/min_speed")
    rospy.init_node('line_nav', anonymous=True)
    bridge = cv_bridge.CvBridge()
    
    rospy.sleep(1)  # sleep to get Time.now() working
    last_press = rospy.Time.now() - resume_delay
    s = rospy.Service('button_press', Empty, enter_teleop)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    pub_mask = rospy.Publisher('mask', Image, queue_size=10)
    pub_lane = rospy.Publisher('line', Image, queue_size=10)
    sub = rospy.Subscriber('/usb_cam_right/image_raw', Image, image_cb)

    msgout = Twist()

    rospy.spin()

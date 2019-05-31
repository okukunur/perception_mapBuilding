#!/usr/bin/env python

import os
import rospy
import curses
import math
from std_msgs.msg import String
from std_msgs.msg import Header
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

Pi = math.pi
dist = 1
search_range_angle = 5  # looks at +/- this degrees to calculate the range
global execution
execution = True
pub = rospy.Publisher('/jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
twist = Twist()


def callback(data):
    global execution
    if(execution):
        execution = navigateToNearestWall(data)
    rospy.loginfo(isObstaclePresent(data))
    rospy.loginfo(obstacleDistance(data))

    
def isObstaclePresent(data):
    # Verifies if there is obstacle straight ahead
    # centre_index is 360
    wall_dist = obstacleDistance(data)
    if(wall_dist <= dist):
        rospy.loginfo(True)
        return True
    else:
        rospy.loginfo(False)
        return False

    
def obstacleDistance(data):
    # return the distance for the obstacle ahead
    min_range_search = int(360 - round(2.66 * search_range_angle))
    max_range_search = int(360 + round(2.66 * search_range_angle))
    avg_wall_distance = (data.ranges[max_range_search] + data.ranges[min_range_search]) / 2
    print "wall distance", avg_wall_distance
    return avg_wall_distance


def navigateToNearestWall(data):
    """length = len(data.ranges)
    complete_range = data.ranges
    maximum_range = max(data.ranges)"""
    rate = rospy.Rate(5)
    closest_range = min(data.ranges)
    index = data.ranges.index(min(data.ranges))
    angle = data.angle_min + (data.angle_increment * index)
    angle = angle * 180 / Pi
    pub = rospy.Publisher('/jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
    twist = Twist()
    try:
        while not rospy.is_shutdown():
            rate.sleep()
            print "closest range ", closest_range
            print "angle", angle
            while not rospy.is_shutdown():   
                if angle > 2 & (closest_range > 1):
                    twist.angular.z = 0.2
                    while angle > 2:
                        pub.publish(twist)
                            
                if angle < -2 & (closest_range > 1):
                    twist.angular.z = -0.2
                    while angle < -2:
                        pub.publish(twist)
        
                if (angle > -2) & (angle < 2) & (closest_range > 1):    
                    twist.angular.z = 0
                    twist.linear.x = 0.3
                    pub.publish(twist)
                else:
                    print "================================================"
                    twist.linear.x = 0.0
                    twist.angular.z = 0
                    pub.publish(twist)            
                    return False
             
    except rospy.ROSInterruptException:
            print "Key Board interruption"
      
    return False

    
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('laserListener', anonymous=True)
    rospy.Subscriber("/front/scan", LaserScan, callback)
    # rospy.Subscriber("/front/scan", LaserScan, isObstaclePresent)
    # rospy.Subscriber("/front/scan", LaserScan, obstacleDistance)
    # rospy.Subscriber("/front/scan", LaserScan, rotateUntillNoObstacle)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()


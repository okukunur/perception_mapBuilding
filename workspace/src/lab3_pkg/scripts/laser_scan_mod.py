#!/usr/bin/env python

import rospy
import sys
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import time
import math
from datetime import datetime
Pi = math.pi

#------------------------------------------#
# Variables which can be modified later    #
# these hold the time to wait from teleop  #
# and distance to stay away from wall.     #
#------------------------------------------#
delayT     = 10   # Time delay in seconds
distanceD  = 1  # Distance from wall in meters
maxSpeed   = 2.0

#mapping of keys to velocity data
key_mapping = { 'w': [ 0, maxSpeed], 'x': [0, -maxSpeed], 
                'a': [maxSpeed, 0], 'd': [-maxSpeed,  0], 
                's': [ 0, 0] }
g_last_twist = None 
#teleop = True
teleopTime = (delayT + time.time())
global angle
angle = 0
global initialSpeed
initialSpeed = 0.25
#list to hold random number, negative and positive are
#used for steering angles
items = [-1, 1]
global angleOffset

#Function which takes in the laserScan message
def scan_callback(msg):
    global closest_range
    global maximum_range
    global complete_range
    global angle
    global index
    closest_range = min(msg.ranges)
    length = len(msg.ranges)
    complete_range = msg.ranges
    print "totalrange", len(complete_range)
    maximum_range = max(msg.ranges)
    index = msg.ranges.index(min(msg.ranges))
    angle = msg.angle_min + (msg.angle_increment*index)
    angle = angle*180/Pi
    obstacleDistance()
    sideWallDist("left")
    sideWallDist("right")
    isObstaclePresent()



def turnTillPerpenndiculatTowallandMoveTowardsIt():
    global angle
    global index
    global initialSpeed
    #if(350>=index & index>=370):
     #   g_last_twist.angular.z = angle

    if (isObstaclePresent()):
       print "Obstacle ahead"
       initialSpeed = initialSpeed - 0.3*initialSpeed 
       g_last_twist.linear.x = initialSpeed
    elif not isObstaclePresent():
       print "No obstacle ahead"
       initialSpeed = initialSpeed + 0.1*initialSpeed 
       g_last_twist.linear.x = initialSpeed
    if distanceD-(distanceD/20) < obstacleDistance() < distanceD+(distanceD/20):
       initialSpeed = 0
    return

def isObstaclePresent():
    # Verifies if there is obstacle straight ahead
    # centre_index is 360
    if(obstacleDistance() <= distanceD+3):
        rospy.loginfo(True)
        return True
    else:
        rospy.loginfo(False)
        return False

def sideWallDist(side):
    global angle;
    global index;

    sideAngle = 10; #ranges of angle to average to find side wall dist
    sidewalldist = 0;
    if('left' in side):
        minrange = int(math.floor(2.66*90-sideAngle/2));
        maxrange = int(math.floor(2.66*90+sideAngle/2));
        print "minrange", minrange
        print "maxrange", maxrange
        #print complete_range
        sidewalldist = (complete_range[minrange] + complete_range[maxrange])/2;
    elif('right' in side):
        minrange = int(math.floor(2.66*-90-sideAngle/2));
        maxrange = int(math.floor(2.66*-90+sideAngle/2));
        print "minrange", minrange
        print "maxrange", maxrange
        #print complete_range
        sidewalldist = (complete_range[minrange] + complete_range[maxrange])/2;
    return abs(sidewalldist)  

def obstacleDistance():
    search_range_angle = 3  # looks at +/- this degrees to calculate the range
    # return the distance for the obstacle ahead
    min_range_search = int(360 - round(2.66 * search_range_angle))
    max_range_search = int(360 + round(2.66 * search_range_angle))
    avg_wall_distance = (complete_range[max_range_search] + complete_range[min_range_search]) / 2
    print "wall distance", avg_wall_distance
    return avg_wall_distance

#Function which will stop the wall following code
def key_callback(msg,twist_pub):
    global teleop
    global teleopTime
    global g_last_twist
    #Now check if the keypress was valid..
    if len(msg.data) == 0 or not key_mapping.has_key(msg.data[0]):
        return # unknown key.
    teleop = True
    teleopTime = (delayT + time.time())
    #act upon keypress...
    vels = key_mapping[msg.data[0]]
    g_last_twist.angular.z = vels[0]
    g_last_twist.linear.x  = vels[1]
    twist_pub.publish(g_last_twist)
    
    return
def gostraight():
    global initialSpeed;
    if (isObstaclePresent()):
       print "Obstacle ahead"
       initialSpeed = initialSpeed - 0.3*initialSpeed 
       g_last_twist.linear.x = initialSpeed
    elif not isObstaclePresent():
       print "No obstacle ahead"
       initialSpeed = initialSpeed + 0.1*initialSpeed 
       g_last_twist.linear.x = initialSpeed
    if distanceD-(distanceD/20) < obstacleDistance() < distanceD+(distanceD/20):
       initialSpeed = 0
    return
def rotate(condition):
    print "in", angleOffset
    if "left" in condition:
       print "here"
       g_last_twist.angular.z = (angle + 90)/50 + angleOffset;
       g_last_twist.linear.x = 0.0;
    elif "right" in condition:
       print "here"
       g_last_twist.angular.z = (angle - 90)/50 - angleOffset;
       g_last_twist.linear.x = 0.0;
    elif "U-turn" in condition:
       print "here"
       g_last_twist.angular.z = (angle - 90)/25 - angleOffset;
       g_last_twist.linear.x = 0.0;   

if __name__ == "__main__":
    closest_range = 2.0
    complete_range = []
    global teleop;
    global angle;
    global speed;
    orientation = 1
    teleop = True
    global angleOffset
    try:
        #initiate node with name rand, It is overwritten in the launch file
	rospy.init_node("rand");
	#Subscribe to appropriate topics
        rospy.Subscriber('/front/scan', LaserScan, scan_callback)
	pub = rospy.Publisher('rawTwist', Twist, queue_size=1)
	
	rospy.Subscriber('keys', String, key_callback, pub)
        print "init"
        #rospy.Subscriber('/front/scan', LaserScan, turnTillPerpenndiculatTowallandMoveTowardsIt)
	rate = rospy.Rate(10)
	twist = Twist()
	g_last_twist = Twist()

    	while not rospy.is_shutdown():
    	    #if a recent teleop occurred we need to find closest wall again
    	    if teleop and (teleopTime < time.time() - 1):
    	        g_last_twist.linear.x = 0.0
    	        g_last_twist.angular.z = 0.0
    
            if teleop and teleopTime < time.time():
       	        #We start with zero after teleop has been dead for a time                				
    	        if (closest_range > distanceD):
	            print "here"
    	            turnTillPerpenndiculatTowallandMoveTowardsIt()
                    if distanceD-(distanceD/20) < obstacleDistance() < distanceD+(distanceD/20):
                       initialSpeed = 0
                       g_last_twist.linear.x = initialSpeed;
    		    pub.publish(g_last_twist)
                    print "published"
    		elif (closest_range <= distanceD):
    		    print "Should be stoping......"
    		    g_last_twist.linear.x = 0.0;
    		    g_last_twist.angular.z = 0.0;
    		    #we made it to the wall so set teleop to False
    		    teleop = False;
    		    pub.publish(g_last_twist);
    		    direction = random.random()*10; # Pick a random item from the list
                    print "Direction is ", direction;
    		    orientation = direction*(-1);

	    rate.sleep()
            

            if closest_range < distanceD:
                angleOffset = (distanceD + closest_range)/(60*distanceD)
            elif closest_range > distanceD:
                angleOffset = (-1)*(distanceD + closest_range)/(60*distanceD) 
            print "out", angleOffset

            if sideWallDist("left") > sideWallDist("right"):
                print("====================1=============================")
                print "Obstacledistace", obstacleDistance()
                print "lower dist", distanceD-(distanceD/20)
                print "upper dist", distanceD+(distanceD/20)
                if (isObstaclePresent()):
                   rotate("left")
                else:
                   gostraight()
                pub.publish(g_last_twist)  
            elif sideWallDist("left") < sideWallDist("right"):
                print("====================2=============================")
                print "Obstacledistace", obstacleDistance()
                print "lower dist", distanceD-(distanceD/20)
                print "upper dist", distanceD+(distanceD/20)
                if (isObstaclePresent()):
                   rotate("right")
                pub.publish(g_last_twist) 
            elif distanceD-(distanceD/20)+1 < sideWallDist("left") < distanceD+(distanceD/20)+1 & distanceD-(distanceD/20)+1 < sideWallDist("right") < distanceD+(distanceD/20)+1:
                print("====================3=============================")
                print "Obstacledistace", obstacleDistance()
                print "lower dist", distanceD-(distanceD/20)
                print "upper dist", distanceD+(distanceD/20)
                if (isObstaclePresent()):
                   rotate("U-turn")
                pub.publish(g_last_twist) 
            else:
                print("====================4=============================")
                rotate("right")

            gostraight()
            pub.publish(g_last_twist)
            if distanceD-(distanceD/20) < obstacleDistance() < distanceD+(distanceD/20):
               initialSpeed = 0
               g_last_twist.linear.x = initialSpeed;
    	    pub.publish(g_last_twist)
    	    rate.sleep()	

    except rospy.ROSInterruptException:
	print "Exception caught...exiting"
        pass












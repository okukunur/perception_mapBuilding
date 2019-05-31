import rospy
import roslaunch
import sys
import time
import os

from   sensor_msgs.msg import Joy

# class to read joystick messages and launch node
class joy_control(object):

    # define self routine
    def __init__(self):

        # define subscriber
        rospy.Subscriber("/bluetooth_teleop/joy", Joy, self.joy_callback)
        rate = rospy.Rate(5)

        rospy.loginfo('started joystick routine..')

        # define and init variables
        self.start1 = False
        self.stop1  = False
        self.start2 = False
        self.stop2  = False
        self.start3 = False
        self.stop3  = False
        self.start4 = False
        self.stop4  = False

        # configure node roslaunch api
        package    = 'quad'

        executable1 = 'obj_follower.py'
        executable2 = 'lane_follower.py'
        executable3 = 'line_stopping.py'
	executables = 'pidWrapper.py'
        executable4 = 'laser_scan.py'

        node1 = roslaunch.core.Node(package, executable1)
        node2 = roslaunch.core.Node(package, executable2)
        node3 = roslaunch.core.Node(package, executable3)
        #nodes = roslaunch.core.Node(package, executables)
        node4 = roslaunch.core.Node(package, executable4)

        launch = roslaunch.scriptapi.ROSLaunch()
        launch.start()

        while not rospy.is_shutdown():
            # if start flag set: launch main launch-file

            if self.start1:
                process1 = launch.launch(node1)
            if self.stop1:
		if 'process1' in locals():
                    process1.stop()

            if self.start2:
                process2 = launch.launch(node2)
            if self.stop2:
		if 'process2' in locals():
                    process2.stop()

            if self.start3:
		#processs = launch.launch(nodes)
                process3 = launch.launch(node3)

            if self.stop3:
		if 'process3' in locals():
                    process3.stop()
		    #processs.stop()

            if self.start4:
                process4 = launch.launch(node4)
            if self.stop4:
		if 'process4' in locals():
                    process4.stop()

	    self.start1 = False
	    self.start2 = False
	    self.start3 = False
	    self.start4 = False

	    self.stop1 = False
	    self.stop2 = False
	    self.stop3 = False
	    self.stop4 = False

	    rate.sleep()

    # joystick callback routine
    def joy_callback(self, data):

        # define joystick buttons
        x, circ, sq, tri, L1, R1, share, options, p4, L3, R3, DL, DR, DU, DD = data.buttons
        llr, lud, L2, rlr, rud, R2 = data.axes

        # Start object tracking
        if (tri == 1) and (self.start1 == False) :
            rospy.loginfo("Starting the object tracking routine...")
            # set the start flag
 	    self.start1 = True         
            
        # Start lane following
        if (circ == 1) and (self.start2 == False):
            rospy.loginfo("Starting the Lane following routine...")
            # set the start flag
            self.start2 = True
            
        # Start line stopping
        if (x == 1) and (self.start3 == False):
            rospy.loginfo("Starting the line stopping routine...")
            # set the start flag
            self.start3 = True          

        # Start wall following
        if (sq == 1) and (self.start4 == False):
            rospy.loginfo("Starting the wall following routine...")
            # set the start flag
            self.start4 = True
            

        # Stop tracking
        if (R1 == 1 or L1 == 1):
            rospy.loginfo("Switching to Manual...")
            # set stop flag
            self.stop1  = True
            self.stop2  = True
            self.stop3  = True
            self.stop4  = True
	    

# standard boilerplate
if __name__ == "__main__":
    try:
        rospy.init_node("joy_start", anonymous=False)
        #read in joystick input
        run = joy_control()
    except rospy.ROSInterruptException:
	rospy.loginfo("joy_start node terminated.")

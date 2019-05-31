#Perception: Map Building

**Tasks to achieve**

1. Build a map of the world ‘project3’ by exploring as quickly as possible
2. Make sure that Jackal motion is smooth without any sudden movements
      - Implement a have control strategy to achieve this motion
3. Get the time required to build the map
4. Display this three instances of map during building


### Team

>Om Kukunuru(Team Lead)

>Sam Kysar

>Sphurti More

## To clone and run project

***1)*** Assumes ROS Indigo and Gazebo 2, clone repository [HERE](https://bitbucket.org/ee5531sp2018/royalpotato/commits/all)

***2)*** open new terminal

***3)*** type: ***cd <path to local repository>/royalpotato/workspace/*** replacing <path to local repository> with the path to local repository

***4)*** type: ***ls*** verify only local folder is src, if not remove all but src

***5)*** type: ***catkin_make***

***6)*** type: ***source devel/setup.bash***

***7)*** open new terminal

***8)*** type: ***cd <path to local repository>/royalpotato/workspace/***       replacing <path to local repository> with the path to local repository

***9)*** type: ***source devel/setup.bash***

***10)*** type: ***roslaunch lab3_pkg lab3.launch config:=front_laser*** In first terminal

***11)*** type: ***roslaunch jackal_viz view_robot.launch config:=gmapping*** In second terminal to view map building in rviz

***12)*** type: ***rosrun map_server map_saver -f <map_name>*** To save map in separate terminal.


***Note:*** If during the launch of lab3.launch file any red shows up in terminal Gazebo may have launched erroneously, therefore hit ctrl c to kill the process and retry steps 10-12 as needed. Gazebo has some problems at times launching also repeat if Gazebo shows only black on the screen.

***Note:*** Second note, the model parameter is set to start driving after 20 seconds giving the operator time to launch rviz with gmapping. This parameter is in the lab3.launch file.

## Working of Project

A launch file ***lab3.launch*** is created which initializes the world ***project3.world***, the navigation python file ***laser_scan.py***, the jackal's movement control file ***twistBuffer.py*** and ***gmapping.launch***.

To run the launch file:
***roslaunch lab3_pkg lab3.launch config:=front_laser***

When the launch file is launched, the gazebo brings up the world, jackal is launched and the gmapping is started. Along with this, jackal navigates to the nearest wall and starts exploring the whole world and starts  mapping instantaneously. For the navigation, the jackal uses the laser scan data (range and angle). 

Once you feel the mapping is done, save the file using the following command along with the previous in another terminal

***rosrun map_server map_saver -f <map_name>***

To view the mapping at any point of time, open rviz
***roslaunch jackal_viz view_robot.launch config:=gmapping***

## Control Strategy for Motion Control

Continuous input of the wall distances and the obstacles are calculated. Based on these values the control loop calculates whether it is moving towards the wall or it moving away from the wall. These values are used for angular corrections and linear motion. If the there are no obstacles and if the jackal is moving straight, then jackal continuously increases the velocity and if it is going to approach a wall, then it decreases the velocity gradually. 

In order to filter out the impulse drives to the motors a simple moving average filter was implemented. The filter block was built by creating an array of zeros which has 15 indexes each new input from laser control is appended while the last one is popped. All are then summed and then divided by 15. The main reason for implementing the mid message filtering was that initially loops were tried but the computation and complexity quickly adds to the main control algorithm so it was thought best to implement a filter on the message data abstracting it away from the control. Also from past experience with this type of filter it was thought to be a good idea as it is just a basic FIR filter.

![rqt_plot.png](https://bitbucket.org/repo/R9ox7XM/images/4087356885-rqt_plot.png)


## Map being built

![image1.png](https://bitbucket.org/repo/R9ox7XM/images/3764763739-image1.png)

![image2.png](https://bitbucket.org/repo/R9ox7XM/images/2592534013-image2.png)

![image3.png](https://bitbucket.org/repo/R9ox7XM/images/2621844952-image3.png)

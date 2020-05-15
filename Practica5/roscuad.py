#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x = 0
y = 0
z = 0
theta = 0

def poseCallback(pose_message):
    global x
    global y
    global z
    global theta
    
    x = pose_message.x
    y = pose_message.y
    theta = pose_message.theta

def orientate (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'

    while(True):
        ka = 4.0
        val_y = ygoal-y
        val_x = xgoal-x
        desired_angle_goal = math.atan2(val_y, val_x)
	dtheta = desired_angle_goal-theta   
        if (dtheta < 0):
            dtheta = theta - desired_angle_goal
	angular_speed = ka * (dtheta)

        velocity_message.linear.x = 0.0
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        print ('angle =',dtheta)

        if (dtheta < 0.01):
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)
            break

def go_to_goal (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'

    while(True):
        kv = 0.5				
        distance = abs(math.sqrt(((xgoal-x)**2)+((ygoal-y)**2)))
        linear_speed = kv# * distance

        ka = 4.0
        val_y = ygoal-y
        val_x = xgoal-x
        #if (val_y < 0.1):
            #val_y = 0.1
        #if (val_x < 0.1):
        #    val_x = 0.1
        desired_angle_goal = math.atan2(val_y, val_x)
	dtheta = desired_angle_goal-theta        
	angular_speed = ka * (dtheta)

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        #print ('x=', x, 'y=', y)

        if (distance < 0.01):
            velocity_message.linear.x = 0.0
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)
            break

if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)     

	
	time.sleep(2.0)
	orientate(5,8)
	#time.sleep(1.0)
	go_to_goal(5,8)
	#time.sleep(1.0)	

	orientate(2,8)
	go_to_goal(2,8)

	orientate(2,5)
	go_to_goal(2,5)

	orientate(5,5)
	go_to_goal(5,5)
		


    except rospy.ROSInterruptException:        
	pass

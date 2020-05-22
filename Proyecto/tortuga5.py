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

x1,x2,x3,x4,x6 = 0,0,0,0,0
y1,y2,y3,y4,y6 = 0,0,0,0,0


def myCallback(pose_message):
    global x
    global y
    global z
    global theta

    x = pose_message.x
    y = pose_message.y
    theta = pose_message.theta

def poseCallback1(pose_message):
    global x1
    global y1
    x1 = pose_message.x
    y1 = pose_message.y

def poseCallback2(pose_message):
    global x2
    global y2
    x2 = pose_message.x
    y2 = pose_message.y

def poseCallback3(pose_message):
    global x3
    global y3
    x3 = pose_message.x
    y3 = pose_message.y

def poseCallback4(pose_message):
    global x4
    global y4
    x4 = pose_message.x
    y4 = pose_message.y

def poseCallback6(pose_message):
    global x6
    global y6
    x6 = pose_message.x
    y6 = pose_message.y

def orientate (angle):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle5/cmd_vel'
    desired_angle_goal = theta + angle
    ka = 4.0

    while(True):

        dtheta = desired_angle_goal-theta   
        angular_speed = ka * (dtheta)

        velocity_message.linear.x = 0.0
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        #print ('angle =',dtheta)

        if (abs(dtheta) < 0.1):
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)
            break

def for_the_horde(xgoal,ygoal):    
    global x
    global y
    global theta  
    velocity_message = Twist()
    cmd_vel_topic = '/turtle5/cmd_vel'

    distance = abs(math.sqrt(((xgoal-x)**2)+((ygoal-y)**2)))
    kv = 0.35
    ka = 8
    angle = 30 * (2*math.pi/360)

    while(True):   	 
        distance = abs(math.sqrt(((xgoal-x)**2)+((ygoal-y)**2)))

        if (distance < 0.1):
            velocity_message.linear.x = 0.0
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)
            break

        lefty = False
        if xgoal < x :
            lefty = True

        despejado = sniffin()

        if despejado:
            linear_speed = kv * distance
            desired_angle_goal = math.atan2(ygoal-y, xgoal-x)
            dtheta = desired_angle_goal-theta   	 

            if lefty and dtheta >0:
                dtheta = -2*math.pi+dtheta

            if abs(dtheta) < 0.00001:
                dtheta = 0

            angular_speed = ka * (dtheta)
            velocity_message.linear.x = linear_speed
            velocity_message.angular.z = angular_speed
            velocity_publisher.publish(velocity_message)

        else:
            velocity_message.linear.x = 0.0
            velocity_message.angular.z = 0.0
            velocity_publisher.publish(velocity_message)
            if lefty:
                orientate(angle)
            else:
                orientate(angle*-1)           	 

def sniffin():  
    global x
    global y
    global theta

    global x1
    global y1
    global x2
    global y2
    global x3
    global y3
    global x4
    global y4
    global x6
    global y6

    exis = [x1,x2,x3,x4,x6]
    yes = [y1,y2,y3,y4,y6]

    despejado = True

    i = 0
    while despejado and i < len(exis):
        distance = abs(math.sqrt(((exis[i]-x)**2)+((yes[i]-y)**2)))
        if distance < 1.4:
            obstacle_angle = math.atan2(yes[i], exis[i])
            if abs(obstacle_angle-theta) < 0.7:
                despejado = False
        i+=1
    return despejado


if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        cmd_vel_topic = '/turtle5/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        position_topic = "/turtle5/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, myCallback)

        position_topic1 = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic1, Pose, poseCallback1)

        position_topic2 = "/turtle2/pose"
        pose_subscriber = rospy.Subscriber(position_topic2, Pose, poseCallback2)

        position_topic3 = "/turtle3/pose"
        pose_subscriber = rospy.Subscriber(position_topic3, Pose, poseCallback3)

        position_topic4 = "/turtle4/pose"
        pose_subscriber = rospy.Subscriber(position_topic4, Pose, poseCallback4)

        position_topic6 = "/turtle6/pose"
        pose_subscriber = rospy.Subscriber(position_topic6, Pose, poseCallback6)


        time.sleep(2.0)
        orientate(2*math.pi/-2)
        for_the_horde(4,10)




    except rospy.ROSInterruptException:   	 
        pass


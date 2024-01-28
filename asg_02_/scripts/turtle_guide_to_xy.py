#!/usr/bin/env python
import rospy
from math import pi, sqrt, atan2, pow
import time
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


rospy.init_node('move_turtle_to_target')

x = 0
y = 0
heading_angle = 0

def initial_pose_callback(data):
    global x
    global y
    global x_found
    global heading_angle
    x = data.x
    y = data.y
    heading_angle = data.theta

def distance(goal_data):
    distance_pg = sqrt(pow((goal_data[0]-x), 2) + pow((goal_data[1]-y), 2))
    return distance_pg
    

def get_goal():
    #x_target = rospy.get_param('/target_x')
    #y_target = rospy.get_param('/target_y')
    #tolerance = rospy.get_param('/tolerance') 
    
    x_target = float(input("set x location:  "))
    y_target = float(input("set y location: "))
    tolerance = float(input("set tolerance: "))
    
    return [x_target, y_target, tolerance]

def pose_goal_angle(goal_data):
    goal_angle = (atan2(goal_data[1] - y, goal_data[0] - x) + 2*pi)%2*pi
    return goal_angle

def angular_vel(goal_data, kp=16):
    error_angle = pose_goal_angle(goal_data) - heading_angle
    if abs(error_angle)>pi/4:
        if error_angle>0:
            error_angle = error_angle - 2*pi
        else:
            error_angle = error_angle + 2*pi

    return kp * error_angle

def linear_vel(goal_data, kv=1.5):
    return kv * distance(goal_data)


rospy.Subscriber('/turtle1/pose', Pose, initial_pose_callback)
publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
msg = Twist()
goal_data = get_goal()
while distance(goal_data) >= float(goal_data[-1]):

    #Linear velocity control
    msg.linear.x = linear_vel(goal_data)
    msg.linear.y = 0 
    msg.linear.z = 0
    
    # Angular velocity control
    msg.angular.z=angular_vel(goal_data)
    msg.angular.y = 0
    msg.angular.x = 0
    
    publisher.publish(msg)

msg.linear.x = 0
msg.angular.z = 0
publisher.publish(msg)
rospy.spin()



        
    

#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from asg_01_.msg import Cylinder_asg_01_

from math import pi

radius = 0
radius_squared = 0
height = 0

radius_found = False
radius_squared_found = False
height_found = False


def radius_callback(data):
	global radius
	global radius_found
	radius = data.data
	radius_found = True
	

def radius_squared_callback(data):
	global radius_squared
	global radius_squared_found
	radius_squared = data.data
	radius_squared_found = True


def height_callback(data):
	global height
	global height_found
	height = data.data
	height_found = True


rospy.init_node("cylinder_calc")
rospy.Subscriber("/radius", Float64, radius_callback)
rospy.Subscriber("/radius_squared", Float64, radius_squared_callback)
rospy.Subscriber("/height", Float64, height_callback)
pub = rospy.Publisher("/cylinder", Cylinder_asg_01_, queue_size=10)

def calculate():
	if radius_found and radius_squared_found and height_found:
		msg = Cylinder_asg_01_()
		msg.volume = pi*radius_squared*height
		msg.surface_area = 2*pi*(radius*height+radius_squared)
		pub.publish(msg)
	

while not rospy.is_shutdown():
	calculate()
	rospy.sleep(0.1)

#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

from math import pi

density = 0
height = 0
radius_squared = 0

density_found = False
height_found = False
radius_squared_found = False

def density_callback(data):
	global density
	global density_found
	density = data.data
	density_found = True

def height_callback(data):
	global height
	global height_found
	height = data.data
	height_found = True

def radius_squared_callback(data):
	global radius_squared
	global radius_squared_found
	radius_squared = data.data
	radius_squared_found = True


	
rospy.init_node("cylinder_weight")
rospy.Subscriber("/density", Float64, density_callback)
rospy.Subscriber("/height", Float64, height_callback)
rospy.Subscriber("/radius_squared", Float64, radius_squared_callback)
pub = rospy.Publisher("/weight", Float64, queue_size=10)

def calculate():
	if density_found and  height_found and radius_squared_found:
		weight = pi*radius_squared*height*density*10
		pub.publish(weight)

while not rospy.is_shutdown():
	calculate()
	rospy.sleep(0.1)

#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
import json
import os
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from math import *
from tf.transformations import *


param = {}


with open(os.path.dirname(os.path.realpath(__file__)) + '/../yaml/dh.json', 'r') as file:
    param = json.loads(file.read())

alpha1=0
alpha2=0
#joints_pos1=0
#joints_pos2=0
#joints_pos3=0

def callback(data):
    calculatedJoints=JointState()
    global alpha1
    global alpha2 

    x=data.pose.position.x
    y=data.pose.position.y
    z=data.pose.position.z
    if x == 0 and y == 0:
        x=0.1
        y=0.1
    a1,d,alpha,th=param["i2"]
    a2,d,alpha,th=param["i3"]
    przesuw=0.3-z
        
    alpha22=-acos((x**2+y**2-a1**2-a2**2)/(2*a1*a2))
    alpha12=asin((a2*sin(alpha22))/(sqrt(x**2+y**2)))+atan2(y,x)
    
    alpha21=acos((x**2+y**2-a1**2-a2**2)/(2*a1*a2))
    alpha11=-asin((a2*sin(alpha21))/(sqrt(x**2+y**2)))+atan2(y,x)
    if fabs(alpha1-alpha11)>fabs(alpha1-alpha12) :
        alpha1=alpha12
        alpha2=alpha22
    else :
        alpha1=alpha11
        alpha2=alpha21  
 
    calculatedJoints.header = Header()
    calculatedJoints.header.stamp = rospy.Time.now()
    calculatedJoints.name = ['base_to_link1','link1_to_link2','link2_to_link3']
    calculatedJoints.position= [ alpha1 , alpha2, przesuw ]
    calculatedJoints.velocity= []
    calculatedJoints.effort= []
    pub.publish(calculatedJoints)
 

if __name__ == '__main__':
    pub = rospy.Publisher('/joint_states', JointState, queue_size = 100 )
    rospy.init_node('IKIN', anonymous=True)
    rospy.Subscriber("oint_pose", PoseStamped, callback)
    rospy.spin()
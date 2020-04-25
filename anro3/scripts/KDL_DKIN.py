#! /usr/bin/python

import rospy
import json
import os
import PyKDL
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker

xaxis= (1,0,0)
zaxis= (0,0,1)


def forward_kinematics(data):

#KDL 
    chain = PyKDL.Chain()
    joint_movement = [PyKDL.Joint.RotZ, PyKDL.Joint.RotZ,PyKDL.Joint.TransZ] 
    n_joints = 3
    for i in range(n_joints):
	a, d, alpha, th = params['i'+str(i+1)]
	alpha, a, d, th = float(alpha), float(a), float(d), float(th)
	frame = PyKDL.Frame()
	joint = PyKDL.Joint(joint_movement[i])
	frame = frame.DH(a, alpha, d, th)
	segment = PyKDL.Segment(joint, frame)
	chain.addSegment(segment)

    joints = PyKDL.JntArray(n_joints)
    for i in range(n_joints-1):
	    joints[i] = data.position[i]
    joints[2] = -data.position[2]
    fk=PyKDL.ChainFkSolverPos_recursive(chain)
    finalFrame=PyKDL.Frame()
    fk.JntToCart(joints,finalFrame)
    quaterions = finalFrame.M.GetQuaternion()

    pose = PoseStamped()
    pose.header.frame_id = 'base_link'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = finalFrame.p[0]
    pose.pose.position.y = finalFrame.p[1] 
    pose.pose.position.z = finalFrame.p[2]
    pose.pose.orientation.x = quaterions[3]
    pose.pose.orientation.y = quaterions[2]
    pose.pose.orientation.z = quaterions[1]
    pose.pose.orientation.w = quaterions[0]
    pub.publish(pose)

    marker = Marker()
    marker.header.frame_id = 'base_link'
    marker.type = marker.CUBE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1

    time = rospy.Duration()
    marker.lifetime = time
    marker.scale.x = 0.09
    marker.scale.y = 0.09
    marker.scale.z = 0.09
    marker.pose.position.x = finalFrame.p[0];
    marker.pose.position.y = finalFrame.p[1];
    marker.pose.position.z = finalFrame.p[2];
    marker.pose.orientation.x = quaterions[3];
    marker.pose.orientation.y = quaterions[2];
    marker.pose.orientation.z = quaterions[1];
    marker.pose.orientation.w = quaterions[0];
    marker.color.a = 0.7
    marker.color.r = 0.2
    marker.color.g = 0.8
    marker.color.b = 0.6
    marker_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node("KDL_KIN", anonymous=True)
    params = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../yaml/dh.json', 'r') as file:
        params = json.loads(file.read())


    pub = rospy.Publisher('kdl_pose', PoseStamped, queue_size=10)
    marker_pub = rospy.Publisher('kdl_visual', Marker, queue_size=100)

    rospy.Subscriber('joint_states', JointState, forward_kinematics)


    rospy.spin()

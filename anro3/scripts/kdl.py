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
print("heeejo")


def forward_kinematics(data):

    result_matrix=translation_matrix((0,0,0))

    a, d, alpha, th = params['i1']
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = translation_matrix((0, 0, d))
    rz = rotation_matrix(data.position[0], zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(alpha, xaxis)
    T1 = concatenate_matrices(rx, tx, rz, tz)

    tx = PyKDL.Vector(0, 0, 0)
    rx = PyKDL.Rotation.EulerZYX(0, 0, 0) 
    Tr = PyKDL.Frame(rx, tx)
    i=0
    a, d, alpha, th = params['i'+str(i+1)]
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = PyKDL.Vector(0, 0, d)
    rz = PyKDL.Rotation.EulerZYX(data.position[i], 0, 0)
    tx = PyKDL.Vector(a, 0, 0)   
    rx = PyKDL.Rotation.EulerZYX(0, 0, alpha) 
    Tx = PyKDL.Frame(rx, tx)
    Tz = PyKDL.Frame(rz, tz)
    Tr *= Tx * Tz
    import pdb;pdb.set_trace()
    THD = PyKDL.HD(a, alpha, d,data.position[i]) 

    a, d, alpha, th = params['i2']
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = translation_matrix((0, 0, d))
    rz = rotation_matrix(data.position[1], zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(alpha, xaxis)
    T2 = concatenate_matrices(rx, tx, rz, tz)

    import pdb;pdb.set_trace()
    a, d, alpha, th = params['i3']
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = translation_matrix((0, 0, data.position[2]))
    rz = rotation_matrix(th, zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(alpha, xaxis)
    T3 = concatenate_matrices(rx, tx, rz, tz)

    result_matrix = concatenate_matrices(T1, T2, T3)
    x, y, z = translation_from_matrix(result_matrix)

    import pdb;pdb.set_trace()
    qx, qy, qz, qw = quaternion_from_matrix(result_matrix)

    pose = PoseStamped()
    pose.header.frame_id = 'base_link'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    pose.pose.orientation.w = qw
    pub.publish(pose)

    marker = Marker()
    marker.header.frame_id = 'base_link'
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1

    time = rospy.Duration()
    marker.lifetime = time
    marker.scale.x = 0.09
    marker.scale.y = 0.09
    marker.scale.z = 0.09
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.pose.orientation.x = qx;
    marker.pose.orientation.y = qy;
    marker.pose.orientation.z = qz;
    marker.pose.orientation.w = qw;
    marker.color.a = 0.7
    marker.color.r = 0.5
    marker.color.g = 0.0
    marker.color.b = 0.6
    marker_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node("NONKDL_KIN", anonymous=True)
    params = {}
    print os.path.dirname(os.path.realpath(__file__))
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../yaml/dh.json', 'r') as file:
        params = json.loads(file.read())


    pub = rospy.Publisher('nkdl_pose', PoseStamped, queue_size=10)
    marker_pub = rospy.Publisher('nkdl_visual', Marker, queue_size=100)

    rospy.Subscriber('joint_states', JointState, forward_kinematics)


    rospy.spin()

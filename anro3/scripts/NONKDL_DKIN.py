#! /usr/bin/python

import json
import rospy
import os
import rospkg
from tf.transformations import *
from sensor_msgs.msg import *
from geometry_msgs.msg import *
xaxis=(1,0,0)
zaxis=(0,0,1)
param = {}
rospack = rospkg.RosPack()
PACKAGE_PATH = rospack.get_path('anro3')

def loadFromFile():
    global param
    results = ''
    with open(os.path.join(PACKAGE_PATH, 'yaml', 'dh.json'), 'r') as file:
        param = json.loads(file.read())    
    rospy.loginfo(param)
    rospy.loginfo("hejjjol")

def callback(data):

    publisher=rospy.Publisher('pose/update',PoseStamped,queue_size=100)
    pose=PoseStamped()
    result_matrix=translation_matrix((0,0,0))

    for i in range (1,3):
        a,d,alpha,th = param["i"+str(i)]
        a=float(a)
        d=float(d)
        alpha=float(alpha)
        th=float(th)

        tz = translation_matrix((0, 0, d))  
        rz = rotation_matrix(data.position[i-1], zaxis)     
        tx = translation_matrix((a, 0, 0))  
        rx = rotation_matrix(alpha, xaxis)  

        matrix = concatenate_matrices(tz, rz, tx, rx)  
        result_matrix= concatenate_matrices(result_matrix,matrix)

    x, y, z = translation_from_matrix(result_matrix)

    pose.header.frame_id = "base_link";
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x=x
    pose.pose.position.y=y
    pose.pose.position.z=z+d

    x_orient,y_orient,z_orient,w_orient=quaternion_from_matrix(result_matrix)
    pose.pose.orientation.x=x_orient
    pose.pose.orientation.y=y_orient
    pose.pose.orientation.z=z_orient
    pose.pose.orientation.w=w_orient
    rospy.loginfo("heeeeeja")

    publisher.publish(pose)


def listener():

    rospy.loginfo("listener")
    rospy.Subscriber("joint_states",JointState, callback)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('NONKDL',anonymous=True)
    loadFromFile()
    listener()

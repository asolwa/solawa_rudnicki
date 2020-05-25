#! /usr/bin/env python

import math
from math import *
import rospy
from anro4.srv import Oint
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from tf.transformations import quaternion_from_euler

f=30
new_pos=[0,0,0]
new_orient = [0,0,0]
start_pos=[0,0,0]
start_orient=[0,0,0]
actual_pos=[0,0,0]
actual_orient=[0,0,0]
path = Path()

def interpolation_function(data):

    new_pos = data.pos
    new_orient = data.orient
    rate = rospy.Rate(f)

    frames_num = int(math.ceil(data.time*f))
    pose = PoseStamped()
    pose.header.frame_id = "base_link"
    pose.header.stamp = rospy.Time.now()

    for actual_frame in range(0,frames_num+1):
        for i in range(3):
            actual_pos[i]=linear_interpolation(
                    start_pos[i], new_pos[i], frames_num, actual_frame)
            actual_orient[i]=linear_interpolation(
                    start_orient[i], new_orient[i], frames_num, actual_frame)

        quaterion = quaternion_from_euler(*actual_orient)
        pose.pose.position.x = actual_pos[0]
        pose.pose.position.y = actual_pos[1]
        pose.pose.position.z = actual_pos[2]
        
        pose.pose.orientation.x = quaterion[0]
        pose.pose.orientation.y = quaterion[1]
        pose.pose.orientation.z = quaterion[2]
        pose.pose.orientation.w = 1

        path.header = pose.header
        path.poses.append(pose)
        path_pub.publish(path)
        pub.publish(pose)
        rate.sleep()

    start_pos[:] = actual_pos[:]
    start_orient[:] = actual_orient[:]

    return {"status": True, "msg": "Interpolation finished successfully"}


def linear_interpolation(start,end,time,actual_time):
    return start+(float(end-start)/time)*actual_time

if __name__ == '__main__':

    print("File works")
    rospy.init_node('interpol_srv', anonymous=True)
    pub = rospy.Publisher('oint_pose', PoseStamped, queue_size=10)
    path_pub = rospy.Publisher('pathing', Path, queue_size=10)
    s=rospy.Service('oint_control_srv',Oint,interpolation_function)

    rospy.spin()

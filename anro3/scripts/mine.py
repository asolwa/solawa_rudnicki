#! /usr/bin/python
import json
import rospy
import os
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker
xaxis=(1,0,0)
zaxis=(0,0,1)


def loadFromFile():
    results = ''
    print os.path.dirname(os.path.realpath(__file__))

    with open(os.path.dirname(os.path.realpath(__file__))+ '/../yaml/dh.json','r') as file:
        param=json.loads(file.read())
def callback(data):

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

        matrix[i] = concatenate_matrices(rx,rz,tx,tz)  


    result_matrix= concatenate_matrices(matrix[1],matrix[2],matrix[3])
    x,y,z=translation_from_matrix(result_matrix)
    x_orient,y_orient,z_orient,w_orient=quaternion_from_matrix(result_matrix)


    pose.header.frame_id = "base_link"
    pose.header.stamp = ros.Time.now()
    pose.pose.position.x=x
    pose.pose.position.y=y
    pose.pose.position.z=z
    pose.pose.orientation.x=x_orient
    pose.pose.orientation.y=y_orient
    pose.pose.orientation.z=z_orient
    pose.pose.orientation.w=w_orient
    publisher.publish(pose)

    # marker=Marker()
    # marker.header.frame_id="base_link"
    # marker.type=marker.SPHERE
    # marker.action=marker.ADD
    # marker.pose.orientatation.w=1

    # time= rospy.Duration()
    # marker.lifetime=time
    # marker.scale.x=0.1
    # marker.scale.y=0.1
    # marker.scale.z=0.1
    # marker.pose.position.x=x
    # marker.pose.position.x=y
    # marker.pose.position.x=z
    # marker.pose.orientation.x=x_orient
    # marker.pose.orientation.y=y_orient
    # marker.pose.orientation.z=z_orient
    # marker.pose.orientation.w=w_orient  
    # marker.color.a=0.6
    # marker.color.r=0.4
    # marker.color.g=0.4
    # marker.color.b=0
    # m_publisher.publish(marker)



if __name__ == '__main__':
    rospy.init_node('NONKDL',anonymous=True)

    publisher=rospy.Publisher('poseStamped',PoseStamped,queue_size=100)
    # m_publisher=rospy.Publisher('NOKDLvisual',Marker,queue_size=100)
    rospy.Subscriber("joint_states",JointState,callback)
    param = {}
    rospy.spin()

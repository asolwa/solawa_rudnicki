#! /usr/bin/python

import rospy
from anro4.srv import interpol
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math

f=50
actual_pos=[0,0,0]

def interpolation_function(data):

    if data.time<=0:
        return False
    if -1.57 >= data.j1 or data.j1>=1.57:
        return False
    if -1.57 >= data.j2 or data.j2>=1.57:
        return False
    if  data.j3<=0.05 or data.j3>=0.16:
        return False

    actual_pos=ropsy.wait_for_message('joint_states',JointState,timeout=10).position
    new_pos=[data.j1,data.j2,data.j3]
    rate=rospy.Rate(f)
    j1=actual_pos[0]
    j2=actual_pos[1]
    j3=actual_pos[2]

    frames_num= int(math.ceil(data.t*f))
    actual_time=0

    for i in range(0,frames_num+1):
        calculatedJointState=JointState()
        calculatedJointState.header=Header()
        calculatedJointState.header.stamp=rospy.Time.now()
        calculatedJointState.name=['base_to_link1','link1_to_link2','link2_to_link3']

        j1=linear_interpolation(actual_pos[0],_new_pos[0],data.time,actual_time)
        j2=linear_interpolation(actual_pos[1],_new_pos[1],data.time,actual_time)
        j3=linear_interpolation(actual_pos[2],_new_pos[2],data.time,actual_time)

        calculatedJointState.postion=[j1,j2,j3]
        calculatedJointState.velocity= []
        calculatedJointState.effort= []
        pub.publish(calculatedJointState)
        actual_time+=1
        rate.sleep()


    return True




def linear_interpolation(start,end,time,actual_time):
    return start+(float(end-start)/time)*actual_time


if __name__ == '__main__':

    rospy.init_node('interpol_srv', anonymous=True)
    pub = rospy.Publisher('interpolation', JointState, queue_size=10)
    s=rospy.Service('interpol',interpol,interpolation_function)


    rospy.spin()

#! /usr/bin/env python

import rospy
from anro4.srv import Interpol
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math

f=10
actual_pos=[0,0,0.05]
new_pos=[0,0,0]

def interpolation_function(data):
    if data.time<=0:
        return {"status": False, "msg": "Wrong time value"}
    if -1.57 >= data.j1 or data.j1>=1.57:
        return {"status": False, "msg": "Wrong 1rd joint value"}
    if -1.57 >= data.j2 or data.j2>=1.57:
        return {"status": False, "msg": "Wrong 2rd joint value"}
    if  data.j3<=0.05 or data.j3>=0.16:
        return {"status": False, "msg": "Wrong 3rd joint value"}
    if  data.type not in msg_to_function.keys():
        return {"status": False, "msg": "Wrong interpolation type"}

    calculatedJointState=JointState()
    calculatedJointState.header=Header()
    calculatedJointState.name=['base_to_link1','link1_to_link2','link2_to_link3']
    new_pos=[data.j1,data.j2,data.j3]
    #calculatedJointState.position=[0,0,0.12]
    #calculatedJointState.velocity=[]
    #calculatedJointState.effort=[]
    #pub.publish(calculatedJointState)
    rate=rospy.Rate(f)

    interpol_function = msg_to_function["spline"]

    frames_num= int(math.ceil(data.time*f))

    for actual_frame in range(0,frames_num+1):
        j1=interpol_function(actual_pos[0],new_pos[0],frames_num,actual_frame)
        j2=interpol_function(actual_pos[1],new_pos[1],frames_num,actual_frame)
        j3=interpol_function(actual_pos[2],new_pos[2],frames_num,actual_frame)

        calculatedJointState.header.stamp=rospy.Time.now()
        calculatedJointState.position=[j1,j2,j3]
        calculatedJointState.velocity= []
        calculatedJointState.effort= []
        pub.publish(calculatedJointState)
        rate.sleep()
    actual_pos[0]=j1
    actual_pos[1]=j2
    actual_pos[2]=j3
    return {"status": True, "msg": "Interpolation finished successfully"}


def linear_interpolation(start,end,time,actual_time):
    return start+(float(end-start)/time)*actual_time

def spline_interpolation(start,end,end_time,actual_time):
    t = actual_time / float(end_time)
    s1 = (1 - t) * start    
    s2 = t * end
    s3 = t * (1 - t) * ((1 - t) * (start - end) + t * (end - start))
    return s1 + s2 + s3

msg_to_function = {
    "linear": linear_interpolation,
    "spline": spline_interpolation,
}

if __name__ == '__main__':
    rospy.init_node('interpol_srv', anonymous=True)
    pub = rospy.Publisher('interpolation', JointState, queue_size=10)
    s=rospy.Service('Interpol_control',Interpol,interpolation_function)


    rospy.spin()

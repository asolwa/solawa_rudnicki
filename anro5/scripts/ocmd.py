#!/usr/bin/env python


import sys
import rospy
from math import cos, sin
from anro4.srv import Oint

def interpolate(position, orientation, t):
    rospy.wait_for_service('oint_control_srv')
    try:
        oint_srv = rospy.ServiceProxy('oint_control_srv', Oint)
        resp = oint_srv(position, orientation, t)
        print(resp)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def rectangle(a, b, t):
    rospy.wait_for_service('oint_control_srv')
    orientation = [0,0,0]
    z = 0.1
    try:
        oint_srv = rospy.ServiceProxy('oint_control_srv', Oint)
        for _ in range (4):
            resp = oint_srv([a, b, z], orientation, t)
            resp = oint_srv([-a, b, z], orientation, t)
            resp = oint_srv([-a, -b, z], orientation, t)
            resp = oint_srv([a, -b, z], orientation, t)
        print(resp)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def elipse(ox, oy):
    rospy.wait_for_service('oint_control_srv')
    orientation = [0,0,0]
    z = 0.1
    try:
        oint_srv = rospy.ServiceProxy('oint_control_srv', Oint)
        t = 0
        while True:
            resp = oint_srv([ox * cos(t), oy * sin(t), z], orientation, 1.0/30)
            t += 0.1
        print(resp)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def usage():
    return "%s [x y z alpha beta gamma t]"%sys.argv[0]

if __name__ == "__main__":
    position = []
    orientation = []
    if len(sys.argv) == 8:
        position.append(float(sys.argv[1]))
        position.append(float(sys.argv[2]))
        position.append(float(sys.argv[3]))
        orientation.append(float(sys.argv[4]))
        orientation.append(float(sys.argv[5]))
        orientation.append(float(sys.argv[6]))
        t  = float(sys.argv[7])
        interpolate(position, orientation, t)
    elif len(sys.argv) == 4:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        t = float(sys.argv[3])
        rectangle(a, b, t)
    elif len(sys.argv) == 3:
        ox = float(sys.argv[1])
        oy = float(sys.argv[2])
        elipse(ox, oy)
    else:
        print usage()
        sys.exit(1)

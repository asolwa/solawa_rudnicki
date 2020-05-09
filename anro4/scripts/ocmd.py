#!/usr/bin/env python

import sys
import rospy
from anro4.srv import Oint

def interpolate(position, orientation, t):
    rospy.wait_for_service('oint_control_srv')
    try:
        oint_srv = rospy.ServiceProxy('oint_control_srv', Oint)
        resp = oint_srv(position, orientation, t)
        print(resp)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y z alpha beta gamma]"%sys.argv[0]

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
    else:
        print usage()
        sys.exit(1)
    interpolate(position, orientation, t)

#!/usr/bin/env python

import sys
import rospy
from anro4.srv import interpol

def interpolate(j1, j2, j3, t):
    rospy.wait_for_service('interpol')
    try:
        add_two_ints = rospy.ServiceProxy('interpol', interpol)
        resp = add_two_ints(j1, j2, j3, t)
        print(resp)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:
        j1 = float(sys.argv[1])
        j2 = float(sys.argv[2])
        j3 = float(sys.argv[3])
        t  = float(sys.argv[4])
    else:
        print usage()
        sys.exit(1)
    interpolate(j1, j2, j3, t)

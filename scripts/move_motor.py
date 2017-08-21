#!/usr/bin/env python

import roslib;

roslib.load_manifest("dynamixel_hr_ros")
import rospy
from std_msgs.msg import *
import json

from dynamixel_hr_ros.msg import *

from dxl import *
import logging
import time

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    rospy.init_node("dxl_replay")
    enabler = rospy.Publisher("/dxl/enable", Bool)
    commander = rospy.Publisher("/dxl/command_position", CommandPosition)
    time.sleep(1)
    enabler.publish(True)
    time.sleep(1)

    print "Replaying"

    command = CommandPosition()
    command.id = [1, 2, 3]
    command.angle = [0.1, 0.1, 0.1]
    command.speed = [5, 5, 1]
    commander.publish(command)
    print command
    time.sleep(1)
    enabler.publish(False)


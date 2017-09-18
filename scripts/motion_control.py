#!/usr/bin/env python

import roslib; roslib.load_manifest("dynamixel_hr_ros")
import rospy
from std_msgs.msg import *
import json
from dynamixel_hr_ros.msg import *
from dxl import *
import logging
import time
import pygame
import numpy as np
import math
import csv
import itertools

from threading import Timer

logging.basicConfig(level=logging.DEBUG)


class MotionControl:

    def __init__(self):
        self.skeleton_angles = np.zeros([6])
        #self.motor_list = [1,2,5,7,6,8]
        self.motor_list = [1]

    def start(self):
        # init a listener to kinect angles
        rospy.init_node('motion_control')
        rospy.Subscriber("skeleton_angles", String, self.callback)
        enabler = rospy.Publisher("/dxl/enable", Bool)
        self.commander = rospy.Publisher("/dxl/command_position", CommandPosition)
        time.sleep(1)
        enabler.publish(True)
        time.sleep(1)
        rospy.spin()

    def callback(self, data):
        self.skeleton_angles = np.array([float(x) for x in data.data.split(',')])
        self.move_motors(self.skeleton_angles)
        print self.skeleton_angles[0] * 180 / np.pi

    def move_motors(self, angles):
        command = CommandPosition()
        command.id = self.motor_list
        command.angle = angles
        command.speed = [3] * len(self.motor_list)
        #self.commander.publish(command)


if __name__=="__main__":

    motion_control = MotionControl()
    motion_control.start()

    logging.basicConfig(level=logging.DEBUG)

    print "Listening for commands"



    command=CommandPosition()
    command.id= motor_list
    command.angle= motions[i, :]
    command.speed=[3]*len(motor_list)
    motion_control.commander.publish(command)


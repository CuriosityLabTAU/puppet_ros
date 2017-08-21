#!/usr/bin/env python

import roslib; roslib.load_manifest("dynamixel_hr_ros")
import rospy
from std_msgs.msg import *
import json

from dynamixel_hr_ros.msg import *

from dxl import *
import logging
import time
import numpy as np
import pygame

logging.basicConfig(level=logging.DEBUG)





if __name__=="__main__":
        
        logging.basicConfig(level=logging.DEBUG)

        file = 'eency.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        
        rospy.init_node("dxl_replay")
        enabler=rospy.Publisher("/dxl/enable",Bool)
        commander=rospy.Publisher("/dxl/command_position",CommandPosition)
        time.sleep(1)
        enabler.publish(True)
        time.sleep(1)

        print "Replaying"
        
        f=open("hands_recorded_1","r")
        frames=json.loads(f.read())
        f.close()

        sleeptime = 40.0/1253

        pygame.mixer.music.play()


        for f in frames:
            command=CommandPosition()
            command.id=f[0]
            command.angle=f[1]
            command.speed=[2]*len(f[0])
            commander.publish(command)
            time.sleep(sleeptime)
        enabler.publish(False)
        #~ enabler.publish(False)
        

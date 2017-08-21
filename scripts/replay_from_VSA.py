#!/usr/bin/env python

import roslib; roslib.load_manifest("dynamixel_hr_ros")
import rospy
from std_msgs.msg import *
import json

from dynamixel_hr_ros.msg import *

from dxl import *
import logging
import time
import csv
import math
import pygame



logging.basicConfig(level=logging.DEBUG)





if __name__=="__main__":

        file = 'Talking Mother Goose_2.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)

        logging.basicConfig(level=logging.DEBUG)
        
        
        rospy.init_node("dxl_replay")
        enabler=rospy.Publisher("/dxl/enable",Bool)
        commander=rospy.Publisher("/dxl/command_position",CommandPosition)
        time.sleep(1)
        enabler.publish(True)
        time.sleep(1)

        f = open('export_9.csv')
        csv_f = csv.reader(f)
        mouth = []



        for row in csv_f:
            a = (float(row[1])*(220.0/254)+620)*(math.pi/1023)
            print a
            mouth.append(a)

        print mouth

        print "Replaying"
        
        f=open("recorded","r")        
        frames=json.loads(f.read())
        #print frames
        f.close()

        '''     
        for f in frames:
            command=CommandPosition()
            command.id=f[0]
            command.angle=f[1]
            command.speed=[1]*len(f[0])
            commander.publish(command)
            print [f[0], ', ', f[1], ', ', [1]*len(f[0])]
            time.sleep(0.1)
       '''
        pygame.mixer.music.play()
        for b in mouth:
            command=CommandPosition()
            command.id=[4]
            command.angle=[b]
            command.speed=[2.6]
            commander.publish(command)

            time.sleep(0.033)

        #~ enabler.publish(False)
        

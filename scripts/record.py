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

logging.basicConfig(level=logging.DEBUG)




frames=[]
hands_times =[]

def add_frame(msg):
    frames.append((msg.id,msg.angle))
    hands_times.append(time.time())


if __name__=="__main__":
        
        logging.basicConfig(level=logging.DEBUG)
        
        file = 'eency.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)

        rospy.init_node("dxl_record")
        logging.basicConfig(level=logging.DEBUG)
        enabler=rospy.Publisher("/dxl/enable",Bool)        
        time.sleep(1)
        enabler.publish(False)
        time.sleep(1)
        start = time.time()
        rospy.Subscriber("/dxl/chain_state",ChainState,add_frame)

        pygame.mixer.music.play()

        print "Recording"
        while not rospy.is_shutdown() and (time.time()-start)<40:
                time.sleep(0.1)
        print len(frames)

        f=open("hands_recorded_1","w")
        f.write(json.dumps(frames))
        f.close()

        g=open("hand_times_1","w")
        g.write(json.dumps(hands_times))
        g.close
            
            
        
        

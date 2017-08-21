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


def start_t0(time_seq):
    t0 = time_seq[0]
    for t in range(0,len(time_seq)):
        time_seq[t] = time_seq[t]- t0
    return time_seq


def add_motions(frames,motions,frame_duration,motor_list,motions_x,dt_x, times):
    for i in range(0, frames):
        for j in range(0, len(motor_list)):
            rt = (frame_duration * i) / dt_x - 1
            Rt = int(np.floor(rt))
            rT = Rt + 1 #int(np.ceil(rt))
            if rt < 0:
                motions[i, motor_list[j] - 1] = motions_x[0][1][j]
            elif rT*dt_x > times[-1]:
                motions[i, motor_list[j] - 1] = motions_x[-1][1][j]
            elif Rt >= len(motions_x)-1:
                print i, j, Rt, rt, len(motions_x)
                motions[i, motor_list[j] - 1] = motions_x[Rt-1][1][j]
            else:
                motions[i, motor_list[j] - 1] = motions_x[Rt][1][j] + (motions_x[rT][1][j] -
                                                                       motions_x[Rt][1][j]) * (rt - Rt)
    return motions


def add_motions_VSA(frames,motions,frame_duration,motor,motions_x,dt_x,times):
    for i in range(0, frames):
        rt = (frame_duration * i) / dt_x - 1
        Rt = int(np.floor(rt))
        rT = Rt + 1 #int(np.ceil(rt))
        if rt < 0:
            motions[i, motor - 1] = motions_x[0]
        elif rT*dt_x > times[-1]:
            motions[i, motor - 1] = motions_x[-1]
        elif Rt >= len(motions_x)-1:
            motions[i, motor - 1] = motions_x[Rt-1]
        else:
            motions[i, motor - 1] = motions_x[Rt] + (motions_x[rT] - motions_x[Rt]) * (rt - Rt)
    return motions

def import_from_VSA(csv_file):
    mouth = []
    f = open(csv_file)
    csv_f = csv.reader(f)
    for row in csv_f:
        a = (float(row[1]) * (160.0 / 254) + 645) * (math.pi / 1023)
        mouth.append(a)
    return mouth


if __name__=="__main__":


    fps = 30 # frequency of playback
    total_duration = 40 #total duration of sequence in seconds
    frames = fps * total_duration
    frame_duration = 1.0 / fps
    number_of_motors = 8
    motions = np.zeros((frames, number_of_motors))
    VSA_fps = 30
    mouth_delay = 93

    m1 = open("hands_recorded", "r")
    motions_1 = json.loads(m1.read())
    motor_list_1 = motions_1[1][0]


    t1 = open("hand_times", "r")
    times_1 = json.loads(t1.read())
    times_1 = start_t0(times_1)
    dt_1 = times_1[1] - times_1[0]

    m2 = open("hands_recorded_1", "r")
    motions_2 = json.loads(m2.read())
    motor_list_2 = motions_2[0][0]

    t2 = open("hand_times_1", "r")
    times_2 = json.loads(t2.read())
    times_2 = start_t0(times_2)
    dt_2 = times_2[1] - times_2[0]

    motions_3 = import_from_VSA('eency_me_1.csv')
    temp = [motions_3[1]]*mouth_delay
    motions_3 = temp + motions_3
    dt_3 = 1.0 / VSA_fps
    motor_VSA = 4
    times_3 = np.linspace(0,dt_3*len(motions_3),51)

    motions = add_motions(frames, motions, frame_duration, motor_list_1, motions_1, dt_1, times_1)
    motions = add_motions(frames, motions, frame_duration, motor_list_2, motions_2, dt_2, times_2)
    motions = add_motions_VSA(frames, motions, frame_duration, motor_VSA, motions_3,dt_3, times_3)
    print motions_3
    print motions[:,3]
    print motions.shape
    file = 'eency.mp3'
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

    print "Replaying"

    motor_list = [1,2,3,4,5,6,7,8]

    pygame.mixer.music.play()

    np.savetxt('np.csv', motions, fmt='%.2f', delimiter=',')

    for i in range(0,frames):
        command=CommandPosition()
        command.id= motor_list
        command.angle= motions[i, :]
        command.speed=[3]*len(motor_list)
        commander.publish(command)
        time.sleep(frame_duration)




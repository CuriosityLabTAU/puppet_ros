import json
import numpy as np
import math
import csv

fps = 5 # frequency of playback
total_duration = 20 #total duration of sequence in seconds
frames = fps * total_duration
frame_duration = 1.0 / fps
number_of_motors = 8
motions = np.zeros((frames, number_of_motors))
VSA_fps = 30


def start_t0(time_seq):
    t0 = time_seq[0]
    for t in range(0,len(time_seq)):
        time_seq[t] = time_seq[t]- t0
    return time_seq

def add_motions(frames,motions,frame_duration,motor_list,motions_x,dt_x):
    for i in range(0, frames):
        motions[i][0] = i * frame_duration
        for j in range(0, len(motor_list)):
            rt = (frame_duration * i) / dt_x - 1
            Rt = int(np.floor(rt))
            rT = int(np.ceil(rt))
            if rt < 0:
                motions[i, motor_list[j] - 1] = motions_x[0][1][j]
            elif rT > times_1[-1]:
                motions[i, motor_list[j] - 1] = motions_x[-1][1][j]
            else:
                motions[i, motor_list[j] - 1] = motions_x[Rt][1][j] + (motions_x[rT][1][j] -
                                                                       motions_x[Rt][1][j]) * (rT - Rt)
    return motions

def add_motions_VSA(frames,motions,frame_duration,motor,motions_x,dt_x):
    for i in range(0, frames):
        motions[i][0] = i * frame_duration
        rt = (frame_duration * i) / dt_x - 1
        Rt = int(np.floor(rt))
        rT = int(np.ceil(rt))
        if rt < 0:
            motions[i, motor - 1] = motions_x[0]
        elif rT > times_1[-1]:
            motions[i, motor - 1] = motions_x[-1]
        else:
            motions[i, motor - 1] = motions_x[Rt] + (motions_x[rT] -motions_x[Rt]) * (rT - Rt)
    return motions

def import_from_VSA(csv_file):
    mouth = []
    f = open(csv_file)
    csv_f = csv.reader(f)
    for row in csv_f:
        a = (float(row[1]) * (220.0 / 254) + 620) * (math.pi / 1023)
        mouth.append(a)
    return mouth

m1 = open("hands_recorded","r")
motions_1 = json.loads(m1.read())
motor_list_1 =  motions_1[1][0]

t1 = open("hand_times","r")
times_1 = json.loads(t1.read())
times_1 = start_t0(times_1)
dt_1 = times_1[1] - times_1[0]

m2 = open("hands_recorded_1","r")
motions_2 = json.loads(m2.read())
motor_list_2 =  motions_2[0][0]

t2 = open("hand_times_1","r")
times_2 = json.loads(t2.read())
times_2 = start_t0(times_2)
dt_2 = times_2[1] - times_2[0]

motions_3 = import_from_VSA('eency_me_1.csv')
dt_3 = 1.0 / VSA_fps
motor_VSA = 4

motions = add_motions(frames,motions,frame_duration,motor_list_1,motions_1,dt_1)
motions = add_motions(frames,motions,frame_duration,motor_list_2,motions_2,dt_2)
motions = add_motions_VSA(frames,motions,frame_duration,motor_VSA,motions_3,dt_3)










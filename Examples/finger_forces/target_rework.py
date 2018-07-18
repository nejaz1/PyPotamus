import numpy as np
import csv
import random

num_sampl = 8
angle_inc = 360/num_sampl
angles = []
forces = [5,2.5]
radii = [0.8,0.4]
target_space = []
digits = [1,2,3,4,5]
Hand = 2
ens_perc = 0.8


for i in range(num_sampl):
    angle = (i*angle_inc)
    rad = (angle * (np.pi/180))
    angles.append(rad)

for j in range(len(radii)):
    target_radi = np.array([radii[j],0])
    force = forces[j]
    for i in angles:
        RM = np.array([[np.cos(i), -np.sin(i)], [np.sin(i), np.cos(i)]])
        new = np.matmul(RM, target_radi)
        new = new.tolist()
        for i in range(2):
            new[i] = round(new[i], 2)
        new.append(force)
        target_space.append(new)

all_trials = []
for i in digits:
    for j in target_space:
        all_trials.append([i,j[0],j[1],j[2]])



random.shuffle(all_trials)


with open('test_2.tgt', 'w', newline='') as tgt:
    headernames = ['TN', 'Hand', 'Digit', 'TargetX', 'TargetY', 'Force', 'EnsPercent']
    writer = csv.writer(tgt, delimiter = '\t')

    writer.writerow(headernames)

    for i in range(len(all_trials)):
        row = []
        row.append(i+1)
        row.append(Hand)
        target = all_trials[i]
        row.append(target[0])
        row.append(target[1])
        row.append(target[2])
        row.append(target[3])
        row.append(ens_perc)

        writer.writerow(row)
        
    
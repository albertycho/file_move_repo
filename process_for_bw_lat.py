#!/usr/bin/env python

import os
import sys
import csv
import math
import statistics
import numpy as np
from os.path import exists


csf = open('collected_stats.csv','w')
csf.write('cores,MBW,AVGLAT,LAT90,IPC,\n')
for i in range(16):
    MBW='0'
    AVGLAT='0'
    LAT90='0'
    IPC='0'
    dname = str(i+1)+'C'
    if(i<10):
        dname='0'+dname
    print(dname)
    if exists(dname):
        os.chdir(dname)
        os.system('rm stat_summary.txt')
        os.system('python3 /home/azureuser/CXL_WD/scripts/qpp_cxl.py')
        if exists('stat_summary.txt'):
            stat_file = open('stat_summary.txt','r')
            line = stat_file.readline()
            while line:
                if('avgbw:' in line):
                    MBW = (line.split('avgbw:')[1]).split('\n')[0]
                if('all_lat_avg' in line):
                    AVGLAT = line.split(',')[1]
                if('p90' in line):
                    LAT90 = line.split(',')[1]
                if('IPC' in line):
                    IPC = (line.split(':')[1]).split(',')[0]
                line=stat_file.readline()
        os.chdir('..')
    csf.write(str(i+1)+','+MBW+','+AVGLAT+','+LAT90+','+IPC+',\n')



csf.close()

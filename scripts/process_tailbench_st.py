#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from os.path import exists




cumulative_st = []

if exists('tailbench_st.txt'):
    ftbst = open('tailbench_st.txt','r')
else:
    print("tailbench_st file not found")
    exit(-1)

line = ftbst.readline()
while line:
    if not ('core' in line):
        st=int(line.split(',')[0])
        st_in_us=st/2000
        cumulative_st.append(st_in_us)
    
    line=ftbst.readline()

f_st_summary = open('tailbench_st_summary.txt','w')
avgst = str(sum(cumulative_st)/len(cumulative_st))
p90 = str(np.percentile(cumulative_st, 90))
p95 = str(np.percentile(cumulative_st, 95))
p99 = str(np.percentile(cumulative_st, 99))
f_st_summary.write('avg_st, '+avgst +',\n')
f_st_summary.write('p90 , '+p90 +',\n')
f_st_summary.write('p95 , '+p95 +',\n')
f_st_summary.write('p99 , '+p99 +',\n')

f_st_summary.close()

os.system("cat tailbench_st_summary.txt");

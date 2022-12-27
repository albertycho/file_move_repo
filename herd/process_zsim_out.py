#!/usr/bin/env python3

import os
import sys
import csv
import math
#import statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt


os.system('cp zsim.out zsim2.out')
f1 = open("zsim.out",'r')
f2 = open("zsim2.out",'r')
f3 = open("zsim_final.out",'w')
f4 = open("same_lines_zsim.out",'w')

line1 = f1.readline();
line2 = f2.readline();

while not ('root:' in line1):
    line1 = f1.readline();

while not ('root:' in line2):
    line2 = f2.readline();

line2 = f2.readline();
while not ('root:' in line2):
    line2 = f2.readline();
#### bring line2 to second dump

f3.write(line2)
f4.write(line2)
line1=f1.readline()
line2=f2.readline()

while ((line2) and (not ('root:' in line2))):
    if(line1 == line2):
        f3.write(line2)
        f4.write(line2)
    else:
        tmp1 = line1.split(': ')
        tmp2 = line2.split(': ')
        f3.write(tmp2[0]+': ')
        n1s = tmp1[1].split(' #')
        n2s = tmp2[1].split(' #')
        n1 = int(n1s[0])
        n2 = int(n2s[0])
        n3 = n2-n1
        f3.write(str(n3))
        if len(n1s)>1:
            f3.write(' #'+n1s[1])
        else:
            f3.write('\n')

    line1 = f1.readline()
    line2 = f2.readline()

f1.close()
f2.close()
f3.close()
f4.close()

        

#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

#script_dir = '/shared/acho44/CXL_WD/'
script_dir = '~/CXL_WD/scripts/'

cwd = os.getcwd()

#os.system('cp '+script_dir+'process_zsim_out.py .') 
#os.system('cp '+script_dir+'get_zsimout_stats_dramsim.py .')
#os.system('cp '+script_dir+'get_avg_mbw_dramsim_trim.py .')
#os.system('cp '+script_dir+'qpp_cxl.py .')

appNamesFull=['moses', 'imgdnn', 'cc', 'bc', 'lbm', 'masstree', 'pr', 'cactuBSSN', 'tc', 'parest', 'sphinx', 'bfs', 'omnetpp', 'wrf', 'xz', 'mica', 'cam4', 'monetdb', 'mcf', 'sssp', 'xapian', 'leela', 'nab', 'povray', 'deepsjeng', 'perlbench']

appNames=['mose', 'imgd', 'cc', 'bc', 'lbm', 'masst', 'pr', 'cactB', 'tc', 'parst', 'sphx', 'bfs', 'omntp', 'wrf', 'xz', 'mica', 'cam4', 'mDB', 'mcf', 'sssp', 'xapn', 'leela', 'nab', 'povray', 'deepsj', 'perlbc']

d2X_ipcs=[0]*len(appNamesFull)
d8X_ipcs=[0]*len(appNamesFull)
d2X_mbws=[0]*len(appNamesFull)
d8X_mbws=[0]*len(appNamesFull)
d2X_mlats=[0]*len(appNamesFull)
d8X_mlats=[0]*len(appNamesFull)


def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

#running it in 1110_results
for app in os.listdir('.'):
    index=getindex(app, appNamesFull);
    if(index==-1):
        print('app not found in applist: '+app)
        #os.chdir('..')
        continue
    os.chdir(app)
    for aa in os.listdir('.'):
        if('2X' in aa):
            os.chdir(aa)
            #qppscript
            #qppscript
            os.system(script_dir+'qpp_cxl.py')
            f_sss=open('short_stat_summary.txt')
            sline=f_sss.readline()
            while sline:
                if('IPC_ALL:' in sline):
                    tmp2=sline.split(':')
                    tmp=tmp2[1]
                    #tmp=sline.split('IPC_ALL:')[0]
                    if(',' in tmp):
                        tmp=tmp.split(',')[0]
                    print(tmp2)
                    print(tmp)
                    d2X_ipcs[index]=float(tmp)
                if('dramsim.log avgbw:' in sline):
                    tmp=sline.split(':')[1]
                    if(',' in tmp):
                        tmp.replace(',','')
                    d2X_mbws[index]=float(tmp)
                if('all_lat_avg,' in sline):
                   tmp=sline.split(',')[1]
                   #tmp[0].replace(',','')
                   d2X_mlats[index]=float(tmp)                    
                sline=f_sss.readline()
            f_sss.close()
            os.chdir('..')

        elif('8X' in aa):
            os.chdir(aa)
            #qppscript
            os.system(script_dir+'qpp_cxl.py')
            f_sss=open('short_stat_summary.txt')
            sline=f_sss.readline()
            while sline:
                if('IPC_ALL:' in sline):
                    tmp2=sline.split(':')
                    tmp=tmp2[1]
                    #tmp=sline.split('IPC_ALL:')[0]
                    if(',' in tmp):
                        tmp=tmp.split(',')[0]
                    print(tmp2)
                    print(tmp)
                    d8X_ipcs[index]=float(tmp)
                if('dramsim.log avgbw:' in sline):
                    tmp=sline.split(':')[1]
                    if(',' in tmp):
                        tmp.replace(',','')
                    d8X_mbws[index]=float(tmp)
                if('all_lat_avg,' in sline):
                   tmp=sline.split(',')[1]
                   #tmp[0].replace(',','')
                   d8X_mlats[index]=float(tmp)                    
                sline=f_sss.readline()
            f_sss.close()
            os.chdir('..')
    os.chdir('..')


f_2X8X_stats=open('2X8X_stats_collected.csv','w')
f_2X8X_stats.write('app,2X_ipc, 8X_ipc,\n')
for i in range(len(appNames)):
   f_2X8X_stats.write(appNames[i]+','+str(d2X_ipcs[i])+','+str(d8X_ipcs[i])+',\n' )

f_2X8X_stats.close()




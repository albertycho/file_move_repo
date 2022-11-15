#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

#script_dir = '/shared/acho44/CXL_WD/'
script_dir = '~/CXL_WD/qpp_scripts/'

cwd = os.getcwd()

#os.system('cp '+script_dir+'process_zsim_out.py .') 
#os.system('cp '+script_dir+'get_zsimout_stats_dramsim.py .')
#os.system('cp '+script_dir+'get_avg_mbw_dramsim_trim.py .')
#os.system('cp '+script_dir+'qpp_cxl.py .')

appNamesFull=['moses', 'imgdnn', 'cc', 'bc', 'lbm', 'masstree', 'pr', 'cactuBSSN', 'tc', 'parest', 'sphinx', 'bfs', 'omnetpp', 'wrf', 'xz', 'mica', 'cam4', 'monetDB', 'mcf', 'sssp', 'xapian', 'leela', 'nab', 'povray', 'deepsjeng', 'perlbench']

appNames=['mose', 'imgd', 'cc', 'bc', 'lbm', 'masst', 'pr', 'cactB', 'tc', 'parst', 'sphx', 'bfs', 'omntp', 'wrf', 'xz', 'mica', 'cam4', 'mDB', 'mcf', 'sssp', 'xapn', 'leela', 'nab', 'povray', 'deepsj', 'perlbc']

d10ns_ipcs=[0]*len(appNamesFull)
d50ns_ipcs=[0]*len(appNamesFull)
d10ns_mbws=[0]*len(appNamesFull)
d50ns_mbws=[0]*len(appNamesFull)
d10ns_mlats=[0]*len(appNamesFull)
d50ns_mlats=[0]*len(appNamesFull)

def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

f1=open('cxl_stats.csv','w')
f1.write('setup, IPC, MBW, MPKI, L3_Miss_rate, wr_lat_avg, rd_lat_avg, all_lat_avg, svc_time\n')


for dd in os.listdir('.'):
    if os.path.isdir(dd):
    #if '64P' in dd:
        print(dd)
        os.chdir(dd)
        for aa in os.listdir('.'):
            if('10ns' in aa): ##10ns
                print(os.getcwd())
                print(aa)
                os.chdir(aa)
                for app in os.listdir('.'):
                    index=getindex(app, appNamesFull);
                    if(index==-1):
                        print('app not found in applist: '+app)
                        #os.chdir('..')
                        continue
                    os.chdir(app)
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
                            d10ns_ipcs[index]=float(tmp)
                        if('dramsim.log avgbw:' in sline):
                            tmp=sline.split(':')[1]
                            if(',' in tmp):
                                tmp.replace(',','')
                            d10ns_mbws[index]=float(tmp)
                        if('all_lat_avg,' in sline):
                           tmp=sline.split(',')[1]
                           #tmp[0].replace(',','')
                           d10ns_mlats[index]=float(tmp)                    
                        sline=f_sss.readline()
                    f_sss.close()
                    os.chdir('..')
                os.chdir('..')
            elif('50ns' in aa): ##50ns
                print(os.getcwd())
                print(aa)
                os.chdir(aa)
                for app in os.listdir('.'):
                    index=getindex(app, appNamesFull);
                    if(index==-1):
                        print('app not found in applist: '+app)
                        #os.chdir('..')
                        continue
                    os.chdir(app)
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
                                #tmp.replace(',','')
                            print(tmp)
                            print(tmp2)
                            print(sline)
                            d50ns_ipcs[index]=float(tmp)
                        if('dramsim.log avgbw:' in sline):
                            tmp=sline.split(':')[1]
                            if(',' in tmp):
                                tmp.replace(',','')
                            d50ns_mbws[index]=float(tmp)
                        if('all_lat_avg,' in sline):
                           tmp=sline.split(',')[1]
                           #tmp[0].replace(',','')
                           print(str(tmp))
                           d50ns_mlats[index]=float(tmp)                    
                        sline=f_sss.readline()
                    f_sss.close()
                    os.chdir('..')
                os.chdir('..')
        os.chdir(cwd)

f_1050ns_stats=open('1050ns_stats_collected.csv','w')
f_1050ns_stats.write('app,10ns_ipc, 50ns_ipc,\n')
for i in range(len(appNames)):
   f_1050ns_stats.write(appNames[i]+','+str(d10ns_ipcs[i])+','+str(d50ns_ipcs[i])+',\n' )

f_1050ns_stats.close()


#        ipc='0';
#        mbw='0';
#        mpki='0';
#        l3_mr='0';
#        wr_lat_avg='0';
#        rd_lat_avg='0';
#        all_lat_avg='0';
#        svc_time='0';
#    
#        os.system('python3 ../qpp_cxl.py')
#
#        if exists('stat_summary.txt'):
#            stat_file = open('stat_summary.txt','r')
#
#            line = stat_file.readline()
#            while line:
#                if 'IPC_ALL' in line:
#                    tmp = line.split(': ')[1]
#                    ipc=tmp.replace(",\n","")
#                if 'MPKI' in line:
#                    tmp = line.split(':')[1]
#                    mpki=tmp.replace(",\n","")
#                if 'All_ways_miss_rate' in line:
#                    tmp = line.split(',')[1]
#                    l3_mr=tmp
#                if 'dramsim.log avgbw' in line:
#                    tmp = line.split(': ')[1]
#                    mbw=tmp.replace("\n","")
#                if 'wr_lat_avg' in line:
#                    tmp = line.split(',')[1]
#                    wr_lat_avg = tmp
#                if 'rd_lat_avg' in line:
#                    tmp = line.split(',')[1]
#                    rd_lat_avg = tmp
#                if 'all_lat_avg' in line:
#                    tmp = line.split(',')[1]
#                    all_lat_avg = tmp
#                if 'svc:' in line:
#                    tmp = line.split('mean')[1]
#                    svc_time = tmp.split('ms')[0]
#
#                ##################################
#
#                line=stat_file.readline()
#        else:
#            print('stat_summary.txt did not exist')
#
#
#        f1.write(dd+', '+ipc+','+ mbw+','+ mpki+','+ l3_mr+','+wr_lat_avg+','+rd_lat_avg+','+all_lat_avg+','+svc_time  +',\n')
#        os.chdir('..')
#
#f1.close()
#

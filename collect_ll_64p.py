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
appNames=['moses', 'imgdnn', 'cc', 'bc', 'lbm', 'masstree', 'pr', 'cactuBSSN', 'tc', 'parest', 'sphinx', 'bfs', 'omnetpp', 'wrf', 'xz', 'mica', 'cam4', 'monetDB', 'mcf', 'sssp', 'xapian', 'leela', 'nab', 'povray', 'deepsjeng', 'perlbench']

#appNames=['mose', 'imgd', 'cc', 'bc', 'lbm', 'masst', 'pr', 'cactB', 'tc', 'parst', 'sphx', 'bfs', 'omntp', 'wrf', 'xz', 'mica', 'cam4', 'mDB', 'mcf', 'sssp', 'xapn', 'leela', 'nab', 'povray', 'deepsj', 'perlbc']

DDR_ipcs=[0]*len(appNamesFull)
CXL_ipcs=[0]*len(appNamesFull)
DDR_mbws=[0]*len(appNamesFull)
CXL_mbws=[0]*len(appNamesFull)
DDR_mlats=[0]*len(appNamesFull)
CXL_mlats=[0]*len(appNamesFull)

def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1


for dd in os.listdir('.'):
    if os.path.isdir(dd):
    #if '64P' in dd:
        print(dd)
        os.chdir(dd)
        for aa in os.listdir('.'):
            if(KEYWORDFOR64P in aa):
                if('C_128_MC_8' in aa): ##DDR
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
                                DDR_ipcs[index]=float(tmp)
                            if('dramsim.log avgbw:' in sline):
                                tmp=sline.split(':')[1]
                                if(',' in tmp):
                                    tmp=tmp.split(',')[0]
                                DDR_mbws[index]=float(tmp)
                            if('all_lat_avg,' in sline):
                               tmp=sline.split(',')[1]
                               #tmp[0].replace(',','')
                               DDR_mlats[index]=float(tmp)                    
                            sline=f_sss.readline()
                        f_sss.close()
                        os.chdir('..')
                    os.chdir('..')
                elif('C_128_MC_32' in aa): ##CXL
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
                                print(tmp)
                                print(tmp2)
                                print(sline)
                                CXL_ipcs[index]=float(tmp)
                            if('dramsim.log avgbw:' in sline):
                                tmp=sline.split(':')[1]
                                if(',' in tmp):
                                    tmp=tmp.split(',')[0]
                                print(tmp)
                                CXL_mbws[index]=float(tmp)
                            if('all_lat_avg,' in sline):
                               tmp=sline.split(',')[1]
                               #tmp[0].replace(',','')
                               print(str(tmp))
                               CXL_mlats[index]=float(tmp)                    
                            sline=f_sss.readline()
                        f_sss.close()
                        os.chdir('..')
                    os.chdir('..')
        os.chdir(cwd)

f_ll16p_stats=open('ll_64P_stats_collected.csv','w')
f_ll16p_stats.write('app,ddr_ipc, cxl_ipc,ddr_mbw,cxl_mbw,ddr_mlat,cxl_mlat,\n')
for i in range(len(appNames)):
   f_ll16p_stats.write(appNames[i]+','+str(DDR_ipcs[i])+','+str(CXL_ipcs[i])+','+str(DDR_mbws[i])+','+str(CXL_mbws[i])+','+str(DDR_mlats[i])+','+str(CXL_mlats[i])+',\n' )

f_ll16p_stats.close()



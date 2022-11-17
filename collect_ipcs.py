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

#appNamesFull=['moses', 'imgdnn', 'cc', 'bc', 'lbm', 'masstree', 'pr', 'cactuBSSN', 'tc', 'parest', 'sphinx', 'bfs', 'omnetpp', 'wrf', 'xz', 'mica', 'cam4', 'monetdb', 'mcf', 'sssp', 'xapian', 'leela', 'nab', 'povray', 'deepsjeng', 'perlbench']
#
#appNames=['mose', 'imgd', 'cc', 'bc', 'lbm', 'masst', 'pr', 'cactB', 'tc', 'parst', 'sphx', 'bfs', 'omntp', 'wrf', 'xz', 'mica', 'cam4', 'mDB', 'mcf', 'sssp', 'xapn', 'leela', 'nab', 'povray', 'deepsj', 'perlbc']

appNames=['moses','bc','bfs','mcf','perlbench']



fixed_ipcs=[0]*len(appNames)
d350_ipcs=[0]*len(appNames)
d450_ipcs=[0]*len(appNames)
d550_ipcs=[0]*len(appNames)

def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

#running it in 1110_results
for app in os.listdir('.'):
    index=getindex(app, appNames);
    if(index==-1):
        print('app not found in applist: '+app)
        #os.chdir('..')
        continue
    os.chdir(app)
    for aa in os.listdir('.'):
        if('fixed' in aa):
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
                    fixed_ipcs[index]=float(tmp)
                sline=f_sss.readline()
            f_sss.close()
            os.chdir('..')
        elif('350' in aa):
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
                    d350_ipcs[index]=float(tmp)
                sline=f_sss.readline()
            f_sss.close()
            os.chdir('..')
        elif('450' in aa):
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
                    d450_ipcs[index]=float(tmp)
                sline=f_sss.readline()
            f_sss.close()
            os.chdir('..')

        elif('550' in aa):
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
                    d550_ipcs[index]=float(tmp)
                sline=f_sss.readline()
            f_sss.close()
            os.chdir('..')

    os.chdir('..')


f_memvar_ipcs=open('memvar_ipcs.csv','w')
f_memvar_ipcs.write('app,fixed_ipc, 350_ipc,450_ipc,550_ipc,\n')
for i in range(len(appNames)):
   f_memvar_ipcs.write(appNames[i]+','+str(fixed_ipcs[i])+','+str(d350_ipcs[i]) +','+str(d450_ipcs[i]) +','+str(d550_ipcs[i]) +',\n' )

f_memvar_ipcs.close()




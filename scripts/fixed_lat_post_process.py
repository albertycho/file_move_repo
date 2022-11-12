#!/usr/bin/env python3                                                          
                                                                                
import os                                                                       
import sys                                                                      
import csv                                                                      
import math                                                                     
import statistics                                                               
import numpy as np                                                              
import argparse                                                                 
from os.path import exists                                                      
                                                                                
                                                                                
parser = argparse.ArgumentParser()                                              
parser.add_argument('--prefix', type=str, default='fixed')                      
args = parser.parse_args()                                                      
prefix=args.prefix                                                              
                                                                                
script_dir = '/home/azureuser/CXL_WD/scripts/'                                           
                                                                                
os.system('cp '+script_dir+'process_zsim_out.py .')                             
#os.system('rm get_mem_lat.py')                                                 
#os.system('cp '+script_dir+'get_mem_lat.py .')                                 
#os.system('cp '+script_dir+'get_avg_mbw_trim_roi.py .')                        
os.system('cp '+script_dir+'get_zsimout_stats_dramsim.py .')                    
os.system('cp '+script_dir+'get_avg_mbw_dramsim_trim.py .')                     
                                                                                
os.system('cp '+script_dir+'parselats_partial.py .')                            
os.system('cp '+script_dir+'qpp_cxl.py .')                                      
#os.system('cp '+script_dir+'get_memhog_perf.py .')                             
                                                                                
f1=open('cxl_stats.csv','w')                                                    
#f1.write('setup, IPC, MBW, MPKI, L3_Miss_rate, wr_lat_avg, rd_lat_avg, all_lat_avg, svc_time\n')
f1.write('setup, IPC, CPI, RERD, MBW, MPKI,\n')  

for jj in range(0,1100,100):
    #dd = 'r200_'+str(jj)
    dd = prefix+'_'+str(jj)

    if os.path.isdir(dd):
    #if '64P' in dd:
        print(dd)
        os.chdir(dd)
        ipc='0';
        cpi='0';
        rerd='0';
        mbw='0';
        mpki='0';
        l3_mr='0';
        wr_lat_avg='0';
        rd_lat_avg='0';
        all_lat_avg='0';
        svc_time='0';

        os.system('python3 ../qpp_cxl.py')

        if exists('stat_summary.txt'):
            stat_file = open('stat_summary.txt','r')

            line = stat_file.readline()
            while line:
                if 'IPC_ALL' in line:
                    tmp = line.split(': ')[1]
                    ipc=tmp.replace(",\n","")
                if 'CPI' in line:
                    tmp = line.split(': ')[1]
                    cpi=tmp.replace(",\n","")
                if 'RERD' in line:
                    tmp = line.split(': ')[1]
                    rerd=tmp.replace(",\n","")
                                                                             
                                                                                
                if 'MPKI' in line:                                              
                    tmp = line.split(':')[1]                                    
                    mpki=tmp.replace(",\n","")                                  
                if 'All_ways_miss_rate' in line:                                
                    tmp = line.split(',')[1]                                    
                    l3_mr=tmp                                                   
                if 'dramsim.log avgbw' in line:                                 
                    tmp = line.split(': ')[1]                                   
                    mbw=tmp.replace("\n","")                                    
                if 'wr_lat_avg' in line:                                        
                    tmp = line.split(',')[1]                                    
                    wr_lat_avg = tmp                                            
                if 'rd_lat_avg' in line:                                        
                    tmp = line.split(',')[1]                                    
                    rd_lat_avg = tmp                                            
                if 'all_lat_avg' in line:                                       
                    tmp = line.split(',')[1]                                    
                    all_lat_avg = tmp                                           
                if 'svc:' in line:                                              
                    tmp = line.split('mean')[1]                                 
                    svc_time = tmp.split('ms')[0]                               
                                                                                
                ##################################                              
                                                                                
                line=stat_file.readline()                                       
        else:                                                                   
            print('stat_summary.txt did not exist')           


        f1.write(dd+','+ipc +','+cpi +','+rerd+','+ mbw+','+ mpki+',\n')
        os.chdir('..')
f1.close()

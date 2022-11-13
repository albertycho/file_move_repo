#!/usr/bin/env python                                                           
                                                                                
import os                                                                       
import sys                                                                      
                                                                                
from multiprocessing import Process                                             
from multiprocessing import Semaphore                                           
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
#mcs = ['4','8','16']                                                           
#cxl_delays=['100']                                                             
                                                                                
                                                                                
                                                                                
pcmds=[]                                                                        
for i in range(0,16,1):                                                         
    #pcmd = './cxl_memhog_rand_run.py --base_cfg AMD64_cxl_memhog.cfg  --num_server '+str(i+1)+'  --mem_controllers 1  --out_dir 0928_DDR5_BW_LAT/DDR4_1006/'+str(i+1)+'C'
    pcmd = './cxl_seracc.py --base_cfg AMD_DDR5_base_1109_BWLAT.cfg  --num_server '+str(i+1)+'  --mem_controllers 64  --out_dir 1110_BW_LAT/SERACC64MC/'+str(i+1)+'C'
    pcmds.append(pcmd)                                                          
    print(pcmd)                                                                 
                                                                                
                                                                                
                                                                                
                                                                                
def f(fcmd, sema):                                                              
    print(fcmd)                                                                 
    os.system(fcmd)                                                             
    sema.release()                                                              
                                                                                
                                                                                
def clean_runaways():                                                           
    os.system('killall -9 herd')                                                
    os.system('killall -9 l3fwd')                                               
    os.system('killall -9 simpNF')                                              
    os.system('killall -9 zsim')                                                
    os.system('killall -9 nic_egress_proxy_app')                                
    os.system('killall -9 nic_proxy_app')                                       
    os.system('killall -9 memhog_mt')                                           
    os.system('ipcrm -a')                                       


                                                                                   
if __name__=='__main__':                                                           
    concurrency = 6                                                                
    sema = Semaphore(concurrency)                                               
    all_processes=[]                                                            
                                                                                
    tmp=0                                                                       
    tmp2=0                                                                      
                                                                                
    for pcmd in pcmds:                                                          
        sema.acquire()                                                          
        p=Process(target=f, args=(pcmd,sema))                                   
        all_processes.append(p)                                                 
        p.start()                                                               
        print('runall launched task no '+str(tmp))                              
        tmp=tmp+1                                                               
        ### clean up periodically. making sure to not send kill while things run
        #if(tmp==concurrency*2):                                                
        #    for p in all_processes:                                            
        #        p.join()                                                       
        #    tmp2=tmp2+1                                                        
        #    tmp=0                                                              
        #    #print('preiodic cleanup')                                         
        #    #clean_runaways()                                                  
        #    #print(str(tmp2)+'th '+str(concurrency*2)+' tasks done')           
                                                                                
    for p in all_processes:                                                     
        p.join()                                                                
                                                                                
                                                                                
    print('runall_mp - '+' Done')                                               
    #os.system('ipcrm -a')                             

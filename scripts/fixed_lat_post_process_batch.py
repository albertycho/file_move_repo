#!/usr/bin/env python3                                                          
                                                                                
import os                                                                       
import sys                                                                      
import csv                                                                      
import math                                                                     
import statistics                                                               
import numpy as np                                                              
import argparse                                                                 
from os.path import exists                                                      
                                                                                
                                                                                
                                                                                
for dd in os.listdir('.'):                                                      
    if os.path.isdir(dd):                                                       
        print(dd)                                                               
        os.chdir(dd)                                                            
        os.system('python3 /home/azureuser/CXL_WD/scripts/fixed_lat_post_process.py --prefix '+dd)
        os.chdir('..')                                                          
        os.system('cat '+dd+'/cxl_stats.csv >> cxl_stats.csv')                  

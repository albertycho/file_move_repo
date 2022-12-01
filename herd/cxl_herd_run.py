#!/usr/bin/env python

import os
import sys
import argparse

#args: 1 outdir 2 zsim_exec 3 base cfg file 4 num_server 5 phaseLength 

# this is your base zsim directory
home = '/nethome/acho44/zsim/albert_dev_zsim/zSim'
#home = '/nethome/acho44/zsim/1027_zSim'

herd_path = '/nethome/acho44/zsim/herd-sonuma-zsim/build/herd'



# parse cmd args
parser = argparse.ArgumentParser()
#parser.add_argument('--zsim_dir', type=str, default='/nethome/acho44/zsim/zSim')
parser.add_argument('--zsim_dir', type=str, default='/nethome/acho44/zsim/albert_dev_zsim/zSim')
parser.add_argument('--out_dir', type=str, default='out_dir')
parser.add_argument('--exec_file', type=str, default='build/opt/zsim')
#parser.add_argument('--base_cfg', type=str, default='AMD64_cxl_HERD.cfg')
#parser.add_argument('--base_cfg', type=str, default='AMD_DDR5_HERD.cfg')
parser.add_argument('--base_cfg', type=str, default='AMD_DDR5_HERD_keep_128C.cfg')
parser.add_argument('--printstd', type=str, default='0')


parser.add_argument('--num_keys', type=str, default='0')
parser.add_argument('--num_server', type=str, default='8')
parser.add_argument('--llc_size', type=str, default='0')
parser.add_argument('--mem_controllers', type=str, default='1')
parser.add_argument('--cxl_delay',type=str,default='0')
parser.add_argument('--req_per_core',type=str,default='5000')
args = parser.parse_args()

# 1st input: the output directory you want the run to take place + store results
#outdir = sys.argv[1] 
outdir = args.out_dir
os.system('rm -rf '+outdir)
os.system('mkdir '+outdir)
os.chdir(outdir)

zsim_dir=args.zsim_dir

# 2nd input: the zsim executable to use
#zsim_exec = sys.argv[2]
zsim_exec = args.exec_file
os.system ('cp '+zsim_dir+'/'+zsim_exec+' .')
#os.system ('cp '+home+'/'+zsim_exec+' .')

# 3rd input: the base config file (assuming it's in the tests folder)
#confile = sys.argv[3]
confile = args.base_cfg
#os.system('cp '+home+'/tests/'+confile+' .')
os.system('cp /shared/acho44/CXL_WD/'+confile+' .')
#os.system('cp '+moses_path+'moses.ini'+' .')

os.system('cp '+home+'/sweeper_tests/nic_proxy_app .')                                  
os.system('cp '+home+'/sweeper_tests/nic_egress_proxy_app .') 
os.system('cp '+herd_path+' .') 



set_num_keys=True
num_keys=args.num_keys
if(num_keys=='0'):
    set_num_keys=False

# configurable param input:


num_server=args.num_server
num_server_int=int(num_server)

llc_size=args.llc_size
llc_size_int=int(llc_size)
if(llc_size_int==0):
    llc_size_int=2*int(num_server)
llc_size_int=llc_size_int*1024*1024
llc_size=str(llc_size_int)


mem_controllers=args.mem_controllers
is_ideal_IO = False
is_simplemem = False
if('ideal' in mem_controllers):
    is_ideal_IO = True
    mem_controllers = '8'
if('simplemem' in mem_controllers):
    is_simplemem = True
    mem_controllers = '8' #doesn't really matter as long as there is some value


cxl_delay=args.cxl_delay
set_cxl_delay=True
if(cxl_delay=='0'):
    set_cxl_delay=False

req_per_core=args.req_per_core
total_reqs=str((int(req_per_core))*num_server_int)

#wsize=args.wsize
#set_wsize=True
#if(wsize=='0'):
#    set_wsize=False


printstd=args.printstd


# create params.txt in outdir to record input params to this run/dir
#fpar = open('params.txt', 'w')
#fpar.write('num_server ='+num_server+'\n')
#fpar.write('phaseLength ='+phaseLength+'\n')
#fpar.write('packet_injection_rate ='+packet_injection_rate+'\n')
#fpar.write('packet_count ='+packet_count+'\n')
#fpar.close()


# create the new config file
f1 = open(confile)
f2 = open('conf.cfg','w')
line = f1.readline()
while line:
        if 'controllers' in line:
            tmp = line.split('=')[0]
            f2.write(tmp+'= '+mem_controllers+';\n')

        elif 'networkFile' in line:
            tmp = line.split('network.conf')
            if(set_cxl_delay):
                #f2.write(tmp[0]+'network_'+mem_controllers+'_'+cxl_delay+'.conf'+tmp[1])
                f2.write(tmp[0]+'network_mem_splitter_'+cxl_delay+'.conf'+tmp[1])
            else:
                #f2.write(tmp[0]+'network_'+mem_controllers+'_0.conf'+tmp[1])
                f2.write(tmp[0]+'network_mem_splitter_0.conf'+tmp[1])
        #elif 'cxl_delay' in line:
        #    if(set_cxl_delay):
        #        tmp = line.split('=')[0]
        #        f2.write(tmp+' = '+cxl_delay+';\n')
        #    else:
        #        f2.write(line);
        elif 'L3SIZE_TAG' in line:
            tmp = line.split('=')[0]
            f2.write(tmp+'= '+llc_size+';\n')
            
        elif 'num_keys' in line:
            if(set_num_keys):
                tmp = line.split('=')[0]
                f2.write(tmp+'= '+num_keys+';\n')
            else:
                f2.write(line)
        elif '--num-keys' in line:
            if(set_num_keys):
                tmp = line.split(' ')[0]
                f2.write(tmp+' '+num_keys+' \\\n')
            else:
                f2.write(line)
        ## num_server
        elif 'num_cores_serving_nw' in line:
            tmp = line.split('=')[0]
            f2.write(tmp+' = '+num_server+';\n')
        elif 'assoc_cores' in line:
            tmp = line.split('=')[0]
            f2.write(tmp+' = '+num_server+';\n')
        elif 'dumpHeartbeats' in line:
            tmp = line.split('=')[0]
            f2.write(tmp+' = '+num_server+'L;\n')
        elif 'qps-to-create' in line:
            tmp = line.split(' ')[0]
            f2.write(tmp+' '+num_server+' \\\n')
        elif 'num-threads' in line:
            tmp = line.split(' ')[0]
            f2.write(tmp+' '+num_server+' \\\n')
        #elif 'banks' in line:
	#	tmp = line.split('=')[0]
        #        f2.write(tmp+'= '+num_server+';\n')

        else:
            f2.write(line)
        
        line = f1.readline()

###now add processes
##for i in range(0,num_server_int,1):
##    f2.write('process'+str(i)+' = {\n')
##    #f2.write('ffiPoints = "4100000000 10000000000000";\n')
##    f2.write('startFastForwarded = True;\n')
##    f2.write('    command = '+pcommand+'\n')
##    f2.write('};\n')
##

f1.close()
f2.close()

# launch the run, redirectung stdin and stderr to log files 

##os.system('./zsim conf.cfg 1> res.txt 2>app.txt &')
if '1' in printstd:
    #os.system('timeout 30m ./zsim conf.cfg')
    os.system('./zsim conf.cfg')
else:
    #os.system('timeout 30m ./zsim conf.cfg 1> res.txt 2>app.txt')
    os.system('./zsim conf.cfg 1> res.txt 2>app.txt &')
#os.system('python3 ../process_zsim_out.py')
#os.system('python3 ../process_timestamps.py')
#os.system('../process_skew.py')
os.system('cd ..')

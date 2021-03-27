# Functins to fetch data from ecfs
import subprocess
import os
import numpy as np
from collections import OrderedDict
import re
import date_utils as du

def fetch_CONV(obsdir,year,month,destination):
    '''
    This copies all conventional observations for a given month and year
    '''
    lobs_epath = 'ec:/rml/precise/obs/obsoul/locobs/v11jun20/'
    #First check if directory exists
    obspath = os.path.join(lobs_epath,str(year),str(month).zfill(2))
    try:
        cmd = "els "+obspath
        ret = subprocess.check_output(cmd,shell=True) 
        ret_clean = ret.rstrip().decode('utf-8')
        files_found = ret_clean.split("\n") 
        #add whole path to the file names:
        files_found = [os.path.join(obspath,f) for f in files_found]
        #print(f"Return from els: {files_found}")
    except subprocess.CalledProcessError as err:
        print("Error in subprocess {}".format(err))
        print("Directory {}")
       
        
    cmd="ecp "+os.path.join(lobs_epath,str(year),str(month).zfill(2),"*")+' '+destination
    print("DEBUG obsoul command: %s"%cmd)
    try:
        ret=subprocess.check_output(cmd,shell=True)
    except subprocess.CalledProcessError as err:
        print('obsoul monthly file not found %s'%err)

def fetch_OSISAF(obsdir,year,month,destination):
    obsfile='carra_sst_iceconc_'
    obspath = els_cmd.replace("els ec:","")
    file_names = "".join([obsfile,str(year),str(month).zfill(2),"*"])
    cmd = os.path.join(els_cmd,obsdir,"osisaf_v5",str(year),file_names)
    #this is only for checking files are there
    try:
        ret = subprocess.check_output(cmd,shell=True)
        ret_clean = ret.rstrip().decode('utf-8')
        files_found = ret_clean.split("\n")
        #add whole path to the file names:
        files_found = [os.path.join(obspath,obsdir,"osisaf_v5",str(year),f) for f in files_found]
        #print(f"Return from els: {files_found}")
    except subprocess.CalledProcessError as err:
        print("Error in subprocess {}".format(err))
    ndays = du.days_month(month,year)
    if len(files_found) == ndays:
        print(f"All {obsdir} files for {month}{year} present")
    else:
        print(f"WARNING: {obsdir} files for {month}{year} not complete. Only {len(files_found)} found")
    cmd = cmd.replace("els","ecp")+' '+destination    
    print("DEBUG obsoul command: %s"%cmd)
    try:
        ret=subprocess.check_output(cmd,shell=True)
    except subprocess.CalledProcessError as err:
        print(f'Error running {cmd}: {err}')

def create_destination(obsdir,year,month,scratch):
    if obs == "CONV":
        obspath=os.path.join(scratch,obsdir,year,month) #"LocalObsdata")
    elif obs == "RO":
        obspath=os.path.join(scratch,obsdir)

    if not os.path.isdir(obspath):
        os.makedirs(obspath)



def check_if_present(obs,year,month,fpre): #scratch):
    '''
    Check if data already present. Currently assuming it is only locobs
    Not sure how many files are supposed to be available, but 
    counting for 1994 I see between 224 and 248
    '''
    print(f"Checking if {obs} data for {year}/{month} is already there")
    if obs == "CONV":
        fmin = 200 #threshold for obs. Completely arbitrary!
        obsYYMM = os.path.join(destination,fpre+"_"+str(year)+str(month).zfill(2))
    elif obs == "RO":
        fmin = du.days_month(month,year)
        obsYYMM = os.path.join(destination,fpre+"_"+str(year)+str(month).zfill(2))
    files_present=False
    import glob
    obsfiles = glob.glob(obsYYMM+"*")
    #print(f"obs files found {obsfiles}")
    if len(obsfiles) >= fmin:
        files_present = True
    return files_present



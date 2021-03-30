# Functins to fetch data from ecfs
import subprocess
import os
import numpy as np
from collections import OrderedDict
import re
import date_utils as du
import sys

def fetch_RO_local(localpath,fpre,fend,year,month,destination):
    print("Attempting to fetch RO observations locally")
    tarball = "_".join([fpre,str(year)+str(month).zfill(2),fend])
    obspath = os.path.join(localpath,tarball)
    if os.path.isfile(obspath):
        from shutil import copy2
        copy2(obspath,os.path.join(destination,tarball))
        #untar and delete file
        cdir=os.getcwd()
        os.chdir(destination)
        cmd = "tar xvf "+tarball
        ret=subprocess.check_output(cmd,shell=True)
        os.remove(tarball)
        os.chdir(cdir)
    else:
        print(f"{obspath} does not exist!")

def fetch_CONV(ecfspath,year,month,destination):
    '''
    This copies all conventional observations for a given month and year
    '''
    print("Attempting to fetch CONV observations")
    obspath = os.path.join(ecfspath,str(year),str(month).zfill(2))
    #First check if file(s)there
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
       
    if len(files_found) != 0:
        cmd="ecp "+os.path.join(obspath,"*")+' '+destination
        print("DEBUG obsoul command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('obsoul monthly file not found %s'%err)
    else:
        print(f"No data found for {year} and {month}")

def fetch_RO(ecfspath,tarball,destination):
    '''
    Fetch RO data. In this case we grab .tar balls
    and uncompress them in destination directory
    '''
    print("Attempting to fetch RO observations")
    obspath = os.path.join(ecfspath,tarball)
    try:
        cmd = "els "+obspath
        ret = subprocess.check_output(cmd,shell=True) 
        ret_clean = ret.rstrip().decode('utf-8')
        files_found = ret_clean.split("\n") 
        #add whole path to the file names:
        files_found = [os.path.join(ecfspath,f) for f in files_found]
        #print(f"Return from els: {files_found}")
    except subprocess.CalledProcessError as err:
        print("Error in subprocess {}".format(err))
        print("Directory {}")
       
    if len(files_found) != 0:
        cmd="ecp "+obspath+' '+destination
        print("DEBUG RO command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('RO monthly file not found %s'%err)
        #untar and delete file
        cdir=os.getcwd()
        os.chdir(destination)
        cmd = "tar xvf "+tarball
        ret=subprocess.check_output(cmd,shell=True)
        os.remove(tarball)
        os.chdir(cdir)
    else:
        print(f"No data found for {year} and {month}")

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
    '''
    Create destination directory if it doesnt exist
    Return the path
    '''
    if obsdir == "LocalObsdata":
        obspath=os.path.join(scratch,obsdir) #,year,month) #"LocalObsdata")
    elif obsdir == "ROdata":
        obspath=os.path.join(scratch,obsdir)

    if not os.path.isdir(obspath):
        os.makedirs(obspath)
    return obspath



def test_if_present(obs,year,month,fpre,destination): 
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
        fmin = 8 # Every 3 hours. du.days_month(month,year)
        obsYYMM = os.path.join(destination,fpre+"_"+str(year)+str(month).zfill(2))
    files_present=False
    import glob
    obsfiles = glob.glob(obsYYMM+"*")
    #print(f"obs files found {obsfiles}")
    if len(obsfiles) >= fmin:
        files_present = True
    return files_present



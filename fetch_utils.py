# Functins to fetch data from ecfs
import subprocess
import os
import numpy as np
from collections import OrderedDict
import re
import date_utils as du
import sys

def fetch_CRYO(ecfs,year,month,destination):
    '''
    Fetch the CRYO data, which is organized in two different
    directories for East and West
    '''
    #data["OBS"]["CRYO"]["ECSUBDIR"]
    ecfspath = ecfs["PATH"]
    print("Attempting to fetch CONV observations")
    #First check if file(s)there
    for cdir in ecfs["SUBDIR"]:
        obspath = os.path.join(ecfspath,cdir,str(year))
        try:
            fnames = "_".join([ecfs["FPRE"],str(year)+str(month).zfill(2)])+"*"
            cmd = "els "+os.path.join(obspath,fnames)
            ret = subprocess.check_output(cmd,shell=True) 
            ret_clean = ret.rstrip().decode('utf-8')
            files_found = ret_clean.split("\n") 
            #add whole path to the file names:
            files_found = [os.path.join(obspath,f) for f in files_found]
            #print(f"Return from els: {files_found}")
        except subprocess.CalledProcessError as err:
            print("Error in subprocess {}".format(err))
            print(f"Directory {obspath}")
            print(f"Files probably not found!")
            sys.exit(1)
        if len(files_found) != 0:
            fnames = "_".join([ecfs["FPRE"],str(year)+str(month).zfill(2)])+"*"
            cmd="ecp "+os.path.join(obspath,fnames)+' '+destination
            print("DEBUG CRYO command: %s"%cmd)
            try:
                ret=subprocess.check_output(cmd,shell=True)
            except subprocess.CalledProcessError as err:
                print(f'No data found for {cdir}: {err}')
        else:
            print(f"No data found for {year}")

#def fetch_RO_local(localpath,fpre,fend,year,month,destination):
def fetch_RO_local(localpath,ecfs,year,month,destination):
    ecfspath = ecfs["PATH"]
    print("Attempting to fetch RO observations locally")
    fpre = ecfs["FPRE"]
    fend = ecfs["FEND"]
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

def fetch_CONV(ecfs,year,month,destination):
    '''
    This copies all conventional observations for a given month and year
    '''
    ecfspath = ecfs["PATH"]
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
        print(f"Directory {obspath}")
        print(f"Files probably not found!")
        sys.exit(1)
       
    if len(files_found) != 0:
        cmd="ecp "+os.path.join(obspath,"*")+' '+destination
        print("DEBUG obsoul command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('obsoul monthly file not found %s'%err)
    else:
        print(f"No data found for {year} and {month}")

def fetch_RO(ecfs,tarball,destination):
    '''
    Fetch RO data. In this case we grab .tar balls
    and uncompress them in destination directory
    '''
    ecfspath = ecfs["PATH"]
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
        print(f"Directory {obspath}")
        print(f"Files probably not found!")
        sys.exit(1)
       
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

def fetch_OSISAF(ecfs,year,month,destination):
    '''
    Fetch OSISAF data
    '''
    ecfspath = ecfs["PATH"]
    print("Attempting to fetch OSISAF observations")
    obspath = os.path.join(ecfspath,str(year))
    try:
        fnames = "_".join([ecfs["FPRE"],str(year)+str(month).zfill(2)])+"*"
        cmd = "els "+os.path.join(obspath,fnames)
        ret = subprocess.check_output(cmd,shell=True) 
        ret_clean = ret.rstrip().decode('utf-8')
        files_found = ret_clean.split("\n") 
        #add whole path to the file names:
        files_found = [os.path.join(obspath,f) for f in files_found]
    except subprocess.CalledProcessError as err:
        print("Error in subprocess {}".format(err))
        print(f"Directory {obspath}")
        print(f"Files probably not found!")
        sys.exit(1)
    if len(files_found) != 0:
        fnames = "_".join([ecfs["FPRE"],str(year)+str(month).zfill(2)])+"*"
        cmd="ecp "+os.path.join(obspath,fnames)+' '+destination
        print("DEBUG OSISAF command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print(f'No data found for {cdir}: {err}')
    else:
        print(f"No data found for {year}")

def create_destination(obsdir,year,month,scratch):
    '''
    Create destination directory if it doesnt exist
    Return the path
    '''
    obspath=os.path.join(scratch,obsdir["OBSDIR"]) #,year,month) #"LocalObsdata")
    if len(obsdir["SUBDIR"]) == 0: #== "LocalObsdata":
        if not os.path.isdir(obspath):
            os.makedirs(obspath)
    else:
        for cdir in obsdir["SUBDIR"]:
            if cdir == "YYYY":
                fdir = str(year)
            else:
                fdir = cdir
            obspath = os.path.join(obspath,fdir)
            if not os.path.isdir(obspath):
                os.makedirs(obspath) #os.path.join(obspath,fdir))
     
    #elif obsdir["OBSDIR"] == "ROdata":
    #    obspath=os.path.join(scratch,obsdir)
    #elif obsdir["OBSDIR"] == "CRYO":
    #    import pdb
    #    pdb.set_trace()
    #    obspath=os.path.join(scratch,obsdir)

    #if not os.path.isdir(obspath):
    #    os.makedirs(obspath)
            
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
    elif obs == "CRYO":
        fmin = 28 # A file per day. TODO: calculate number of days in month here!
        obsYYMM = os.path.join(destination,fpre+"_"+str(year)+str(month).zfill(2))
    elif obs == "OSISAF":
        fmin = 28 # A file per day. TODO: calculate number of days in month here!
        obsYYMM = os.path.join(destination,fpre+"_"+str(year)+str(month).zfill(2))
    files_present=False
    import glob
    obsfiles = glob.glob(obsYYMM+"*")
    #print(f"obs files found {obsfiles}")
    if len(obsfiles) >= fmin:
        files_present = True
    return files_present



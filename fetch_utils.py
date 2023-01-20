# Functins to fetch data from ecfs
import subprocess
import os
import numpy as np
from collections import OrderedDict
import re
import date_utils as du
import sys

def fetch_local(obs,ecfs,localpath,year,month,destination):
    if obs == 'RO':
        fetch_RO_local(localpath,ecfs,year,month,destination)
    else:
        print(f"No local data available for {obs}!")

def fetch_ecfs(obs,ecfs,year,month,destination):
    '''
    single call to ecfs according to DTG
    '''
    if obs == 'CONV':
        fetch_CONV(ecfs,year,month,destination)
    elif obs == 'RO':
        #tarball = "_".join(["GPSRO",str(year)+str(month).zfill(2),"Precise"])+".tar"
        tarball = "_".join([ecfs["FPRE"],str(year)+str(month).zfill(2),ecfs["FEND"]])+"."+ecfs["FILETYPE"]
        fetch_RO(ecfs,tarball,destination)
    elif obs == 'CRYO':
        fetch_CRYO(ecfs,year,month,destination)
    elif obs == 'OSISAF':
        fetch_OSISAF(ecfs,year,month,destination)
    elif obs == 'SCATT':
        import SCATTdata
        SCATTdata.fetch_SCATT(ecfs,year,month,destination)
    elif obs == 'IASI':
        import IASIdata
        IASIdata.fetch_IASI(ecfs,year,month,destination)
    elif obs == 'SICE':
        import SICEdata
        SICEdata.fetch_SICE(ecfs,year,month,destination)
    elif obs == 'GEUS':
        import GEUSdata
        GEUSdata.fetch_GEUS(ecfs,year,destination)
    else:
        ecfspath = ecfs["PATH"]
        print(f"No implementation for {ecfspath} just yet!")
        print("Currently doing ONLY CONV, RO, CRYO and OSISAF observations")
        sys.exit()



def fetch_CRYO(ecfs,year,month,destination):
    '''
    Fetch the CRYO data, which is organized in two different
    directories for East and West
    destination is a list here
    '''
    #data["OBS"]["CRYO"]["ECSUBDIR"]
    ecfspath = ecfs["PATH"]
    print("Attempting to fetch CRYO observations")
    #First check if file(s)there
    #for cdir in ecfs["SUBDIR"]:
    cdir = os.path.split(destination)[-1]
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
        return
        #sys.exit(1)
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

def fetch_RO_local(localpath,ecfs,year,month,destination):
    '''
    destination is a string
    '''
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

def fetch_CONV(ecfs,year,month,destination,cp_com="ecfsdir"):
    '''
    This copies all conventional observations for a given month and year
    destination is a string
    NOTE: I use ecp ONLY in some special cases (ie for DANRA).
    Normally I use the ecfsdir command (ie, for CARRA)
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
        #sys.exit(1)
        return
       
    if len(files_found) != 0:
        if cp_com == "ecp":
            cmd=cp_com+" "+os.path.join(obspath,"*")+' '+destination
        elif cp_com == "ecfsdir":
            #for ecfsdir, first copy to local yyyymm, then move to location
            cmd=cp_com+" "+obspath+' '+os.path.join(destination,str(year)+str(month).zfill(2))
        print("DEBUG obsoul command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('obsoul monthly file not found %s'%err)
        #move data if command was ecfsdir
        if cp_com == "ecfsdir":
            cmd="mv "+os.path.join(destination,str(year)+str(month).zfill(2),"obs*")+' '+destination
            print(f"Moving data: {cmd}")
            try:
                ret=subprocess.check_output(cmd,shell=True)
                os.rmdir(os.path.join(destination,str(year)+str(month).zfill(2)))
            except subprocess.CalledProcessError as err:
                print(f'{cmd} failed with error {err}')
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
        return
        #sys.exit(1)
       
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
    destination is a list
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
        return
        #sys.exit(1)
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
    Return the path, either a list or a single string
    '''
    obspath_base=os.path.join(scratch,obsdir["OBSDIR"]) #,year,month) #"LocalObsdata")
    if len(obsdir["SUBDIR"]) == 0:
        if not os.path.isdir(obspath_base):
            os.makedirs(obspath_base)
        destination = obspath_base
    else:
        destination = []
        for cdir in obsdir["SUBDIR"]:
            if cdir == "YYYY":
                fdir = str(year)
            elif cdir == "YYYY/MM":
                fdir = str(year)+"/"+str(month).zfill(2)
            else:
                fdir = cdir
            obspath = os.path.join(obspath_base,fdir)
            if not os.path.isdir(obspath):
                os.makedirs(obspath) #os.path.join(obspath,fdir))
            destination.append(obspath)
    return destination



#def test_if_present(obs,year,month,fpre,destination): 
def fetch_data(yaml_args):
    '''
    Check if data already present. Currently assuming it is only locobs
    Not sure how many files are supposed to be available, but 
    counting for 1994 I see between 224 and 248
    '''
    obs = yaml_args["CL_ARGS"]["OBS"]
    ecfs = yaml_args["OBS"][obs]["ECFS"]
    ecfspath = yaml_args["OBS"][obs]["ECFS"]["PATH"]
    year = yaml_args["CL_ARGS"]["YEAR"]
    month = yaml_args["CL_ARGS"]["MONTH"]
    obsdir = yaml_args["OBS"][obs]["LOCALDIR"]
    fpre = ecfs["FPRE"]
    scratch = yaml_args["SCRATCH"]

    print(f"Checking if {obs} data for {year}/{month} is already there")
    #note, this is the min number for files, for those with 28 it is really the number of days
    #todo: define this as number of days in month
    #for geus, those are julian days, for a few months of the year
    fmin = { "CONV": 200, "RO": 8, "CRYO": 28, "OSISAF": 28,
            "SCATT":1, "IASI":120, "SICE":28,"GEUS":240}
    destination = create_destination(obsdir,year,month,scratch)
    #use this path instead of the ECFS path if it is defined
    localpath = yaml_args["OBS"][obs]["ECFS"]["LOCALPATH"]
    if isinstance(destination,list):
        dest_todo = []
        for dest in destination:
            obsYYMM = os.path.join(dest,fpre+"_"+str(year)+str(month).zfill(2))
            import glob
            obsfiles = glob.glob(obsYYMM+"*")
            #print(f"obs files found {obsfiles}")
            if len(obsfiles) >= fmin[obs]:
                print(f"Observations for {year}/{month} already copied!")
            else:
                if len(localpath) != 0:
                    print(f"Fetching data locally from: {localpath}")
                    fetch_local(obs,ecfs,localpath,year,month,dest)
                else:
                    print(f"Fetching data from ECFS: {ecfspath}")
                    fetch_ecfs(obs,ecfs,year,month,dest)

    else:
        obsYYMM = os.path.join(destination,fpre+"_"+str(year)+str(month).zfill(2))
        import glob
        obsfiles = glob.glob(obsYYMM+"*")
        #print(f"obs files found {obsfiles}")
        if len(obsfiles) >= fmin[obs]:
            print(f"Observations for {year}/{month} already copied!")
        else:
            if len(localpath) != 0:
                print(f"Fetching data locally from: {localpath}")
                fetch_local(obs,ecfs,localpath,year,month,destination)
            else:
                print(f"Fetching data from ECFS: {ecfspath}")
                fetch_ecfs(obs,ecfs,year,month,destination)


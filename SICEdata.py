import os
import subprocess

def fetch_SICE(ecfs,year,month,destination):
    '''
    Fetch SICE data
    '''
    ecfspath = ecfs["PATH"]
    obspath = os.path.join(ecfspath,str(year))
    print(f"Attempting to fetch SICE data from {obspath}")
    yyyy=str(year)
    mm=str(month).zfill(2)
    yyyymm = "-".join([yyyy,mm,"??"])
    fpre = ecfs["FPRE"]
    suffix = ecfs["FILETYPE"]
    fnames = "_".join([fpre,yyyymm])+"."+suffix
    try:
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
    if len(files_found) != 0:
        cmd="ecp "+os.path.join(obspath,fnames)+' '+destination
        print("DEBUG SICE command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('SICE monthly file not found %s'%err)
    else:
        print(f"No data found for {year} and {month}")


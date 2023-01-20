import os
import subprocess

def fetch_RS(ecfs,year,month,destination):
    '''
    Fetch RS data
    '''
    ecfspath = ecfs["PATH"]
    yy=str(year)[0:2]
    mm=str(month).zfill(2)
    obspath = os.path.join(ecfspath)
    print(f"Attempting to fetch RS observations from {obspath}")
    suffix = ecfs["FILETYPE"]
    fpre = ecfs["FPRE"]
    fnames = "_".join([fpre,yy+mm+"????"])+"."+suffix
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
        #sys.exit(1)
    if len(files_found) != 0:
        cmd="ecp "+os.path.join(obspath,fnames)+' '+destination
        print("DEBUG GEUSv2 command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('GEUSv2 files not found %s'%err)
    else:
        print(f"No data found for {year}")


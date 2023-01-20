import os
import subprocess

def fetch_GEUS(ecfs,year,destination):
    '''
    Fetch SCAT data. In this case we grab .tar balls
    and uncompress them in destination directory
    '''
    ecfspath = ecfs["PATH"]
    yyyy=str(year)
    obspath = os.path.join(ecfspath,yyyy)
    print(f"Attempting to fetch GEUS observations from {obspath}")
    suffix = ecfs["FILETYPE"]
    fnames = "_".join([str(year),"???","ll"])+"."+suffix
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


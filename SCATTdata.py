import os
import subprocess

def fetch_SCATT(ecfs,year,month,destination):
    '''
    Fetch SCAT data. In this case we grab .tar balls
    and uncompress them in destination directory
    '''
    ecfspath = ecfs["PATH"]
    print("Attempting to fetch SCATT observations")
    obspath = os.path.join(ecfspath,str(year),str(month).zfill(2))
    fnames = "".join(["*",str(year)+str(month).zfill(2),".tar"])
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
        print("DEBUG SCATT command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('SCATT monthly file not found %s'%err)
    else:
        print(f"No data found for {year} and {month}")


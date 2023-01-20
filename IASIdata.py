import os
import subprocess
def fetch_IASI(ecfs,year,month,destination):
    '''
    NOTE: use a different directory for
    IASI data if date over 202004 
    This is only a very particular case,
    if date > 20204 use IASI_DATA2
    '''
    ecfspath = ecfs["PATH"]
    mm=str(month).zfill(2)
    yyyy=str(year)
    if int(year) == 2020 and month >= 4:
        subdir = "IASI_DATA2"
        ecfspath = os.path.join(ecfspath,subdir)
    elif int(year) == 2021:
        subdir = "IASI_DATA2"
        ecfspath = os.path.join(ecfspath,subdir)
    elif int(year) >= 2022:
        subdir = "IASI_DATA3"
        ecfspath = os.path.join(ecfspath,subdir,yyyy,mm)
    else:
        subdir = "IASI_DATA"
        ecfspath = os.path.join(ecfspath,subdir)
    print(f"Attempting to fetch IASI observations from {ecfspath}")
    obspath = ecfspath
    fnames = "".join(["*",yyyy+mm,"*"])
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
        print("DEBUG IASI command: %s"%cmd)
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print('IASI monthly file not found %s'%err)
    else:
        print(f"No data found for {year} and {month}")


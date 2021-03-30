# Get some data for the back extension
# Gets one month at a time

import sys
import logging
import configparser
import os
import subprocess
import re
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict
from pathlib import Path
import numpy as np
import fetch_utils as fu
import date_utils as du

def fetch_local(obs,fpre,fend,localpath,year,month,destination):
    if obs == 'RO':
        fu.fetch_RO_local(localpath,fpre,fend,year,month,destination)
    else:
        print(f"No local data available for {obs}!")

def fetch_ecfs(obs,ecfspath,year,month,destination):
    '''
    single call to ecfs according to DTG
    '''
    if obs == 'CONV':
        fu.fetch_CONV(ecfspath,year,month,destination)
    elif obs == 'RO':
        tarball = "_".join(["GPSRO",str(year)+str(month).zfill(2),"Precise"])+".tar"
        fu.fetch_RO(ecfspath,tarball,destination)
    else:
        print(f"No implementation for {ecfspath} just yet!")
        print("Currently doing ONLY CONV and RO observations")
        sys.exit()


def run_comms(comms):
    for cmd in comms:
        print(f"Running: {cmd}")
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print(f"Error in subprocess {err}")
            print(ret)

def read_yaml(file_path):
    import yaml
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def fetch_data(yaml_args):
    year = yaml_args["CL_ARGS"]["YEAR"]
    month = yaml_args["CL_ARGS"]["MONTH"]
    obs = yaml_args["CL_ARGS"]["OBS"]
    fpre = yaml_args["OBS"][obs]["FPRE"]
    fend = yaml_args["OBS"][obs]["FEND"]
    scratch =yaml_args["SCRATCH"]
    obsdir = yaml_args["OBS"][obs]["OBSDIR"]
    ecfspath = yaml_args["OBS"][obs]["ECFSPATH"]
    localpath = yaml_args["OBS"][obs]["LOCALPATH"] #Use this path if defined
    #check first if data already there
    destination = fu.create_destination(obsdir,year,month,scratch)
    files_present = fu.test_if_present(obs,year,month,fpre,destination)
    if not files_present:
        if len(localpath) != 0:
            print(f"Fetching data locally from: {localpath}")
            fetch_local(obs,fpre,fend,localpath,year,month,destination)
        else:
            print(f"Fetching data from ECFS: {ecfspath}")
            fetch_ecfs(obs,ecfspath,year,month,destination)
    else:
        print(f"Observations for {args.year}/{args.month} already copied!")

def main(args):
    HHOME = "/ws/home/ms/dk"
    #Read arguments from the yaml file
    yaml_args = read_yaml(args.yfile)

    #Include the command line arguments
    yaml_args["CL_ARGS"] = {}
    yaml_args["CL_ARGS"]["OBS"] = args.obs


    # Check user's scratch directory and add it to yml options
    cmd = "echo $SCRATCH"
    ret = subprocess.check_output(cmd,shell=True)
    SCRATCH = ret.rstrip().decode('utf-8')
    #Change final dest to tmp location if only testing
    if args.test:
        print("This is a test!")
        SCRATCH = os.path.join(SCRATCH,"tmp")
    yaml_args["SCRATCH"] = SCRATCH
    
    #obsdir = yaml_args["OBS"][args.obs]

    #if year and month given, fetch data for that year and month
    # Otherwise go through all streams

    if not args.auto:
        if args.year is None or args.month is None:
            print(args.help)
            sys.exit(1)
        else:
            yaml_args["CL_ARGS"]["YEAR"] = args.year
            yaml_args["CL_ARGS"]["MONTH"] = args.month
            fetch_data(yaml_args)
    else:
        #streams = [st for st in yaml_args["STREAMS"].keys()]
        streams = [st for st in yaml_args["STREAMS"].keys() if yaml_args["STREAMS"][st]["ACTIVE"]]
        print(f"Active streams: {streams}")
        yyyymm = []
        for st in streams:
            #The hhome path is only needed to read the progress.log file
            hh = os.path.join(HHOME,yaml_args["STREAMS"][st]["USER"],"hm_home")
            DTG = du.get_current_dtg(hh,st)
            year,month = du.calc_year_month(DTG,mdays=15)
            print(f"Latest year and month from {st} progressMCI.log: {year} {month}")
            if year != None and month != None:
                yyyymm.append(year+"_"+month)
            else:
                print(f"Doing nothing for {st}")
        #remove all repeated values, so I dont request a month year more than once
        yyyymm = list(set(yyyymm))
        for ym in yyyymm:
            args.year = int(ym.split("_")[0])
            args.month = int(ym.split("_")[1])
            if args.year != None and args.month != None:
                print(f"From progressMCI.log: need to fetch {args.year} {args.month}")
                yaml_args["CL_ARGS"]["YEAR"] = args.year
                yaml_args["CL_ARGS"]["MONTH"] = args.month
                fetch_data(yaml_args)
            else:
               print("Something went wrong reading the year or month from progressMCI.log")
               print(f"year: {args.year}, month: {args.month}")

if __name__=='__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='''
            Fetch data from ecfs or local path to predetermined locations in $SCRATCH for a given
            month and year

            Example usage: python3 call_ecfs.py -year 1997 -month 1 -obs CONV (for specific year and month)
                           python3 call_ecfs.py -auto -obs CONV (it will read latest DTG from MCI progress file of corresponding stream) ''',formatter_class=RawTextHelpFormatter)

    parser.add_argument('-month',metavar='month to fetch (integer)',
                        type=int,
                        default=None,
                        required=False)

    parser.add_argument('-year',metavar='year to fetch (integer)',
                        type=int,
                        default=None,
                        required=False)
   
    parser.add_argument('-obs',metavar='Observation source to be processed (currently only CONV or RO)',
                        type=str,
                        default="CONV",
                        required=False)
    #if this one is used it will get the year and month from the latest progress.log
    parser.add_argument('-auto',action='store_true',help="If selected it will decide month and year based on current progressMCI.log") # set to false by default
    parser.add_argument('-test',action='store_true',help="For testing. It will write all data in directories $SCRATCH/tmp") # set to false by default
    parser.add_argument('-yfile',metavar='name of the yaml config file (default is streams.yaml)',
                        type=str,
                        default="./streams.yaml",
                        required=False)

    args = parser.parse_args()
    args.help =  parser.print_help()
    main(args)
    #List of observation types
    # CONV,RO
    #If auto is not set, ask for params
    #Normally running it in automatic mode, so it goes through all the streams
    print("call_ecfs FINISHED")

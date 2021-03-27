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

epath = 'ec:/rml/precise/obs/obsoul/locobs/v11jun20/'

def obs_path(obs,year,month):
    obs_dirs = {'CONV':'LocalObsdata' ,
                'OSISAF':os.path.join('OSISAF_data',str(year)) }
    return obs_dirs[obs]

def fetch_ecfs(obs,year,month,scratch,destination):
    '''
    single call to ecfs according to DTG
    '''
    found_files = None
    files_to_copy = None
    copy_com = None
    print("Checking observations %s"%obs)
    if obs == 'CONV':
        fu.fetch_CONV(obs,year,month,scratch,destination)
    elif obs == 'RO':
        fu.fetch_RO(obs,year,month,scratch,destination)
    else:
        print(f"No implementation for {obs} just yet!")
        print("Currently doing ONLY conventional observations (obsoul)")
        sys.exit()
    return copy_com


def run_comms(comms):
    for cmd in comms:
        print(f"Running: {cmd}")
        try:
            ret=subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as err:
            print("Error in subprocess {}".format(err))

def read_yaml(file_path):
    import yaml
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def fetch_data(yaml_args):
    obs = yaml_args["OBS"]
    year = yaml_args["CL_ARGS"]["YEAR"]
    month = yaml_args["CL_ARGS"]["MONTH"]
    files_present = fu.check_if_present(obs,year,month)
    if not files_present:
        fu.create_destination(obsdir,year,month,scratch)
        fetch_ecfs(args.obs,args.year,args.month,scratch,destination)
    else:
        print(f"Observations for {args.year}/{args.month} already copied!")

def main(args):
    #Read arguments from the yaml file
    yaml_args = read_yaml(args.yfile)
    #Include the CL arguments
    yaml_args["CL_ARGS"] = {}
    yaml_args["CL_ARGS"]["OBS"] = args.obs
    scratch = yaml_args["HARMONIE"]["SCRATCH"]
    #destination = os.path.join(scratch,yaml_args["OBSFILES"][args.obs]["SCRPATH"])
    # If user is not nhe, copy all to local tmp dir
    cmd = "echo $USER"
    ret = subprocess.check_output(cmd,shell=True)
    USER = ret.rstrip().decode('utf-8')
    obsdir = yaml_args["OBSFILES"][args.obs]
    if USER != "nhe":
        scratch = scratch.replace("nhe",USER+"/tmp")
    import pdb
    pdb.set_trace()

    #if year and month given, fetch data for that year and month
    # Otherwise go through all streams

    if not args.auto:
        if args.year == None or args.month == None:
            print("Please provide year and month!")
            sys.exit(1)
        else:
            yaml_args["CL_ARGS"]["YEAR"] = args.year
            yaml_args["CL_ARGS"]["MONTH"] = args.month
            fetch_data(yaml_args)
    else:
        streams = [st for st in data["STREAMS"].keys()]
        yyyymm = []
        for st in streams:
            hh = os.path.join(yaml_args["HARMONIE"]["HHOME"],yaml_args["STREAMS"][st]["USER"],"hm_home")
            DTG = du.get_current_dtg(hh,st)
            year,month = du.calc_year_month(DTG,mdays=15)
            print(f"Latest year and month from {st} progressMCI.log: {year} {month}")
            if year != None and month != None:
                yyyymm.append(year+"_"+month)
            else:
                print(f"Doing nothing for {st}")
        #remove all repeated
        yyyymm = list(set(yyyymm))
        for ym in yyyymm:
            args.year = int(ym.split("_")[0])
            args.month = int(ym.split("_")[1])
            if args.year != None and args.month != None:
                print(f"From progressMCI.log: need to fetch {args.year} {args.month}")
                fetch_data(args,yaml_args)

if __name__=='__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='''Copies a whole month
            Example usage: python3 call_ecfs.py -year 1997 -month 1 -obs CONV ''',formatter_class=RawTextHelpFormatter)

    parser.add_argument('-month',metavar='month to pull out (integer)',
                        type=int,
                        default=None,
                        required=False)

    parser.add_argument('-year',metavar='year to pull out (integer)',
                        type=int,
                        default=None,
                        required=False)
   
    parser.add_argument('-obs',metavar='Observation source to be processed',
                        type=str,
                        default="CONV",
                        required=False)
    #if this one is used it will get the year and month from the latest progress.log
    parser.add_argument('-auto',action='store_true') # set to false by default
    parser.add_argument('-yfile',metavar='name of the yaml config file',
                        type=str,
                        default="./streams.yaml",
                        required=False)

    args = parser.parse_args()
    main(args)
    #List of observation types
    # CONV,RO
    #If auto is not set, ask for params
    #Normally running it in automatic mode, so it goes through all the streams
    print("call_ecfs FINISHED")

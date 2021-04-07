#!/bin/bash

module load python3

#Usage
#
# Type python3 ./call_ecfs.py for full options

# Examples:
# 
# python3 ./call_ecfs.py -auto -obs OBSTYPE
# This will copy the observation type OBSTYPE if latest month and year in stream's MCI log is less than 15 days

# python3 ./call_ecfs.py -month 1 -year 1998 -obs OBSTYPE
# This will copy the observation type OBSTYPE for given year and month
# 
# Add -test option to test in local $SCRATCH/tmp directory (useful if testing in user other than running streams)


#python3 ./call_ecfs.py -auto -obs CONV -test
#python3 ./call_ecfs.py -auto -obs RO -test
#python3 ./call_ecfs.py -month 8 -year 2020 -obs RO 

#python3 ./call_ecfs.py -auto -obs CONV -test
#python3 ./call_ecfs.py -auto -obs RO -test -mdays 25
python3 ./call_ecfs.py -auto -obs CRYO -test -mdays 25

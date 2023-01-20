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

# available: CONV,CRYO,OSISAF,RO,IASI,GEUS

# expected: CONV,CRYO,GEUSv2,OSISAF,RO,RS,IASI_DATA,SCATT


#python3 ./call_ecfs.py -auto -obs CONV -test
#python3 ./call_ecfs.py -auto -obs RO -test
#python3 ./call_ecfs.py -month 8 -year 2020 -obs RO 

#python3 ./call_ecfs.py -auto -obs CONV -test
#python3 ./call_ecfs.py -auto -obs RO -test -mdays 25
#python3 ./call_ecfs.py -auto -obs CRYO -test -mdays 25
MDAYS=30 #if I want to wait longer before checking for data
#Month and year for specifying arguments below
MM=08 #integer, no leading zero
YYYY=2020 #integer

#Calls for carra_pan.
#cd /home/ms/dk/nhx/scr/check_transfer_data/pyecf
#python3 ./call_ecfs.py -auto -obs IASI -yfile streams_pan.yaml 
#python3 ./call_ecfs.py -auto -obs SCATT -yfile streams_pan.yaml
#python3 ./call_ecfs.py -auto -obs CONV -yfile streams_pan.yaml

#Examples to call with month and year
#python3 ./call_ecfs.py -obs CONV -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs OSISAF -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs CRYO -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs RO -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs SICE -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
python3 ./call_ecfs.py -obs GEUS -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
exit 0

#python3 ./call_ecfs.py -auto -obs CONV -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs CRYO -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs RO -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs OSISAF -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs CRYO -yfile streams_carra.yaml -test -mdays 20
#python3 ./call_ecfs.py -auto -obs RO -yfile streams_carra.yaml -test

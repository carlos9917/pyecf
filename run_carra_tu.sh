#!/usr/bin/bash
#SBATCH --mem-per-cpu=16GB
#SBATCH --time=8:00:00
#SBATCH --account=c3srra

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
MDAYS=0 #if I want to wait longer before checking for data
#Month and year for specifying arguments below
MM=08 #integer, no leading zero
YYYY=2022 #integer

#Examples to call with month and year, test run (output in $SCRATCH/tmp)
#python3 ./call_ecfs.py -obs CONV -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs OSISAF -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs CRYO -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs RO -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs SICE -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
#python3 ./call_ecfs.py -obs GEUS -yfile streams_carra_tu.yaml -month $MM -year $YYYY -test
MDAYS=200

if [ -z $1 ]; then
    echo "No obs type provided. Doing all"	
    python3 ./call_ecfs.py -obs CONV -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs OSISAF -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs CRYO -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs RO -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test 
    python3 ./call_ecfs.py -obs SICE -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs GEUS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    exit 0
else
    OBS=$1	
    python3 ./call_ecfs.py -obs $OBS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
fi

#python3 ./call_ecfs.py -auto -obs CONV -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs CRYO -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs RO -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs OSISAF -yfile streams_carra.yaml -test -mdays $MDAYS
#python3 ./call_ecfs.py -auto -obs CRYO -yfile streams_carra.yaml -test -mdays 20
#python3 ./call_ecfs.py -auto -obs RO -yfile streams_carra.yaml -test

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
# Add -test option to test in local $SCRATCH/tmp directory (useful for not replacing the current path)


# available obs types: CONV,CRYO,OSISAF,RO,IASI,GEUS,RS,IASI,SICE,SCATT

# Set the minimum number of days (default is 15 in call_ecfs)
MDAYS=10 #if I want to wait longer before checking for data

if [ -z $1 ]; then
    echo "No obs type provided. Doing all"	
    for OBS in CONV OSISAF CRYO RO RS IASI SICE SCATT; do #GEUS should not be needed, I think...
      echo "Processing $OBS"	    
      python3 ./call_ecfs.py -obs $OBS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    done
    #python3 ./call_ecfs.py -obs CONV -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs OSISAF -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs CRYO -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs RO -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs RS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs SICE -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    ##python3 ./call_ecfs.py -obs GEUS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #python3 ./call_ecfs.py -obs SCATT -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
    #exit 0
else
    OBS=$1	
    echo "Doing only $OBS"
    python3 ./call_ecfs.py -obs $OBS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto 
fi


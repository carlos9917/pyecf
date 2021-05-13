#!/bin/ksh
#using this script with nhe

export PATH=/usr/local/bin:$PATH
. ~/.profile
. ~/.kshrc
$@ 

today=`date +'%Y%m%d_%H%M%S'`
echo Fetching observations on $today
# Examples:
# 
# python3 ./call_ecfs.py -auto -obs OBSTYPE
# This will copy the observation type OBSTYPE if latest month and year in stream's MCI log is less than 15 days

# python3 ./call_ecfs.py -month 1 -year 1998 -obs OBSTYPE
# This will copy the observation type OBSTYPE for given year and month
# 
# Add -test option to test in local $SCRATCH/tmp directory (useful if testing in user other than running streams)


echo ">>>> Running call_ecfs.py <<<<"
module load python3
#module list
cd /home/ms/dk/nhe/scr/pyecf
python3 ./call_ecfs.py -auto -obs CONV -yfile ./streams_danra.yaml
python3 ./call_ecfs.py -auto -obs RO -yfile ./streams_danra.yaml
echo ">>>> Finished <<<<"

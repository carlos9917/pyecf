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

copy_data()
{
# Set the minimum number of days (default is 15 in call_ecfs)
MDAYS=10 #set this if I want to wait longer before checking for data

# TODO: uncomment following 6 lines, comment lines 7 and 8 after this comment
dtgstart=$(date -d "`date +%Y%m01` -2 month" +%Y%m%d)
echo "Current dtg: $dtgstart"
YYYY=$(echo $dtgstart | awk '{print substr($1,1,4)}')
mm=$(echo $dtgstart | awk '{print substr($1,5,2)}')
MM=$(echo $mm | sed 's/^0*//')
echo "Doing $YYYY $MM, according to $dtgstart"
#test:
#MM=2 #integer, no leading zero
#YYYY=2023 #integer
#copy data for this month
python3 ./call_ecfs.py -obs CONV -yfile streams_carra_tu.yaml -month $MM -year $YYYY
python3 ./call_ecfs.py -obs OSISAF -yfile streams_carra_tu.yaml -month $MM -year $YYYY
python3 ./call_ecfs.py -obs CRYO -yfile streams_carra_tu.yaml -month $MM -year $YYYY
python3 ./call_ecfs.py -obs RO -yfile streams_carra_tu.yaml -month $MM -year $YYYY 
python3 ./call_ecfs.py -obs RS -yfile streams_carra_tu.yaml -month $MM -year $YYYY
python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -month $MM -year $YYYY 
python3 ./call_ecfs.py -obs SICE -yfile streams_carra_tu.yaml -month $MM -year $YYYY 
python3 ./call_ecfs.py -obs GEUS -yfile streams_carra_tu.yaml -month $MM -year $YYYY 
python3 ./call_ecfs.py -obs SCATT -yfile streams_carra_tu.yaml -month $MM -year $YYYY 

#extra: copy data for next month for IASI:
dtgstart=$(date -d "`date +%Y%m01` -1 month" +%Y%m%d)
YYYY=$(echo $dtgstart | awk '{print substr($1,1,4)}')
mm=$(echo $dtgstart | awk '{print substr($1,5,2)}')
MM=$(echo $mm | sed 's/^0*//')
echo "Doing also $YYYY $MM for IASI, since the data for the following month is also needed there"
python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -month $MM -year $YYYY 
exit
}

follow_cli()
{
# This example copies everything to $SCRATCH/tmp Get rid of the "-test" option to copy to directories under $SCRATCH
if [ -z $1 ]; then
    echo "No obs type provided. Doing all"	
    python3 ./call_ecfs.py -obs CONV -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs OSISAF -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs CRYO -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs RO -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs RS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs IASI -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test 
    python3 ./call_ecfs.py -obs SICE -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs GEUS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    python3 ./call_ecfs.py -obs SCATT -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
    exit 0
else
    OBS=$1	
    python3 ./call_ecfs.py -obs $OBS -yfile streams_carra_tu.yaml -mdays $MDAYS -auto -test
fi
}

#follow_cli

copy_data

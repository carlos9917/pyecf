#Scripts to fetch observational data from ecfs to use with Harmonie runs at ECMWF

Script to call ecfs commands from cca.
Needs to run from cca. It will copy all data in $SCRATCH

Currently only copying CONV,RO, CRYO and OSISAF data for the DANRA project.


## Config file

All params like paths and obs needed are defined in yaml file streams.yaml
Create a new file for your streams (ie streams_carra.yaml)

There are 2 sections in the yaml file:
- STREAMS
- OBS

### STREAMS
Indicate stream ini and end date, user (to define path) and if the stream is active
STREAMS:
  dkrea198909:
    BEG_DATE: 1989090100
    END_DATE: 1994090123
    USER: nhe
    ACTIVE: False

### OBS
Define observation types in the OBS section
OBS:
  CONV:
    ECFSPATH: "ec:/rml/precise/obs/obsoul/locobs/v11jun20"
    LOCALPATH: path
    OBSDIR: "LocalObsdata"
    SUBDIR: "YYYY/MM"

If LOCALPATH defined inside the ECFS section it will copy local data instead of copying from ECFS
(currently only for RO)

#Scripts to fetch observational data from ecfs to use with Harmonie runs at ECMWF

Needs to run from cca

Currently only copying CONV and RO for the DANRA project

## Config file
All params like paths and obs needed are defined in yaml file streams.yaml

Indicate stream ini and end date, user (to define path) and if the stream is active
STREAMS:
  dkrea198909:
    BEG_DATE: 1989090100
    END_DATE: 1994090123
    USER: nhe
    ACTIVE: False

Define observation types in the OBS section
OBS:
  CONV:
    ECFSPATH: "ec:/rml/precise/obs/obsoul/locobs/v11jun20"
    OBSDIR: "LocalObsdata"
    SUBDIR: "YYYY/MM"



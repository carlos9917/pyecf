# Funcions dealing with dates

import subprocess
import os
import numpy as np
from collections import OrderedDict
import re
from datetime import datetime
from datetime import timedelta

#hhome = "/ws/home/ms/dk/nhx/hm_home"

def calc_year_month(cdate,mdays=15):
    domonth = None
    doyear = None
    current = datetime.strptime(cdate,"%Y%m%d%H")
    month = cdate[4:6]
    year = cdate[0:4]
    ndays = days_month(month,year)
    final_day = datetime.strptime(cdate[0:6]+str(ndays),"%Y%m%d")
    delta = (final_day - current).days
    next_dtg = current + timedelta(days=delta+1)
    if delta < mdays:
       domonth = datetime.strftime(next_dtg,"%m") 
       doyear = datetime.strftime(next_dtg,"%Y") 
       #print(f"Need to fetch {doyear} {domonth} ({delta} days until end of the month)")
    else:
       print(f"No need to fetch data yet, since still {delta} days until end of the current month")

    return doyear, domonth

def days_month(month,year):
    month = int(month)
    year = int(year)
    ndays=999
    months31=[1, 3, 5, 7, 8, 10, 12]
    months30=[4, 6, 9, 11]
    if month in months31:
        ndays=31
    elif month in months30:
        ndays=30
    elif month == 2:
        #Evaluation for leap years from https://bash.cyberciti.biz/time-and-date/find-whether-year-ls-leap-or-not/
        if year % 4 != 0 or year % 400 != 0 and year % 100 == 0:
            ndays=28
        else:
            ndays=29
    return ndays


def get_current_dtg(hhome,stream):
    '''
    Get dtg from progress.log of the stream
    '''
    pfile=os.path.join(hhome,stream,'progressMCI.log')
    with open(pfile, 'r') as f:
        lines=f.readlines()
        #print(lines[0])
        cdate=re.search('DTGMCI=(.*) export',lines[0]).group(1)

    print(f"Current date in {stream}: {cdate}")
    return cdate

def split_dtg(dtg):
    year = dtg[0:4]
    month = dtg[4:6]
    day = dtg[6:8]
    return year, month, day

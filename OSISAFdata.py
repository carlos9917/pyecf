#TODO later: define every type as a class 
# Class for OSISAF data

class OSISAFdata(object):
    def __init__(self,year=None, month=None, ecfs=None, obsdir=None, scratch = None):
        self.year = year
        self.month = month
        self.mdays = mdays
        self.scratch = scratch
        self.ecfs = ecfs
        self.obs = obs
    def fetch_ecfs(self):
        pass
    def fetch_local(self):

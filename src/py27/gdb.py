# C:\Python27\ArcGIS10.7
# we wish to install the GDB from ArcGIS, not bleeding edge ArcPro

import arcpy
import os


class Gdb(object):

    def __init__(self):

        self.sdeconn = os.environ['SDEFILE']

    def enable(self,
               authfile):
            
        # dont use this
        pass



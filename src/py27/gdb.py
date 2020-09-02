# C:\Python27\ArcGIS10.7
# we wish to install the GDB from ArcGIS, not bleeding edge ArcPro

import arcpy
import os


class Gdb(object):

    def __init__(self):

        self.sdeconn = os.environ['SDEFILE']

    def enable(self,
               authfile):
            

        try:
            arcpy.EnableEnterpriseGeodatabase_management(self.sdeconn, 
                                                         authfile)
        
        except:

            print "{0}".format(arcpy.GetMessages())
            print "using {0} and {1}".format(self.sdeconn,
                                             authfile)
            raise ValueError('Failure on enable enterprise gdb from ArcGIS')

        
        print "".format(arcpy.GetMessages())



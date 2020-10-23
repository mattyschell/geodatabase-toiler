import arcpy
import os
import logging

# monkey patch python 2.7 arcmap functionality
# where arcgis pro is busted

class Fc(object):

    def __init__(self
                ,gdb 
                ,name):

        # gdb object should know arcpy2path
        # from environemental or default
        self.gdb = gdb
        # ex BUILDING
        self.name = name.upper()
        # esri tools usually expect this C:/sdefiles/bldg.sde/BUILDING
        # also acceptable: C:/sdefiles/bldg.sde/BLDG.BUILDING
        self.featureclass = gdb.sdeconn + "/" + self.name

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def createversionedviews(self):

        # https://desktop.arcgis.com/en/arcmap/10.6/tools/data-management-toolbox/create-versioned-view.htm

        self.logger.info('Py27 is Creating versioned views for {0}'.format(self.name)) 

        arcpy.CreateVersionedView_management(self.featureclass)

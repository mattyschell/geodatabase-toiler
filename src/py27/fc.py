import arcpy
import os
import logging

# monkey patch python 2.7 arcmap functionality
# where arcgis pro (or compatibility) is busted

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
        self.logger.info('Like so  arcpy.CreateVersionedView_management({0})'.format(self.featureclass)) 

        arcpy.CreateVersionedView_management(self.featureclass)

    def enablearchiving(self):

        self.logger.info('Py27 is Creating versioned views for {0}'.format(self.name)) 
        self.logger.info('Like so  arcpy.CreateVersionedView_management({0})'.format(self.featureclass)) 

        arcpy.EnableArchiving_management(self.featureclass)

    def addglobalids(self):

        # with a 10.7 enterprise geodatabase and versioned views
        # (which are created by default now)
        # it is not possible to add globalids from arcgis pro or arcmap 10.8+
        # the globalid tools fail with new columns populated with all {00-00}s
        # and the versioned view gone.  Error is from the DBMS and comes out 
        # on the ESRI side as the famous 99999s
        # We must monkey patch global id creation from  ArcGIS Desktop 10.7
        # this is a lot of chit chat for one line of code. Stop being obnoxious
        arcpy.AddGlobalIDs_management(self.featureclass)

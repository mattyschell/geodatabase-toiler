import arcpy
import logging
import pathlib
from subprocess import call
#
import gdb
import cx_sde

class Fc(object):

    def __init__(self
                ,gdb 
                ,name):

        # gdb object
        self.gdb = gdb
        # ex BUILDING
        self.name = name.upper()
        # esri tools usually expect this C:/sdefiles/bldg.sde/BUILDING
        # also acceptable: C:/sdefiles/bldg.sde/BLDG.BUILDING
        self.featureclass = gdb.sdeconn + "/" + self.name

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def getfields(self):

        desc = arcpy.Describe(self.featureclass)
        fields = desc.fields
        fieldsameslist = []
        for field in fields:
            fieldsameslist.append(field.name)

        return fieldsameslist

    def exists(self):

        return arcpy.Exists(self.featureclass)

    def delete(self):

        self.logger.info('deleting {0}'.format(self.name)) 

        arcpy.Delete_management(self.featureclass)

    def locksexist(self):

        if arcpy.TestSchemaLock(self.featureclass):

            # "True A schema lock can be applied to the dataset"
            return False

        else:

            return True

    def version(self):

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/register-as-versioned.htm

        self.logger.info('versioning {0}'.format(self.name)) 

        arcpy.RegisterAsVersioned_management(self.featureclass
                                            ,"NO_EDITS_TO_BASE")

        # https://support.esri.com/en/technical-article/000023226
        # When an ArcGIS 10.8 / ArcGIS Pro 2.5 (or newer) client connects to a 
        # 10.7.1, or earlier, release of an Enterprise geodatabase in Oracle, 
        # and registers the data as versioned, the versioned view is not created
        # for the associated table or feature class.

        #py2versionedviews = pathlib.Path(__file__).parent.parent \
        #                                          .joinpath('py27') \
        #                                          .joinpath('create_versionedviews.py')
            
        # see gdb class for this path, perhaps 'C:\Python27\ArcGIS10.6'
        #callcmd =  f"{self.gdb.arcpy2path} {py2versionedviews} {self.name} " 
        #callcmd = r'{0} {1} {2}'.format(self.gdb.arcpy2path, py2versionedviews, self.name)

        #try:
                
            #self.logger.info('attempting to create versioned views from py27 using {0}'.format(callcmd))

            #C:\Python27\ArcGIS10.6\python.exe C:\matt_projects\geodatabase-toiler\src\py27\create_versionedviews.py TOILERTESTFC
                
        #    exit_code = call(callcmd)

            #self.logger.info('exit code is {0}'.format(exit_code))

        #except:

        #    self.logger.error('failure creating versioned views with {0}'.format(callcmd))    
        #    raise ValueError(f"failure creating versioned views with {callcmd}") 
        
    def trackedits(self):

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/enable-editor-tracking.htm
        # this will create fields only if they dont exist
        # I am gonna fix the field names here.  Reminder that our goal is to 
        # be opinionated and consistent across anything we manage 

        self.logger.info('enabling editor tracking on {0}'.format(self.name)) 

        arcpy.EnableEditorTracking_management(self.featureclass,
                                              "CREATED_USER",
                                              "CREATED_DATE",
                                              "LAST_EDITED_USER",
                                              "LAST_EDITED_DATE",
                                              "NO_ADD_FIELDS",
                                              "UTC")

    def grantprivileges(self
                       ,user
                       ,edits='GRANT'): # or AS_IS 

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/change-privileges.htm
        # caller should know who editors are we dont concern ourselves here

        # always grant select, edits are GRANT or AS_IS for grant select only
        # The nobs and dials on this tool are confounding
        
        self.logger.info('granting privileges on {0} to {1}'.format(self.name
                                                                   ,user))    

        arcpy.ChangePrivileges_management(self.featureclass 
                                         ,user
                                         ,"GRANT" 
                                         ,edits)  

    def index(self
             ,column):

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-attribute-index.htm          
        # unique indexes cant be specified for multiversioned tables   
        
        self.logger.info('indexing column {0} on {1}'.format(column
                                                            ,self.name))      

        # BUILDINGBINIX 
        # BUILDING_HISTORICDOITT_IDIX = 27 careful friend
        arcpy.AddIndex_management(self.featureclass
                                 ,column
                                 ,'{0}{1}{2}'.format(self.name 
                                                    ,column
                                                    ,'IX'))

import arcpy
import logging
import pathlib
import subprocess

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
        self.featureclass = self.gdb.sdeconn + "/" + self.name

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

        logging.info('deleting {0}'.format(self.name)) 

        if self.exists():

            desc = arcpy.da.Describe(self.featureclass)

            if 'isArchived' in desc:

                if desc['isArchived'] == True:

                    # disable archving and axe the _H table
                    arcpy.DisableArchiving_management(self.featureclass,
                                                    'DELETE') 

            arcpy.Delete_management(self.featureclass)

    def locksexist(self):

        if arcpy.TestSchemaLock(self.featureclass):

            # "True A schema lock can be applied to the dataset"
            return False

        else:

            return True

    def interpret(self
                 ,resobject):

        # could also work with resobject.status 
        output = 0

        if 'succeeded' not in resobject.getMessages().lower():

            output = 1
            logging.warn('response code is {0}'.format(resobject.status))
            logging.warn('response messages are {0}'.format(resobject.getMessages()))

        return output

    def version(self):

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/register-as-versioned.htm

        logging.info('versioning {0}'.format(self.name)) 

        arcpy.RegisterAsVersioned_management(self.featureclass
                                            ,"NO_EDITS_TO_BASE")

        # https://support.esri.com/en/technical-article/000023226
        # When an ArcGIS 10.8 / ArcGIS Pro 2.5 (or newer) client connects to a 
        # 10.7.1, or earlier, release of an Enterprise geodatabase in Oracle, 
        # and registers the data as versioned, the versioned view is not created
        # for the associated table or feature class.

        # I cant get this shell out to python27 to work
        # so like I dummy I'm gonna print it to the screen for now
        # the test will fail until I (or esri) get it right, thats honest at least

        py2versionedviews = pathlib.Path(__file__).parent.parent \
                                                  .joinpath('py27') \
                                                  .joinpath('create_versionedviews.py')
            
        # see gdb class for this path, perhaps 'C:\Python27\ArcGIS10.6'
        callcmd = r'{0} {1} {2}'.format(self.gdb.arcpy2path, py2versionedviews, self.name)
        logging.info('YOU MUST CREATE versioned views from py27 using {0}'.format(callcmd))
        logging.info('YOU YES YOU MUST call this: {0}'.format(callcmd))

        # From a script run a postprocess something like:
        # C:\Python27\ArcGIS10.6\python.exe C:\matt_projects\geodatabase-toiler\src\py27\create_versionedviews.py TOILERTESTFC
            
        # exit_code = subprocess.call(callcmd,shell=True)
        # exit_code = subprocess.run([self.gdb.arcpy2path, 'C:\matt_projects\geodatabase-toiler\src\py27\create_versionedviews.py'])
        # subprocess.Popen(["virtualenv1/bin/python", "my_script.py"])

        # attempts above yield
        #  File "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Lib\site.py", line 177
        #file=sys.stderr)
        #    ^
        # SyntaxError: invalid syntax

    def trackedits(self):

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/enable-editor-tracking.htm
        # this will create fields only if they dont exist
        # I am gonna fix the field names here.  Reminder that our goal is to 
        # be opinionated and consistent across anything we manage 

        logging.info('enabling editor tracking on {0}'.format(self.name)) 

        return self.interpret(arcpy.EnableEditorTracking_management(self.featureclass
                                                                   ,'CREATED_USER'
                                                                   ,'CREATED_DATE'
                                                                   ,'LAST_EDITED_USER'
                                                                   ,'LAST_EDITED_DATE'
                                                                   ,'NO_ADD_FIELDS'
                                                                   ,'UTC'))

    def grantprivileges(self
                       ,user
                       ,edits='GRANT'): # or AS_IS 

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/change-privileges.htm
        # caller should know who editors are we dont concern ourselves here

        # always grant select, edits are GRANT or AS_IS for grant select only
        # The nobs and dials on this tool are confounding
        
        logging.info('granting privileges on {0} to {1}'.format(self.name
                                                               ,user))    

        return self.interpret(arcpy.ChangePrivileges_management(self.featureclass 
                                                               ,user
                                                               ,'GRANT'
                                                               ,edits))  

    def index(self
             ,column
             ,unique=False):

        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-attribute-index.htm          
        # unique indexes cant be specified for multiversioned tables   
        
        logging.info('indexing column {0} on {1}'.format(column
                                                        ,self.name))      

        # BUILDINGBINIX 
        # BUILDING_HISTORICDOITT_IDIX = 27 careful friend
        return self.interpret(arcpy.AddIndex_management(self.featureclass
                                                       ,column
                                                       ,'{0}{1}{2}'.format(self.name 
                                                                          ,column
                                                                          ,'IX')
                                                       ,unique))

    def analyze(self
               ,components=['BUSINESS','ADDS','DELETES']):

        return self.interpret(arcpy.Analyze_management(self.featureclass
                                                      ,components))

    def rebuildindexes(self):

        # https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/rebuild-indexes.htm

        return self.interpret(arcpy.RebuildIndexes_management(self.gdb.sdeconn
                                                             ,'NO_SYSTEM'
                                                             ,self.name
                                                             ,'ALL'))

    def enablearchiving(self):

        desc = arcpy.Describe(self.featureclass)
        
        if desc.IsArchived == False: 
            return self.interpret(arcpy.EnableArchiving_management(self.featureclass))
        else:
            return 0

    def exporttoshp(self
                   ,outputdir
                   ,outputname):

        # print('fc2fc {0} {1} {2}'.format(self.featureclass, outputdir, outputname))
        
        arcpy.FeatureClassToFeatureClass_conversion(self.featureclass
                                                   ,outputdir
                                                   ,outputname)

    # TODO exportogeopackage if ESRI ever fills in some functionality in
    # https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/an-overview-of-the-to-geopackage-toolset.htm

    # TODO exportogeojson if ESRI tool does something other than error 99999 (guess: sdo_geometry not supported)
    # For now export to shp, then ogr2ogr to other formats.  Classic




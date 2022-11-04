import arcpy
import os
import pathlib
import logging
import configparser
from subprocess import call
#
import cx_sde


class Gdb(object):

    def __init__(self
                ,arcpy2path=None
                ,database='oracle'):

        self.sdeconn = os.path.normpath(os.environ['SDEFILE'])

        #https://pro.arcgis.com/en/pro-app/arcpy/functions/workspace-properties.htm
        desc = arcpy.Describe(self.sdeconn)
        connProps = desc.connectionProperties
        self.username = connProps.user.upper()

        # database property doesnt exist? This mess is our best option
        # strong SQL Server vibes from these props
        # dbsde:oracle11g:DITGSDV1
        self.databasestring = connProps.instance 
        
        # when we need to call oldskool python 27 under arcgis
        if arcpy2path is None:
            self.arcpy2path = os.path.join(os.path.normpath('C:\Python27\ArcGIS10.6')
                                          ,'python.exe')
        else:
            self.arcpy2path = os.path.join(os.path.normpath(arcpy2path)
                                          ,'python.exe')

        # used only as fetch path to all SQLs we will execute
        # for now src\sql_<oracle>
        # life goals: src\sql_<postgres> switch and life is beautiful
        # really tho I do too much in SQL, should RTFM, convert SQLs to arcpy 
        self.database = database

        self.administrator =  self.isadministrator()

    def interpret(self
                 ,resobject):

        # could also work with resobject.status 
        output = 0

        if 'succeeded' not in resobject.getMessages().lower():

            output = 1
            logging.warn('response code is {0}'.format(resobject.status))
            logging.warn('response messages are {0}'.format(resobject.getMessages()))

        return output

    def isadministrator(self):

        if self.database == 'oracle':

            try:
                sdereturn = cx_sde.selectavalue(self.sdeconn
                                               ,self.fetchsql('{0}'.format('isadministrator.sql')))
            except:
                return False
                
            if sdereturn == 1:
                return True
            else:
                return False

        elif self.database == 'sqlserver':

            # bad!  There has to be an arcpy env for this
            # I cant find it, looked for a whole 15 minutes and everything 
            if self.sdeconn.lower().endswith('dbo.sde'):
                return True
            else:
                return False
    
    def isadministratoractive(self):
        
        try:
            sdereturn = cx_sde.selectavalue(self.sdeconn
                                           ,self.fetchsql('{0}'.format('isadministratoractive.sql')))
        except:
            return False

        if sdereturn == 1:
            return True
        else:
            return False

    def checkconnection(self):

        check = False

        try:
            sdereturn = cx_sde.selectavalue(self.sdeconn
                                           ,self.fetchsql('{0}'.format('dummysql.sql')))
            if len(sdereturn) == 1:
                check = True
        except:
            check = False

        return check

    def fetchsql(self
                ,whichsql):

        # fetch any sql from the library under the repo sql_<database> directory
        sqlfilepath = pathlib.Path(__file__).parent.parent \
                                            .joinpath('sql_{0}'.format(self.database)) \
                                            .joinpath(whichsql)
        
        with open(sqlfilepath, 'r') as sqlfile:
            sql = sqlfile.read() 

        return sql 

    def spoolsql(self
                ,startorstop='start'):

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             self.fetchsql('spool_sql_{0}.sql'.format(startorstop)))        

    def checkgdbadminprivs(self):

        #this one is a big old SQL that returns values

        logging.info('checking sde geodatabase admin privs using {0}'.format(self.sdeconn))

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                         self.fetchsql('privileges_gdb_admin.sql'))

        if len(sdereturn) > 0:
            for issue in sdereturn:
                print(issue)
            return False
        else:
            return True

    def checkmodules(self):

        logging.info('checking database modules required for an Enterprise Geodatabase')

        try:
            sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                                 self.fetchsql('gdb_requirements.sql'))
        except:
            logging.error('modules issues reported')
            #RAE from anonymous pl/sql block, probably a dumb pattern here
            #self.logger.error('sql returns: %s', sdereturn)
            return False

        return True        

    def checkgdbcreationprivs(self):

        # this one is a big old SQL that returns values

        logging.info('checking sde geodatabase privileges from {0}'.format(self.sdeconn))

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                         self.fetchsql('privileges_gdb_creation.sql'))

        if len(sdereturn) > 0:
            for issue in sdereturn:
                logging.error('{0}'.format(issue))
            return False
        else:
            return True   

    def exportconfig(self):

        # put keywords next to the .sde file
        # assumption is that .sde files are well organized with folders 
        # corresponding to databases and one "sde.sde" per folder with sidecar keywords
        keywordfile = pathlib.Path(self.sdeconn).parent.joinpath('keyword.txt')

        #keywordfile = "XX:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\keyword2.txt"


        arcpy.ExportGeodatabaseConfigurationKeywords_management('{0}'.format(self.sdeconn),
                                                                '{0}'.format(keywordfile))

    def config_gdb(self):

        # https://desktop.arcgis.com/en/arcmap/10.7/manage-data/gdbs-in-oracle/configuration-keywords.htm
        # just doing 1 val, risking it from sql
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             self.fetchsql('update_geometry_storage.sql'))

        # https://desktop.arcgis.com/en/arcmap/10.7/manage-data/gdbs-in-oracle/update-open-cursors.htm
        # similar going rogue
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             self.fetchsql('upsert_open_cursors.sql'))


    def enable(self,
               authfile):

        if  self.checkconnection() \
        and self.checkgdbadminprivs() \
        and self.checkmodules() \
        and self.checkgdbcreationprivs():

            py2enable = pathlib.Path(__file__).parent.parent \
                                              .joinpath('py27') \
                                              .joinpath('enable_gdb.py')
            
            callcmd =  f"{self.arcpy2path} {py2enable} " 

            try:
                
                self.logger.info('attempting to enable geodatabase from py27 using {0}'.format(callcmd))
                
                exit_code = call(callcmd)
                #exit_code = 0
                # looks like this
                #arcpy.EnableEnterpriseGeodatabase_management(self.sdeconn, 
                #                                             authfile)
                logging.info('exit code is {0}'.format(exit_code))
            except:
                logging.error('failure calling ArcGIS enable gdb with {0}'.format(callcmd))    
                raise ValueError(f"failure calling ArcGIS enable gdb with {callcmd}") 

        else:

            logging.error('missing requirements to enable a geodatabase from {0}'.format(self.sdeconn))             
            raise ValueError('missing requirements to enable a geodatabase from {0}'.format(self.sdeconn))
            
        try:
            
            logging.info('exporting keywords to a file next to {0}'.format(self.sdeconn))
            logging.info('update keywords then run arcpy.ImportGeodatabaseConfigurationKeywords_management')
            self.exportconfig()            

        except:
        
            print (arcpy.GetMessages())

        logging.info('updating geodatabase configuration')
        self.config_gdb()

    def compress(self):

        states_removed = 0

        if self.isadministrator():

            if self.interpret(arcpy.Compress_management(self.sdeconn)) == 0:

                states_removed = cx_sde.selectavalue(self.sdeconn
                                                    ,self.fetchsql('{0}'.format('get_compress_states.sql')))
        
        return states_removed

    def rebuildindexes(self):

        # https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-oracle/rebuild-system-table-indexes.htm

        output = 0

        if self.isadministrator():

            return self.interpret(arcpy.RebuildIndexes_management(self.sdeconn
                                                                 ,'SYSTEM'
                                                                 , ''
                                                                 ,'ALL'))

        return output

    def importfeatureclass(self
                          ,sourcefc
                          ,targetfcname):

        # print('fc2fc {0} {1} {2}'.format(sourcefc, self.sdeconn, targetfcname))

        # I like this formulation I am writing code for gdbs, and gdbs import fcs
        #    (avoid thinking of this as a "copy" or an ETL)
        # caller to manage locks, delete if exists, etc, via the fc class
        # sourcefc is the hard part, any ESRI-approved will work like
        # C:\matt_projects\database_utils\arcgisconnections\bldg@giscmnt.sde\BLDG.BUILDING
        arcpy.FeatureClassToFeatureClass_conversion(sourcefc
                                                   ,self.sdeconn
                                                   ,targetfcname)        

    def importtable(self
                   ,sourcetab
                   ,targettabname):

        arcpy.TableToTable_conversion(sourcetab
                                     ,self.sdeconn
                                     ,targettabname)   
   
                            
        
import arcpy
import os
import pathlib
import logging
import configparser
from subprocess import call

import cx_sde


class Gdb(object):

    def __init__(self
                ,arcpy2path=None
                ,database='oracle'):
            
        self.sdeconn = os.path.normpath(os.environ['SDEFILE'])
        
        if arcpy2path is None:
            self.arcpy2path = 'C:\Python27\ArcGIS10.6\python.exe'
        else:
            self.arcpy2path = arcpy2path

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # used only as fetch path to all SQLs we will execute
        # for now src\sql_<oracle>
        # life goals: src\sql_<postgres> switch and everything just works?
        self.database = database

        self.administrator =  self.isadministrator()

    def isadministrator(self):

        sdereturn = cx_sde.selectavalue(self.sdeconn
                                       ,self.fetchsql('{0}'.format('isadministrator.sql')))

        if sdereturn == 1:
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

        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,self.fetchsql('{0}'.format('dummysql.sql')))

        if len(sdereturn) == 1:
            return True
        else:
            return False

    def fetchsql(self
                ,whichsql):

        # fetch any sql from the library under the repo sql_oracle directory
        # highfalutin plans that some day we might have an sql_postgres directory
        # and simply instantiating a gdb instance with database type 'postgres'
        # switcheroos all sql here

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

        self.logger.info('checking sde geodatabase admin privs using {0}'.format(self.sdeconn))

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                         self.fetchsql('privileges_gdb_admin.sql'))

        if len(sdereturn) > 0:
            for issue in sdereturn:
                print(issue)
            return False
        else:
            return True

    def checkmodules(self):

        self.logger.info('checking database modules required for an Enterprise Geodatabase')

        try:
            sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                                 self.fetchsql('gdb_requirements.sql'))
        except:
            self.logger.error('modules issues reported')
            #RAE from anonymous pl/sql block, probably a dumb pattern here
            #self.logger.error('sql returns: %s', sdereturn)
            return False

        return True        

    def checkgdbcreationprivs(self):

        # this one is a big old SQL that returns values

        self.logger.info('checking sde geodatabase privileges from {0}'.format(self.sdeconn))

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                         self.fetchsql('privileges_gdb_upgrade.sql'))

        if len(sdereturn) > 0:
            for issue in sdereturn:
                self.logger.error('{0}'.format(issue))
            return False
        else:
            return True   

    def exportconfig(self):

        # put keywords next to the .sde file
        # assumption is that .sde files are well organized with folders 
        # corresponding to databases and one "sde.sde" per folder with sidecar keywords
        keywordfile = pathlib.Path(self.sdeconn).parent.joinpath('keyword.txt')


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
                # looks like this
                #arcpy.EnableEnterpriseGeodatabase_management(self.sdeconn, 
                #                                             authfile)
                self.logger.info('exit code is {0}'.format(exit_code))
            except:
                self.logger.error('failure calling ArcGIS enable gdb with {0}'.format(callcmd))    
                raise ValueError(f"failure calling ArcGIS enable gdb with {callcmd}") 

        else:

            self.logger.error('missing requirements to enable a geodatabase from {0}'.format(self.sdeconn))             

        self.logger.info('exporting geodatabase configuration keywords to {0}'.format(keywordfile))

        try:
            
            self.logger.info('exporting keywords to a file next to {0}'.format(self.sdeconn))
            self.logger.info('update keywords then run arcpy.ImportGeodatabaseConfigurationKeywords_management')
            self.exportconfig()            

        except:
        
            print (arcpy.GetMessages())

        self.logger.info('updating geodatabase configuration')
        self.config_gdb()

        

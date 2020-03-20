import arcpy
import os
import pathlib
from subprocess import call

import cx_sde


class Gdb(object):

    def __init__(self,
                 arcpy2path=None):

        self.sdeconn = os.environ['SDEFILE']
        
        if arcpy2path is None:
            self.arcpy2path = 'C:\Python27\ArcGIS10.6\python.exe'
        else:
            self.arcpy2path = arcpy2path

    def checkconnection(self):

        sql = 'SELECT dummy from dual'
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        if len(sdereturn) == 1:
            return True
        else:
            return False

    def fetchsql(self,
                 whichsql):

        # fetch any sql from the library under the repo sql directory
        sqlfilepath = pathlib.Path(__file__).parent.parent \
                                            .joinpath('sql') \
                                            .joinpath(whichsql)
        
        with open(sqlfilepath, 'r') as sqlfile:
            sql = sqlfile.read() 

        return sql 

    def checkgdbadminprivs(self):

        #this one is a big old SQL that returns values

        print(f"checking sde geodatabase admin privs using {self.sdeconn}")

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                         self.fetchsql('privileges_gdb_admin.sql'))

        if len(sdereturn) > 0:
            for issue in sdereturn:
                print(issue)
            return False
        else:
            return True

    def checkmodules(self):

        print("checking database modules required for an Enterprise Geodatabase")

        try:
            sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                                 self.fetchsql('gdb_requirements.sql'))
        except:
            print("see screen output for errors")
            return False

        return True        

    def checkgdbcreationprivs(self):

        # this one is a big old SQL that returns values

        print(f"checking sde geodatabase privileges from {self.sdeconn}")

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                         self.fetchsql('privileges_gdb_upgrade.sql'))

        if len(sdereturn) > 0:
            for issue in sdereturn:
                print(issue)
            return False
        else:
            return True   

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
                
                print(f"attempting to enable geodatabase from py27 using {callcmd}")
                
                exit_code = call(callcmd)
                # looks like this
                #arcpy.EnableEnterpriseGeodatabase_management(self.sdeconn, 
                #                                             authfile)
                print(f"exit code is {exit_code}")
            except:

                raise ValueError(f"failure calling ArcGIS enable gdb with {callcmd}") 

        else:

            raise ValueError(f"missing requirements to enable a geodatabase from {self.sdeconn}") 
            

        # put keywords next to the .sde file
        keywordfile = pathlib.Path(self.sdeconn).parent.joinpath('keyword.txt')

        print(f"exporting geodatabase configuration keywords to {keywordfile}")

        try:

            arcpy.ExportGeodatabaseConfigurationKeywords_management(self.sdeconn,
                                                                    keywordfile)

        except:
        
            print (arcpy.GetMessages())

        print (f"update {keywordfile} then run arcpy.ImportGeodatabaseConfigurationKeywords_management")

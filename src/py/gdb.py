import arcpy
import os
import pathlib

import cx_sde


class Gdb(object):

    def __init__(self):

        self.sdeconn = os.environ['SDEFILE']

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
        sqlfilepath = pathlib.Path(__file__).joinpath('sql').joinpath(whichsql)
        
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

        print(f"checking sde geodatabase enablement privileges from {self.sdeconn}")

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
            
            # untested

            try:
                arcpy.EnableEnterpriseGeodatabase_management(self.sdeconn, 
                                                             authfile)
            
            except:

                print (arcpy.GetMessages())

        # put keywords next to the .sde file
        keywordfile = pathlib.Path(self.sdeconn).parent.joinpath('keyword.txt')

        print(f"exporting geodatabase configuration keywords to {keywordfile}")

        try:

            arcpy.ExportGeodatabaseConfigurationKeywords_management(self.sdeconn,
                                                                    keywordfile)

        except:
        
            print (arcpy.GetMessages())

        print (f"update {keywordfile} then run arcpy.ImportGeodatabaseConfigurationKeywords_management")

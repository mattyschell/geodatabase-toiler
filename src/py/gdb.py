"""This is a check on known requirements for a geodatabase.  Reminder: 
don't think of this as tests, unit tests, etc.
"""
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

    def checkgdbadminprivs(self):

        #this one is a big old SQL that returns values

        print(f"checking sde geodatabase admin privs, ignore if {self.sdeconn} is not SDE")

        sqlfilepath = os.path.join(pathlib.Path(__file__).parent.parent,
                                   'sql',
                                   'helpers',
                                   'privileges_gdb_admin.sql')
        
        with open(sqlfilepath, 'r') as sqlfile:
            sql = sqlfile.read() 

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                            sql)

        if len(sdereturn) > 0:
            for issue in sdereturn:
                print(issue)
            return False
        else:
            print (".")
            return True


    def checkmodules(self):

        print("checking database modules required for an Enterprise Geodatabase")

        sqlfilepath = os.path.join(pathlib.Path(__file__).parent.parent,
                                   'sql',
                                   'gdb_requirements.sql')
        
        with open(sqlfilepath, 'r') as sqlfile:
            sql = sqlfile.read() 

        try:
            sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                                 sql)
        except:
            print("see screen output for errors")
            return False
            
        print (".")
        return True        


    def checkgdbcreationprivs(self):

        # this one is a big old SQL that returns values

        print(f"checking sde geodatabase enablement privileges from {self.sdeconn}")

        sqlfilepath = os.path.join(pathlib.Path(__file__).parent.parent,
                                   'sql',
                                   'helpers',
                                   'privileges_gdb_upgrade.sql')
        
        with open(sqlfilepath, 'r') as sqlfile:
            sql = sqlfile.read() 

        sdereturn = cx_sde.selectacolumn(self.sdeconn,
                                            sql)

        if len(sdereturn) > 0:
            for issue in sdereturn:
                print(issue)
            return False
        else:
            print (".")
            return True


        


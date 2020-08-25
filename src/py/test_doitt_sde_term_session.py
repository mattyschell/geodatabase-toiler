import unittest
import os
import time
from subprocess import Popen

import cx_sde
import test_doitt_sde_term_session_sleeper

# From Python 3 
# CALL C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_doitt_sde_term_session.py 
# success looks like
#   ----------------------------------------------------------------------
#   Ran 8 tests in <forever>

#   OK

# Tests
# A - Admin user schema can select from system table
# B - Admin user schema can insert/delete into/from system table
# C - Admin user schema can update system table
# D - Admin user schema cannot insert duplicate schema/os_user pair
# E - Non-admin schema cannot insert, update, delete from system table
# F - Admin user can terminate a session from self os_user connected from an application schema
# G - Admin user does not terminate a session from self os_user when specifying application schema and some other os_user  
# H - Admin user attempt to terminate own session and os_user does not succeed


class DoittSdeTermSessionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # will need to manually hack these or externalize, TBD
        self.adminschema = os.path.normpath("T:\GIS\Internal\Connections\oracle19c\dev\CSCL-ditCSdv1\mschell_private\mschell.sde")
        self.appschema = os.path.normpath("T:\GIS\Internal\Connections\oracle19c\dev\CSCL-ditCSdv1\mschell_private\cscl_pub.sde")

        # these should be fixed
        self.systemtable = 'SYSTEM.DOITT_SDE_TERM_SESSION'
        self.systemproceduresql = 'BEGIN SYSTEM.sp_doitt_term_sde_session(); END; '
        self.systemsessionview = 'SYSTEM.V_DOITT_USER_SES_STATUS'

        # when forking off to call a sleep timer in pl/sql
        # we will let the new thread have a few seconds to import all of its
        # bloated dependencies and for the system view to refresh
        # this is obviously a terrible anti-pattern and I will regret this decision
        # (sorry) 
        self.fudgetime = 5

        # tuck away schema names for later use
        sql = """select username from user_users"""
        self.adminschemaname = cx_sde.selectavalue(self.adminschema
                                                  ,sql)
        self.appschemaname = cx_sde.selectavalue(self.appschema
                                                ,sql)

        # me or my brother MR
        sql = """select UPPER(sys_context('USERENV','OS_USER')) from dual"""
        self.myosuser = cx_sde.selectavalue(self.adminschema
                                           ,sql)

    @classmethod
    def tearDownClass(self):

        pass

    def test_aselect_from_system_table(self):

        # A - Admin user schemas can select from system table

        sql = 'SELECT count(*) from {0}'.format(self.systemtable)

        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,sql)

        self.assertGreaterEqual(sdereturn
                               ,0
                               ,'Cant select from {0}'.format(self.systemtable)) 


    def test_binsert_into_system_table(self):

        # B - Admin user schema can insert into system table

        sql = """insert into {0} (username, osuser) """ \
              """select sys_context('USERENV','CURRENT_USER') """ \
              """      ,sys_context('USERENV','OS_USER') """ \
              """from dual """.format(self.systemtable)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

        testsql = """select count(*) from {0} """ \
                  """where """ \
                  """    UPPER(username) = UPPER(sys_context('USERENV','CURRENT_USER')) """ \
                  """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) """.format(self.systemtable)

        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,testsql)

        self.assertEqual(sdereturn
                        ,1
                        ,'Cant insert into {0}'.format(self.systemtable)) 

        # B - Admin user schema can delete from system table

        sql = """delete from {0} """ \
              """where """ \
              """    UPPER(username) = UPPER(sys_context('USERENV','CURRENT_USER')) """ \
              """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) """.format(self.systemtable)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,testsql)

        self.assertEqual(sdereturn
                         ,0
                         ,'Cant delete from {0}'.format(self.systemtable))

    def test_cupdate_system_table(self):
        
        # C - Admin user schema can update system table
        sql = """insert into {0} (username, osuser) """ \
              """select sys_context('USERENV','CURRENT_USER') """ \
              """      ,sys_context('USERENV','OS_USER') """ \
              """from dual """.format(self.systemtable)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

        sql = """update {0} """ \
              """set username = username || 'XX' """ \
              """   ,osuser = osuser || 'XX' """ \
              """where """ \
              """     UPPER(username) = UPPER(sys_context('USERENV','CURRENT_USER')) """ \
              """and  UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) """.format(self.systemtable)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

        testsql = """select count(*) from {0} """ \
                  """where """ \
                  """    UPPER(username) = UPPER(sys_context('USERENV','CURRENT_USER')) || 'XX' """ \
                  """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) || 'XX' """.format(self.systemtable)

        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,testsql)

        self.assertEqual(sdereturn
                        ,1
                        ,'Cant update {0}'.format(self.systemtable))

        sql = """delete from {0} """ \
              """where """ \
              """    UPPER(username) = UPPER(sys_context('USERENV','CURRENT_USER')) || 'XX' """ \
              """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) || 'XX' """.format(self.systemtable)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

    def test_dinsert_duplicates(self):
        
        # D - Admin user schema cannot insert duplicate schema/os_user pair
        sql = """insert into {0} (username, osuser) """ \
              """select sys_context('USERENV','CURRENT_USER') """ \
              """      ,sys_context('USERENV','OS_USER') """ \
              """from dual """ \
              """union all """ \
              """select sys_context('USERENV','CURRENT_USER') """ \
              """      ,sys_context('USERENV','OS_USER') """ \
              """from dual """.format(self.systemtable)



        # TODO: get this right some day
        #self.assertRaises(ValueError,cx_sde.execute_immediate(self.adminschema
        #                                                     ,sql))

        sqlstatus = True
        try:
            sdereturn = cx_sde.execute_immediate(self.adminschema
                                                ,sql)
        except:
            sqlstatus = False

        self.assertFalse(sqlstatus,'Inserted duplicates into {0}'.format(self.systemtable))
            

    def test_ecantinsert_into_system_table(self):

        # E - Non-admin schema cannot insert, update, delete from system table

        sql = """insert into {0} (username, osuser) """ \
              """select sys_context('USERENV','CURRENT_USER') """ \
              """      ,sys_context('USERENV','OS_USER') """ \
              """from dual """.format(self.systemtable)

        sqlstatus = True
        try:
            sdereturn = cx_sde.execute_immediate(self.appschema
                                                ,sql)
        except:
            sqlstatus = False

        self.assertFalse(sqlstatus,'Non admin schema wrote to {0}'.format(self.systemtable))

    def test_fterminate_appschema(self):

        # F - Admin user can terminate a session from self os_user connected from an application schema

        sql = """insert into {0} (username, osuser) """ \
              """select '{1}' """ \
              """      ,UPPER(sys_context('USERENV','OS_USER')) """ \
              """from dual """.format(self.systemtable
                                     ,self.appschemaname)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)
        
        # thats admin schema at the end -->
        Popen(["C:/Progra~1/ArcGIS/Pro/bin/Python/scripts/propy.bat", "./src/py/test_doitt_sde_term_session_sleeper.py", self.appschema])

        time.sleep(self.fudgetime)

        # get count from doitt dba session view
        sql = """select count(*) """ \
              """from {0} """ \
              """where """ \
              """    UPPER(client_user) = UPPER(sys_context('USERENV','OS_USER')) """ \
              """and UPPER(db_user) = '{1}' """.format(self.systemsessionview
                                                ,self.appschemaname)
        
        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,sql)

        #print('got {0} sessions before'.format(sdereturn))
        self.assertGreaterEqual(sdereturn
                               ,1
                               ,'Didnt get a session going from {0}'.format(self.appschemaname)) 

        # call systemproceduresql
        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,self.systemproceduresql)


        # get count again, assert equal to 0
        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,sql)
        #print('got {0} sessions after'.format(sdereturn))
        
        self.assertEqual(sdereturn
                        ,0
                        ,'Didnt kill sessions from {0}'.format(self.appschemaname)) 

        sql = """delete from {0} """ \
              """where """ \
              """    UPPER(username) = '{1}' """ \
              """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) """.format(self.systemtable
                                                                                       ,self.appschemaname)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)
        
    def test_gnoterminate_appschema(self):
    
        # G - Admin user does not terminate a session from self os_user when specifying application schema and some other os_user

        sql = """insert into {0} (username, osuser) """ \
              """select '{1}' """ \
              """      ,UPPER(sys_context('USERENV','OS_USER')) || 'XX' """ \
              """from dual """.format(self.systemtable
                                     ,self.appschemaname)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

        Popen(["C:/Progra~1/ArcGIS/Pro/bin/Python/scripts/propy.bat", "./src/py/test_doitt_sde_term_session_sleeper.py", self.appschema])

        time.sleep(self.fudgetime)

        # get count from doitt dba session view
        sql = """select count(*) """ \
              """from {0} """ \
              """where """ \
              """    UPPER(client_user) = UPPER(sys_context('USERENV','OS_USER')) """ \
              """and UPPER(db_user) = '{1}' """.format(self.systemsessionview
                                                      ,self.appschemaname)
        
        sdereturnb4 = cx_sde.selectavalue(self.adminschema
                                         ,sql)

        print('got {0} sessions before'.format(sdereturn))
        self.assertGreaterEqual(sdereturnb4
                               ,1
                               ,'Didnt get a session going from {0}'.format(self.appschemaname)) 

        # call systemproceduresql, should not kill appschema/osuser
        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,self.systemproceduresql)


        # get count again, assert equal to b4
        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,sql)
        
        self.assertEqual(sdereturn
                        ,sdereturnb4
                        ,'Should not have killed sessions from phony osuserXX and {0}'.format(self.adminschema)) 

        sql = """delete from {0} """ \
              """where """ \
              """    UPPER(username) = '{1}' """ \
              """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) || 'XX' """.format(self.systemtable
                                                                                               ,self.appschemaname)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

    def test_gnoterminate_own(self):
    
        # H - Admin user attempt to terminate own session and os_user does not succeed

        sql = """insert into {0} (username, osuser) """ \
              """select '{1}' """ \
              """      ,UPPER(sys_context('USERENV','OS_USER')) """ \
              """from dual """.format(self.systemtable
                                     ,self.adminschemaname)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)

        Popen(["C:/Progra~1/ArcGIS/Pro/bin/Python/scripts/propy.bat", "./src/py/test_doitt_sde_term_session_sleeper.py", self.adminschema])

        time.sleep(self.fudgetime)

        # get count from doitt dba session view
        sql = """select count(*) """ \
              """from {0} """ \
              """where """ \
              """    UPPER(client_user) = UPPER(sys_context('USERENV','OS_USER')) """ \
              """and UPPER(db_user) = '{1}' """.format(self.systemsessionview
                                                      ,self.adminschemaname)
        
        sdereturnb4 = cx_sde.selectavalue(self.adminschema
                                         ,sql)

        print('got {0} sessions before'.format(sdereturn))
        self.assertGreaterEqual(sdereturnb4
                               ,1
                               ,'Didnt get a session going from {0}'.format(self.adminschemaname)) 

        # call systemproceduresql, should not kill adminschema/osuser
        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,self.systemproceduresql)


        # get count again, assert equal to b4
        sdereturn = cx_sde.selectavalue(self.adminschema
                                       ,sql)
        print('got {0} sessions after'.format(sdereturn))
        
        self.assertEqual(sdereturn
                        ,sdereturnb4
                        ,'Should not have killed sessions from osuser and {0}'.format(self.adminschema)) 

        sql = """delete from {0} """ \
              """where """ \
              """    UPPER(username) = '{1}' """ \
              """and UPPER(osuser) = UPPER(sys_context('USERENV','OS_USER')) """.format(self.systemtable
                                                                                       ,self.adminschemaname)

        sdereturn = cx_sde.execute_immediate(self.adminschema
                                            ,sql)



if __name__ == '__main__':
    unittest.main()

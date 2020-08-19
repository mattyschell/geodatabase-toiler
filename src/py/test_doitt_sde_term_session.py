import unittest
import os

import cx_sde

# From Python 3 
# CALL C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_doitt_sde_term_session.py 

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

        self.adminschema = os.path.normpath("T:\GIS\Internal\Connections\oracle19c\dev\CSCL-ditCSdv1\mschell_private\mschell.sde")
        self.appschema = os.path.normpath("T:\GIS\Internal\Connections\oracle19c\dev\CSCL-ditCSdv1\mschell_private\cscl_pub.sde")

        self.systemtable = 'SYSTEM.DOITT_SDE_TERM_SESSION'
        self.systemprocedure = 'SYSTEM.SP_DOITT_TERM_SDE_SESSION'

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


if __name__ == '__main__':
    unittest.main()

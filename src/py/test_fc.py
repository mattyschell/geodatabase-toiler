import os
import pathlib
import unittest

import cx_sde
import gdb
import fc


class FcTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        self.testgdb = gdb.Gdb()
        # c:\matt_projects\geodatabase-toiler\src\py\testdata\testdata.gpkg\main.BUILDING
        self.srctestfc = os.getcwd() + r'\src\py\testdata\testdata.gpkg\main.BUILDING'

        self.testgdb.importfeatureclass(self.srctestfc
                                       ,'TOILERTESTFC')

        self.testfc = fc.Fc(self.testgdb
                           ,'TOILERTESTFC')     

        #get some non-oracle managed user on the DB to work with
        self.dummyuser = cx_sde.selectavalue(self.testgdb.sdeconn
                                            ,self.testgdb.fetchsql('dummyuser.sql'))

    @classmethod
    def tearDownClass(self):

        #pass
        self.testfc.delete()

    def test_aexists(self):

        self.assertTrue(self.testfc.exists())

    def test_blocksexist(self):

        self.assertFalse(self.testfc.locksexist())

    def test_cversion(self):

        #TODO get versioning with bug workaround to work with the test here

        self.testfc.version()
        pass

        # careful, just for testing
        #self.testfc_evw = fc.Fc(self.testgdb
        #                       ,'TOILERTESTFC_EVW')
    
        #self.assertTrue(self.testfc_evw.exists())    

    def test_dtrackedits(self):

        self.testfc.trackedits()

        self.assertTrue('CREATED_DATE' in self.testfc.getfields() and \
                        'CREATED_USER' in self.testfc.getfields() and \
                        'LAST_EDITED_USER' in self.testfc.getfields() and \
                        'LAST_EDITED_DATE' in self.testfc.getfields() )     

    def test_egrantprivileges(self):       

        self.testfc.grantprivileges(self.dummyuser
                                   ,'GRANT')

        privskount = cx_sde.selectavalue(self.testgdb.sdeconn
                                        ,self.testgdb.fetchsql('dummyuserprivcount.sql'))

        self.assertEqual(privskount, 4)


if __name__ == '__main__':
    unittest.main()

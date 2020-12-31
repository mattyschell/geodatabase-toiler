import os
import pathlib
import unittest

import cx_sde
import gdb


class GdbTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        self.geodatabase = gdb.Gdb()
        

    @classmethod
    def tearDownClass(self):

        pass

    def test_acheckconnection(self):

        #sql returns a single X

        self.assertTrue(self.geodatabase.checkconnection)
    
    
    def test_bcheckmodules(self):

        # this should pass for any valid user connected to an Enterprise GDB

        self.assertTrue(self.geodatabase.checkmodules)

    def test_cisadministrator(self):

        self.assertIsInstance(self.geodatabase.administrator
                             ,bool)

    def test_disadministratoractive(self):

        self.assertIsInstance(self.geodatabase.isadministratoractive()
                             ,bool)

    def test_eexportconfig(self):

        if  self.geodatabase.administrator \
        and self.geodatabase.isadministratoractive():

            self.geodatabase.exportconfig()

            self.assertTrue(os.path.isfile(os.path.join('{0}'.format(self.sdeconn,'keyword.txt')))) 

        else:

            # winning
            self.assertTrue(True)

    def test_fspoolsql(self):

        if self.geodatabase.administrator:

            # only admin user is gonna have privileges to select dictionary views
            # in any expected future

            self.geodatabase.spoolsql('start')

            self.geodatabase.spoolsql('stop')

            sdereturn = cx_sde.selectavalue(self.sdeconn
                                           ,'select count(*) from spoolsdesql')

            self.assertGreaterEqual(sdereturn
                                   ,0)

            sdereturn = cx_sde.execute_immediate(self.sdeconn
                                                ,'drop table spoolsdesql')

        else:

            # winning
            self.assertTrue(True)
    
    def test_gcompress(self):

        states_removed = self.geodatabase.compress()

        self.assertGreaterEqual(states_removed, 0)

    def test_hrebuildindexes(self):

        self.assertEqual(self.geodatabase.rebuildindexes(), 0)


if __name__ == '__main__':
    unittest.main()

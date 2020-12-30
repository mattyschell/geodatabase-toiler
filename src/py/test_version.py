import os
import unittest

import cx_sde
import gdb
import version


class VersionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        self.geodatabase = gdb.Gdb()
        self.version = version.Version(self.geodatabase
                                      ,'TEST_VERSION')
        
        self.version.delete()

    @classmethod
    def tearDownClass(self):

        #delete tester version if it survives
        self.version.delete()

    def test_aexists(self):

        self.assertFalse(self.version.exists())

    def test_bdeletenonexistent(self):

        self.version.delete()

        self.assertFalse(self.version.exists())

    def test_ccreatedelete(self):

        self.version.create()

        self.assertTrue(self.version.exists())

        self.version.delete()

        self.assertFalse(self.version.exists())

    def test_drecnpost(self):

        self.version.create()

        # not much of a test bub
        recnpostoutput = self.version.reconcileandpost()

        self.assertIn('Succeeded'
                     ,recnpostoutput) 

        self.assertIn('Finished reconcile'
                     ,recnpostoutput)

        self.version.delete()


if __name__ == '__main__':
    unittest.main()
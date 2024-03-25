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
        
        self.childversion = version.Version(self.geodatabase
                                           ,'TEST_CHILDVERSION'
                                           ,'TEST_VERSION')
        
        self.childversion.delete()
        self.version.delete()

    @classmethod
    def tearDownClass(self):

        #delete tester version if it survives
        self.childversion.delete()
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
        # go down another level
        # default is usually protected
        self.childversion.create()

        # not much of a test 
        recnpostoutput = self.childversion.reconcileandpost()

        self.assertIn('Succeeded'
                     ,recnpostoutput) 

        self.assertIn('Finished reconcile'
                     ,recnpostoutput)

        self.childversion.delete()
        self.version.delete()

    def test_eeditability(self):

        self.version.create()

        self.assertTrue(self.version.iseditable())

    def test_fprotect(self):

        self.version.create()

        self.version.protect()

        self.assertFalse(self.version.iseditable())

    def test_gprotect(self):

        self.version.create()

        self.version.protect()

        self.version.unprotect()

        self.assertTrue(self.version.iseditable())


if __name__ == '__main__':
    unittest.main()
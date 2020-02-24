
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


    def test_acheckmodules(self):

        #sql returns a single X

        self.assertTrue(self.geodatabase.checkconnection)
    
    
    def test_bcheckmodules(self):

        # this should pass for any valid user connected to an Enterprise GDB

        self.assertTrue(self.geodatabase.checkmodules)

    

if __name__ == '__main__':
    unittest.main()

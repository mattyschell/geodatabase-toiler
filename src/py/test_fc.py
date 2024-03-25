import os
import pathlib
import unittest
import glob

import cx_sde
import gdb
import fc
import arcpy


class FcTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']

        self.testgdb = gdb.Gdb()

        # c:\matt_projects\geodatabase-toiler\src\py\testdata\testdata.gpkg\main.BUILDING
        self.srctestfcdir = os.getcwd() + r'\\src\\py\\testdata\\'
        
        # test geopackage not working (easily) any longer
        # date fields are importing as timestamp
        # self.srctestfc = self.srctestfcdir + r'testdata.gpkg\main.BUILDING'
        self.srctestfilegdb = os.path.join(os.path.dirname(os.path.realpath(__file__))
                                          ,'testdata'
                                          ,'nyc.gdb')
        
        self.srctestfc = os.path.join(self.srctestfilegdb
                                      ,'borough')

        self.testgdb.importfeatureclass(self.srctestfc
                                       ,'TOILERTESTFC')

        self.testfc = fc.Fc(self.testgdb
                           ,'TOILERTESTFC')     

        #get some non-oracle managed user on the DB to work with
        self.dummyuser = cx_sde.selectavalue(self.testgdb.sdeconn
                                            ,self.testgdb.fetchsql('dummyuser.sql'))

    @classmethod
    def tearDownClass(self):

        self.testfc.delete()

        dummyfiles = glob.glob(os.path.join(self.srctestfcdir
                                           ,'dummy.*'))

        for dummyfile in dummyfiles:
             os.remove(dummyfile)

    def test_aexists(self):

        self.assertTrue(self.testfc.exists())

    def test_blocksexist(self):

        self.assertFalse(self.testfc.locksexist())

    def test_cversion(self):

        #TODO get versioning with bug workaround to work with the test here

        self.assertEqual(self.testfc.version(),0)

        #self.testfc_evw = fc.Fc(self.testgdb
        #                       ,'TOILERTESTFC_EVW')
    
        #self.assertTrue(self.testfc_evw.exists())    

    def test_dtrackedits(self):

        self.assertEqual(self.testfc.trackedits('ADD_FIELDS'), 0)

        self.assertTrue('CREATED_DATE' in self.testfc.getfields() and \
                        'CREATED_USER' in self.testfc.getfields() and \
                        'LAST_EDITED_USER' in self.testfc.getfields() and \
                        'LAST_EDITED_DATE' in self.testfc.getfields() )     

    def test_egrantprivileges(self):       

        self.assertEqual(self.testfc.grantprivileges(self.dummyuser
                                                    ,'GRANT')
                        ,0)

        self.assertEqual(cx_sde.selectavalue(self.testgdb.sdeconn
                                            ,self.testgdb.fetchsql('dummyuserprivcount.sql'))
                        ,4)

    def test_findex(self):

        self.assertEqual(self.testfc.index('BOROCODE')
                        ,0)

        # expect the index name to be truncated
        self.assertEqual(cx_sde.selectavalue(self.testgdb.sdeconn
                                            ,self.testgdb.fetchsql('dummyindexcount.sql'))
                        ,1)

    def test_gexporttoshp(self):

        self.testfc.exporttoshp(self.srctestfcdir
                               ,'dummy.shp')

        self.assertTrue(os.path.exists(os.path.join(self.srctestfcdir
                                                   ,'dummy.shp')))

        self.assertTrue(os.path.exists(os.path.join(self.srctestfcdir
                                                   ,'dummy.dbf')))

        self.assertTrue(os.path.exists(os.path.join(self.srctestfcdir
                                                   ,'dummy.prj')))
        
        self.assertTrue(os.path.exists(os.path.join(self.srctestfcdir
                                                   ,'dummy.shx')))

        self.assertTrue(os.path.exists(os.path.join(self.srctestfcdir
                                                   ,'dummy.cpg')))

    def test_hrebuildindexes(self):

        self.testfc.version()

        self.assertEqual(self.testfc.rebuildindexes(), 0)

    def test_ianalyze(self):

        self.assertEqual(self.testfc.analyze(), 0)
     

if __name__ == '__main__':
    unittest.main()

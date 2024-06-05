import os
import unittest

import arcpy
import cx_sde
import gdb


class GdbTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        self.geodatabase = gdb.Gdb() 
        self.testfilegdb = os.path.join(os.path.dirname(os.path.realpath(__file__))
                                       ,'testdata'
                                       ,'nyc.gdb')
        self.testborough = os.path.join(self.testfilegdb
                                       ,'borough')
        
        # this is hard coded and bad
        # but on the other hand if it moves that is also bad
        self.hostedborough = "https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/Borough_view/FeatureServer/0"
        # from the arcgis online "living atlas"
        self.hostedtable   = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services/LPA_DEC_2022_UK_NC/FeatureServer/0"

    @classmethod
    def tearDownClass(self):

        pass

    def test_aainit(self):

        initsucceeded = True

        try:
            os.environ['SDEFILE'] = 'C:/Temp/badsde.sde'
            self.badgeodatabase = gdb.Gdb()
            initsucceeded = True
        except:
            initsucceeded = False
        finally:
            os.environ['SDEFILE'] = self.sdeconn

        self.assertFalse(initsucceeded)

    def test_acheckconnection(self):

        # sql returns a single X

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

    def test_iregisterfeatureclass(self):

        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,'create table foo as select 1 as notobjectid from dual')

        # esri creates objectid in int format or whatever 
        try:
            self.assertEqual(self.geodatabase.registerfeatureclass('foo'), 0)
        finally:
            # consider moving delete to gdb class
            arcpy.Delete_management(os.path.join(self.sdeconn,'foo'))
                                                                               
    def test_jimportfeatureclass(self):       

        self.geodatabase.importfeatureclass(self.testborough
                                           ,'TESTBOROUGH')   
        
        # these are available in the fc class so dont try this at home
        self.assertTrue(arcpy.Exists(self.sdeconn + "/" + 'TESTBOROUGH'))

        arcpy.Delete_management(self.sdeconn + "/" + 'TESTBOROUGH')

    def test_kimporthostedfeatureclass(self):

        try:
            self.geodatabase.importfeatureclass(self.hostedborough
                                               ,'HOSTEDBOROUGH')   
        
            # these are available in the fc class, dont follow this pattern
            self.assertTrue(arcpy.Exists(self.sdeconn + "/" + 'HOSTEDBOROUGH'))
        finally:
            arcpy.Delete_management(self.sdeconn + "/" + 'HOSTEDBOROUGH')

    def test_limporthostedtable(self):

        try:
            self.geodatabase.importtable(self.hostedtable
                                        ,'HOSTEDTABLE')   
        
            # these are available in the fc class, dont follow this pattern
            self.assertTrue(arcpy.Exists(self.sdeconn + "/" + 'HOSTEDTABLE'))
        finally:
            arcpy.Delete_management(self.sdeconn + "/" + 'HOSTEDTABLE')

    def test_mimportprojectedfeatureclass(self):

        # self.hostedborough is 3857 web mercator
        testsrid = 2263
        testfc   = 'HOSTEDBOROUGH'

        try:
            self.geodatabase.importfeatureclass(self.hostedborough
                                               ,testfc
                                               ,testsrid)   
            
            self.assertTrue(arcpy.Exists(self.sdeconn + "/" + testfc))
            
            sdereturn = cx_sde.selectavalue(self.sdeconn
                                           ,'select a.shape.sdo_srid from {0} a where rownum = 1'.format(testfc))
            self.assertEqual(sdereturn
                            ,testsrid)       
                   
        finally:
            arcpy.Delete_management(self.sdeconn + "/" + 'HOSTEDBOROUGH')

if __name__ == '__main__':
    unittest.main()

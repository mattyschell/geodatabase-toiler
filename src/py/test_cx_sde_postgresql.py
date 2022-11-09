import os
import unittest

import cx_sde


class UtilsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        

    @classmethod
    def tearDownClass(self):

        pass

    def test_aexecute_immediate(self):

        #sql returns a single X
        #ValueError: ArcSDESQLExecute: StreamBindOutputColumn 
        #ArcSDE Error -65 Invalid pointer argument to function
        #sql = """ select 'X' """

        # no list here
        # returns 1
        sql = """select 1 """
        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,sql)

        self.assertEqual(sdereturn
                        ,1)

    def test_azexecute_immediate(self):

        # leave this here to clue us in if anything changes        
        klugeyassertraises = False

        sql = """ select 'X' """
        print(f"Expected confusing sql fail from ESRI executing {sql}")
        
        try:
            
            sdereturn= cx_sde.selectavalue(self.sdeconn
                                          ,sql)
        except:
            
            klugeyassertraises = True

        self.assertTrue(klugeyassertraises)            

    def test_bexecute_immediate(self):

        #sql returns a list with 2 Xs

        sql = 'select 1 union all select 1'
        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,sql)

        #print(sdereturn)
        # [[1], [1]]
        self.assertIsInstance(sdereturn
                             ,list)

        self.assertEqual(len(sdereturn)
                        ,2)

        self.assertEqual(len(sdereturn[0])
                        ,1)

        self.assertEqual(sdereturn[0][0]
                        ,1)

    def test_cselectavalue(self):

        sql = """select schemaname from pg_stat_all_tables """ \
            + """where schemaname = 'sde' limit 1"""

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)

        self.assertEqual(sdereturn, 'sde')

    
    def test_dselectnull(self):

        # should error.  Its select a value, not select the void
        sql = 'select null'

        print(f"Expected sql fail on next line from {sql}")

        try:
            sdereturn = cx_sde.selectavalue(self.sdeconn,
                                            sql)
        except:
            pass
        else:
            self.assertFalse(sdereturn)

    def test_eselectacolumn(self):

        sql = """select schemaname from pg_stat_all_tables """ \
            + """where schemaname = 'sde'"""

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertGreater(len(output), 1)
        self.assertEqual(output[0],'sde')

    def test_fselectabadcolumn(self):

        sql = """select bad from pg_stat_all_tables """ 

        print(f"Expected sql fail on next line from {sql}")

        try:
            output = cx_sde.selectacolumn(self.sdeconn,
                                          sql)
        except:
            pass
        else:
            raise ValueError('Shoulda failed')



if __name__ == '__main__':
    unittest.main()

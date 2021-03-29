import os
import unittest
import pathlib

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

        sql = 'SELECT dummy from dual'
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        self.assertEqual(len(sdereturn), 1)

        self.assertEqual(sdereturn[0], 'X')


    def test_bexecute_immediate(self):

        #sql returns a list with 2 Xs

        sql = 'SELECT dummy from dual UNION ALL select dummy from dual'
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        self.assertIsInstance(sdereturn, list)

        self.assertEqual(len(sdereturn), 2)


    def test_cselectavalue(self):

        sql = 'SELECT dummy FROM dual'

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)

        self.assertEqual(sdereturn, 'X')


    def test_dselectnull(self):

        # should error.  Its select a value, not select the void
        sql = 'SELECT NULL FROM dual'

        try:
            sdereturn = cx_sde.selectavalue(self.sdeconn,
                                            sql)
        except:
            pass
        else:
            self.assertFalse(sdereturn)


    def test_eselectacolumn(self):

        sql = 'SELECT dummy FROM dual'

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], 'X')

        sql = 'select dummy from dual union all select dummy from dual'

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], 'X')
        self.assertEqual(output[1], 'X')

    def test_fselectabadcolumn(self):

        sql = 'SELECT boo FROM dual'

        print(f"Expected sql fail on next line from {sql}")

        try:
            output = cx_sde.selectacolumn(self.sdeconn,
                                          sql)
        except:
            pass
        else:
            raise ValueError('Shoulda failed')


    def test_gselectanumbercolumn(self):

            sql = 'SELECT 1 FROM dual'

            output = cx_sde.selectacolumn(self.sdeconn,
                                          sql)

            self.assertIsInstance(output, list)
            self.assertEqual(len(output), 1)
            self.assertEqual(output[0], 1)

            sql = 'select 1 from dual union all select 1 from dual'

            output = cx_sde.selectacolumn(self.sdeconn,
                                            sql)

            self.assertIsInstance(output, list)
            self.assertEqual(len(output), 2)
            self.assertEqual(output[0], 1)
            self.assertEqual(output[1], 1)

    
    def test_hselectanullcolumn(self):

        sql = 'SELECT 1 FROM dual UNION ALL SELECT NULL FROM dual'

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], 1)
        self.assertIsNone(output[1])

        sql = 'SELECT NULL FROM dual'

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)
        self.assertIsNone(output[0])

    def test_ianonymousblock(self):

        #refer to /src/sql/dummy.sql for anonymous pl/sql block style
        dummyfile = os.path.join(pathlib.Path(__file__).parent.parent,
                                 'sql_oracle',
                                 'dummy.sql')

        # avoid stripping new lines and other formatting here, allow comments     
        with open(dummyfile, 'r') as sqlfile:
            sql = sqlfile.read() 

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

    def test_jdmlcommit(self): 

        sql = 'create table test_cx_sde_foo as select * from dual'

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                            sql)

        sql = """update test_cx_sde_foo a set a.dummy = 'Z'"""

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                            sql)

        sql = """select count(*) from test_cx_sde_foo a where a.dummy = 'Z'"""

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)
    
        self.assertEqual(sdereturn, 1)

        sql = 'drop table test_cx_sde_foo'
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                            sql)

    def test_kexecutestatements(self): 

        sql = 'create table test_cx_sde_foo2 as select * from dual'

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)
        sqls = []
        sqls.append("""insert into test_cx_sde_foo2 values('A') """)
        sqls.append("""insert into test_cx_sde_foo2 values('B') """)
        sqls.append("""insert into test_cx_sde_foo2 values('C') """)
        
        sdereturn = cx_sde.execute_statements(self.sdeconn,
                                              sqls)

        sql = """select count(*) from test_cx_sde_foo2 """

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)
    
        self.assertEqual(sdereturn, 4)

        sql = 'drop table test_cx_sde_foo2 '
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)


if __name__ == '__main__':
    unittest.main()

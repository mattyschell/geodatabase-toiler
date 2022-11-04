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
        #ValueError: ArcSDESQLExecute: StreamBindOutputColumn 
        #ArcSDE Error -65 Invalid pointer argument to function
        #sql = """ select 'X' """

        # no list here
        # returns 1
        sql = """select 1 """
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        self.assertEqual(sdereturn, 1)

    def test_bexecute_immediate(self):

        #sql returns a list with 2 Xs

        sql = 'select 1 union all select 1'
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        #print(sdereturn)
        # [[1], [1]]
        self.assertIsInstance(sdereturn, list)

        self.assertEqual(len(sdereturn), 2)

        self.assertEqual(len(sdereturn[0]),1)

        self.assertEqual(sdereturn[0][0], 1)


if __name__ == '__main__':
    unittest.main()

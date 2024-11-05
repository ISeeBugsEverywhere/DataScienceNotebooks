import unittest
from funkcijos import *
import sqlite3
import pandas as pd
import os
# print(os.getcwd())
class Test_funkcijos(unittest.TestCase):
    def setUp(self):
        self.A = 4
        self.B = 5
        
        self.SDB = sqlite3.connect('Auto.db')
        self.C = self.SDB.cursor()
        self.sql="""select Marke, count(*) as k from Autopliuslt
                    group by Marke
                    order by k DESC
                    limit 5;"""
        self.C.execute(self.sql)
        self.ans = self.C.fetchall()
        self.markes, self.kiekiai = list(map(list, zip(*self.ans)))

        self.sql2="""select * from Autopliuslt;"""
        self.df_with_dubs = pd.read_sql_query(self.sql2, con=self.SDB)
        self.df = self.df_with_dubs.drop_duplicates()
        
     
    def test_get_markes_sql(self):
        self.assertEqual(get_markes_sql(), self.markes)


    def test_get_markes_df(self):
        self.assertEqual(get_markes_df(), ['BMW', 'Volkswagen', 'Audi', 'Toyota', 'Mercedes-Benz'])


    def test_get_vid_kaina_top5(self):
        self.assertEqual(get_vid_kaina_top5(), [20971.0, 15244.0, 19219.0, 17269.0, 21967.0])

        
    def  test_add(self):
        self.assertEqual(add(self.A, self.B),9, msg='A nelygus B')
        self.assertEqual(add(-1, 1),0)
        self.assertNotEqual(add(-1, -1),0)
        
    def test_divide(self):
        self.assertEqual(divide(5,5), 1)
        self.assertRaises(ZeroDivisionError, divide, 1, 0)
        
        
    def test_multiply(self):
        self.assertEqual(multiply(2,4),8)
        self.assertNotEqual(multiply(3,1),1)
        
    def test_minus(self):
        self.assertEqual(minus(self.A, self.B), -1)
        self.assertEqual(minus(-1, -1), 0)
        
    def test_saknis(self):
        self.assertEqual(saknis(9),3)
        self.assertEqual(saknis(4),2)
        
        
    def test_unikalus(self):
        self.assertEqual(unikalus([1,1,2,3,3]), [1,2,3])
        self.assertEqual(unikalus(['l', 'a', 'a', 'z']), ['a', 'l', 'z'])
        self.assertNotEqual(unikalus(['l', 'a', 'a', 'z']), ['l', 'a', 'z'])
        
    
    def test_be_neigiamu(self):
        self.assertEqual(be_neigiamu([1, -1, 2, -3, 5]), [1,2,5])
        self.assertNotEqual(be_neigiamu([1, -1, 2, -3, 5]), [-1, -3])
        self.assertEqual(be_neigiamu([]), [])
        
        
    def test_kiek_kartu(self):
        self.assertEqual(kiek_kartu(['l', 'a', 'a', 'z']), {'a': 2, 'l': 1, 'z': 1})
        self.assertEqual(kiek_kartu(['labai Šaltas Vakaras']), {'labai Šaltas Vakaras': 1})
        self.assertNotEqual(kiek_kartu([]), None, msg='Pateiktas sąrašas tuščias')
        
        
    def test_sum_lst(self):
        self.assertEqual(sum_lst([1, 5, 0, 7], [1, 4, 0 ,7 ,6]), [1, 5, 0, 7, 4, 6])
        self.assertNotEqual(sum_lst([1, 5, 0, 7], [1, 5, 0, 7]), [1, 5, 0, 7, 1, 5, 0, 7])
        self.assertEqual(sum_lst(['labas', 'vakaras'], ['rytas', 'labas']), ['labas', 'vakaras', 'rytas'])
        
        
    def test_not_unique_lst(self):
        self.assertEqual(not_unique_lst(['l', 'a', 'a', 'z']), ['a'])
        self.assertEqual(not_unique_lst([1,1,2,3,4,5,5,7,6,6,8,8,9]), [1, 5, 6, 8])
        self.assertNotEqual(not_unique_lst([]), None)
        
    def test_apskr_S(self):
        self.assertRaises(ValueError, apskr_S, '1')
        self.assertRaises(ValueError, apskr_S, -1)
        self.assertEqual(apskr_S(1), 3.14)
        
        
    def test_rut_V(self):
        self.assertRaises(ValueError, rut_V, '1')
        self.assertRaises(ValueError, rut_V, -1)
        self.assertEqual(rut_V(1), 4.187)
        
        
    def test_rut_S(self):
        self.assertRaises(ValueError, rut_S, '1')
        self.assertRaises(ValueError, rut_S, -1)
        self.assertEqual(rut_S(1), 12.56)
        
    def test_flatten_list(self):
        self.assertEqual(flatten_list(['a',2,[2,4,5],6,7]), ['a', 2, 2, 4, 5, 6, 7])
        self.assertEqual(flatten_list([1,2,[2,4,5],6,7]), [1, 2, 2, 4, 5, 6, 7])
        
        
    def tearDown(self):
        # Close the connection
        self.SDB.close()
        
        
            
        
if __name__ == '__main__':
    unittest.main()
    
    

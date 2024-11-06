import unittest
from funkcijos import *


class Test_funkcijos(unittest.TestCase):
        def setUp(self) -> None:
            self.A = 4
            self.B = 5

        def test_add(self):
            self.assertEqual(add(self.A, self.B), 9, msg='A nelygus B')
            self.assertEqual(add(-1,1), 0)
            self.assertNotEqual(add(-1,-1), 0)


        def test_multiply(self):
             self.assertEqual(multiply(self.A, self.B), 20, msg = 'A nelygus B')
             self.assertEqual(multiply(5,5), 25)
             self.assertNotEqual(multiply(-1,-1), 0)

        def test_minus(self):
            self.assertEqual(minus(self.A, self.B), -1, msg = 'A nelygus B')
            self.assertEqual(minus(5,5), 0)

        # def sqrroot(self):
        #     self.assertEqual(sqrroot(self.A, self.B), 2, msg = 'A nelygus B')
        #     self.assertEqual(sqrroot(5,5), 0)


        def test_unique_values(self):
            self.assertEqual(unique_values([1, 2, 2, 3, 4, 4]), [1, 2, 3, 4])
            self.assertEqual(unique_values([]), [])
            self.assertEqual(unique_values([1, 1, 1, 1]), [1])

        def test_remove_negatives(self):
            self.assertEqual(remove_negatives([1, -2, 3, -4, 5]), [1, 3, 5])
            self.assertEqual(remove_negatives([-1, -2, -3]), [])
            self.assertEqual(remove_negatives([0, 1, 2]), [0, 1, 2])

        def test_count_occurrences(self):
            self.assertEqual(count_occurrences([1, 2, 2, 3, 3, 3]), {1: 1, 2: 2, 3: 3})
            self.assertEqual(count_occurrences([]), {})
            self.assertEqual(count_occurrences([1, 1, 1]), {1: 3})

        def test_merge_unique(self):
            self.assertEqual(merge_unique([1, 2, 3], [3, 4, 5]), [1, 2, 3, 4, 5])
            self.assertEqual(merge_unique([], [1, 2]), [1, 2])
            self.assertEqual(merge_unique([1, 1], [1, 1]), [1])

        def test_duplicates(self):
            self.assertEqual(duplicates([1, 2, 2, 3, 3, 3]), [2, 3])
            self.assertEqual(duplicates([1, 2, 3]), [])
            self.assertEqual(duplicates([1, 1, 1]), [1])

        def test_circle_area(self):
            self.assertAlmostEqual(circle_area(1), math.pi)
            self.assertAlmostEqual(circle_area(0), 0)
            self.assertAlmostEqual(circle_area(2), 4 * math.pi)

        def test_sphere_volume(self):
            self.assertAlmostEqual(sphere_volume(1), (4/3) * math.pi)
            self.assertAlmostEqual(sphere_volume(0), 0)
            self.assertAlmostEqual(sphere_volume(2), (4/3) * math.pi * 8)


        def setUp(self):
            
            self.conn = sqlite3.connect(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\cars1.db")
            
        def tearDown(self):
            
            self.conn.close()

        def test_top_5_brands(self):
            result = top_5_brands(self.conn)
            self.assertEqual(len(result), 5)  
            self.assertIsInstance(result, list)  

        def test_avg_price_top_5_brands(self):
            result = avg_price_top_5_brands(self.conn)
            self.assertEqual(len(result), 5)  
            for manufacturer, avg_price in result.items():
                self.assertIsInstance(avg_price, float)  
                self.assertGreaterEqual(avg_price, 0)

if __name__ == '__main__':
     unittest.main()
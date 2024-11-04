import unittest
from funkcijos import *


class Test_funkcijos(unittest.TestCase):
    def setUp(self) -> None:
        self.A = 4
        self.B = 5
    
    def test_add(self):
        self.assertNotEqual(add(self.A, self.B), 11, msg='A nelygus B')
        self.assertEqual(add(-1,1), 0)
        self.assertNotEqual(add(-1,-1), 0)
        
    def test_divide(self):
        self.assertEqual(divide(5,5),1)

if __name__ == '__main__':
    unittest.main()
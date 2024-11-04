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
        
    def test_devide(self):
        self.assertEqual(devide(5,5),1)
        

if __name__ == '__main__':
    unittest.main()


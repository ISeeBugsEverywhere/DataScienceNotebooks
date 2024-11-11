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
        
    def test_divide(self):
        self.assertEqual(divide(5,5),1)
        self.assertRaises(ZeroDivisionError, divide, 1, 0)
        
    def test_multi(self):
        self.assertEqual(multi(5,5), 25)
        self.assertNotEqual(multi(5,5), 20)
        
    def test_substraction(self):
        self.assertEqual(substraction(5,4), 1)
        self.assertNotEqual(substraction(5,4), 2)
        
    def test_sakn(self):
        self.assertEqual(sakn(4), 2)
        self.assertNotEqual(sakn(4), 4)
        
    def test_uniq(self):
        self.assertEqual(uniq([5,5,4,4,3,3,2,1]), [1, 2, 3, 4, 5])
        self.assertNotEqual(uniq([5,5,4,4,3,3,2,1]), [1, 2, 3, 4, 5,5])
        
    def test_wot_neg(self):
        self.assertEqual(wotneg([5,-2,-1,4,3,1]), [1,3,4,5])
        self.assertRaises(TypeError, ap_plot, 'a')
        
    def test_countval(self):
        self.assertEqual(countval([5,5,4,4,3,3,2,1]), {1: 1, 2: 1, 3: 2, 4: 2, 5: 2})
        self.assertRaises(AttributeError, countval, {1:2})
        
    def test_uniqcon(self):
        self.assertEqual(uniqcon([5,5,4,4,3,3,2,1],[6,6,4,4,3,3,2,1]), [1,2,3,4,5,6])
        self.assertRaises(TypeError, uniqcon, 'a', None)
        
    def test_countmt1(self):
        self.assertEqual(countmt1([5,5,4,4,3,3,2,1]), [3,4,5])
        self.assertRaises(AttributeError, countmt1, {1:2})
        
    def test_ap_plot(self):
        self.assertEqual(ap_plot(3), 28.27)
        self.assertRaises(TypeError, ap_plot, [1,2,3])
        
    def test_rut_V(self):
        self.assertEqual(rut_V(5), 523.60)
        self.assertRaises(TypeError, rut_V, [1,2,3])
        
    def test_rut_S(self):
        self.assertEqual(rut_S(6), 452.39)
        self.assertRaises(TypeError, rut_S, [1,2,3])
        
    def test_flatten_and_get_unique(self):
        self.assertEqual(flatten_and_get_unique([1, 2, [2, 4, 5], 'a', None, 7]), [1, 2, 4, 5, 7, 'a'])
        
# class Test_funkcijos_autoplius(unittest.TestCase):
#     def setUp(self):
        
        
if __name__ == '__main__':
    unittest.main()
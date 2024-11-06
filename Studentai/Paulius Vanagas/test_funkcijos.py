import unittest
from funkcijos import *

class Test_funkcijos(unittest.TestCase):
    def setUp(self) -> None:
        self.A = 4
        self.B = 5
        
    def test_add(self):
        self.assertEqual(add(self.A, self.B), 9, msg='A nelygus B')
        self.assertEqual(add(-1, 1), 0)
        self.assertNotEqual(add(-1, -1), 0)
        
    def test_atimtis(self):
        self.assertEqual(atimtis(self.A, self.B), -1)
        self.assertEqual(atimtis(-1, 1), -2)
        self.assertEqual(atimtis(2, -1), 3)
        
    def test_daugyba(self):
        self.assertEqual(daugyba(self.A, self.B), 20)
        self.assertEqual(daugyba(-1, 1), -1)
        self.assertEqual(daugyba(-1, 0), 0)
        
    def test_dalyba(self):
        self.assertEqual(dalyba(self.A, self.B), 0.8)
        self.assertEqual(dalyba(-1, 1), -1)
        self.assertNotEqual(dalyba(-1, 0), 0)
        
    def test_kv_saknis(self):
        self.assertEqual(kv_saknis(self.A), 2)
        self.assertEqual(kv_saknis(25), 5)
        self.assertNotEqual(kv_saknis(-1), 0)
        self.assertEqual(kv_saknis(-25), 'netinkami duomenys')
        
    def test_unikalios(self):
        self.assertEqual(unikalios([4, 4, -2, 5, 4, 0, 'h']), {4, -2, 0, 5, 4, 'h'})
        self.assertEqual(unikalios([1, 1, 1, 1, 1]), {1})
        self.assertEqual(unikalios([]), set())
        
    def test_be_neigiamu(self):
        self.assertEqual(be_neigiamu([4, 4, -2, 5, 4, 0, 'h']), [4, 4, 5, 4, 0, 'h'])
        self.assertEqual(be_neigiamu([1, -3, '-1', None, 1]), [1, '-1', None, 1])
        self.assertEqual(be_neigiamu([]), list())
        
    def test_pasikartoja(self):
        self.assertEqual(pasikartoja(['w', 0, 'w', 1, None, None]), {None, 'w'})
        self.assertEqual(pasikartoja([None, -3, '-1',-3, None, 1]), {None, -3})
        self.assertEqual(pasikartoja([]), set())
        
    def test_sujungimas(self):
        self.assertEqual(sujungimas([None, 'la', 3], [4, 'la']), {None, 'la', 3, 4})
        self.assertEqual(sujungimas([2, 5, 5, 6, -3, 4, 't', 4, 't'], [2, 4, 4, 4, 0, 78, -4]), {0, 2, 4, 5, 6, 78, -4, -3, 't'})
        self.assertEqual(sujungimas([], []), set())
        
    def test_apskritimo_plotas(self):
        self.assertEqual(apskritimo_plotas(0), 0)
        self.assertEqual(apskritimo_plotas(2), 12.56)
        self.assertEqual(apskritimo_plotas(-2), 'spindulys neigiamas')
        self.assertRaises(TypeError, apskritimo_plotas, 'la')
        
    def test_rutulio_turis(self):
        self.assertEqual(rutulio_turis(0), 0)
        self.assertEqual(rutulio_turis(2), 33.49)
        self.assertEqual(rutulio_turis(-2), 'spindulys neigiamas')
        self.assertRaises(TypeError, rutulio_turis, 'la')
        
    def test_pavirsiaus_plotas(self):
        self.assertEqual(pavirsiaus_plotas(0), 0)
        self.assertEqual(pavirsiaus_plotas(2), 50.24)
        self.assertEqual(pavirsiaus_plotas(-2), 'spindulys neigiamas')
        self.assertRaises(TypeError, pavirsiaus_plotas, 'la')
        
    def test_flatten(self):
        self.assertEqual(flatten([1,2,[2,4,5],6,7]), [1, 2, 2, 4, 5, 6, 7])
        self.assertEqual(flatten([None,2,[2,4,5],6,'lambda']), [None, 2, 2, 4, 5, 6, 'lambda'])
        
        
        
if __name__=='__main__':
    unittest.main()
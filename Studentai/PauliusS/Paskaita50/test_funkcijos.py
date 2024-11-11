import unittest
from funkcijos import *


# class Test_funkcijos(unittest.TestCase):
#     def setUp(self) -> None:
#         self.A = 4
#         self.B = 5
    
#     def test_add(self):
#         self.assertNotEqual(add(self.A, self.B), 11, msg='A nelygus B')
#         self.assertEqual(add(-1,1), 0)
#         self.assertNotEqual(add(-1,-1), 0)
        
#     def test_divide(self):
#         self.assertEqual(divide(5,5),1)
#         # self.assertRaises(ZeroDivisionError, divide, 1, 0)  #nurodome funkcijos errora
    
# if __name__ == '__main__':
#     unittest.main()
    
    # pridėkite dar testus daugybai, atimčiai, kv. šaknies traikuimu
    


class Test_funkcijos(unittest.TestCase):
    def setUp(self) -> None:
        self.testinis_list = [1, 2, 2, 3, 4, 5, 6, 6, 7, 7, 7, 8, 9, 9, 10, 10]
        self.reikalingas_rezultatas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.listas_teigiamiems = [1,-1,2,-4,3]
        self.reikalingas_rezultatas_teigiamiems = [1,1,2,4,3]
        
        self.sarasas_pasikartojantiems = [1,1,1,2,3,3,4,5,5,5,5,5]
        self.zodynas_pasikartojantiems = {1:3,2:1,3:2,4:1,5:5}
        
        self.du_sarasai = [1,2,3,4,5]
        self.du_sarasai2 = [1,2,6]
        self.du_sarasai_rezultatas = [1,2,3,4,5,6]
        

    def test_unikalios_reiksmes(self):
        rezultatas = unikalios_reiksmes(self.testinis_list)
        self.assertCountEqual(rezultatas, self.reikalingas_rezultatas, msg="ne unikalios")   #.assertCountEqual - 

    def test_tik_teigiami(self):
        rezultatas2 = tik_teigiami(self.listas_teigiamiems)
        self.assertCountEqual(rezultatas2,self.reikalingas_rezultatas_teigiamiems, msg='ne teigiami')

    def test_pasikartoijimas(self):
        rezultatas3 = pasikartoijimas(self.sarasas_pasikartojantiems)
        self.assertCountEqual(rezultatas3,self.zodynas_pasikartojantiems, msg='ne pasikartojantys')
              
    def test_du_sarasai(self):
        rezultatas4 = du_sarasai(self.du_sarasai,self.du_sarasai2)
        self.assertEqual(du_sarasai(self.du_sarasai,self.du_sarasai2),self.du_sarasai_rezultatas)
    
    def test_pasikartojantys(self):
        self.assertEqual(pasikartojantys([1,1,2,3,4,4]),[1,4])
        
    def test_plotas_turis_pavirsius(self):
        self.assertEqual(plotas_turis_pavirsius(10),[314.1592653589793, 4188.790204786391, 1256.6370614359173])
    
if __name__ == '__main__':
    unittest.main()




#coding:utf-8
#......................................MODULES IMPORTANTS..............................................................#

from fonctions import QRcode
import unittest


#...........................................TESTS AUTOMATISÉS.............................................................#

class TestMesFonctions(unittest.TestCase):
    def setUp(self):
        self.command=QRcode()
    def test_MultiDansGF(self):
        self.assertEqual(self.command.MultiDansGF(0,2),0)
    def test_ProduitScalaireDansGF(self):
        self.assertEqual(self.command.ProduitScalaireDansGF([1,1],[1,2],1),3)
    def test_DegreDupolynome(self):
        self.assertEqual(self.command.DegreDupolynome([0,0,0,0,0,0,0,0,0,0]),-1)
    def test_SupprimeZeros(self):
        self.assertEqual(self.command.SupprimeZeros([0,0,0,0,0,1,2,4]),5)
    def test_AddPolynome2(self):
        self.assertEqual(self.command.AddPolynome2([0,1,0,1],[0,1,1,1],4),[0,0,1,0])
    def test_InModuleReserver(self):
        self.assertEqual(self.command.InModuleReserver(17,8),False)
    def test_InverseDansGF(self):
        self.assertEqual(self.command.InverseDansGF(1),1)
    def test_MiseAJour(self):
        self.assertEqual(self.command.MiseAJour([0,0,0,0,0],2,10),[0,0,10,0,0])
    def test_VersionETNiveauCorrection(self):
        self.assertEqual(self.command.VersionETNiveauCorrection("Bienvenu a Namur 2022! merci a vous"),(8,"H"))
    def test_IndicateurDemode(self):
        self.assertEqual(self.command.IndicateurDemode("2&leo10&"),("ascii","0100"))
    def test_IndicateurNombreCaractere(self):
        self.assertEqual(self.command.IndicateurNombreCaractere("Bienvenu a Namur 2022!"),8)
    def test_CapaciteECBloc(self):
        self.assertEqual(self.command.CapaciteECBloc(2,"M"),(28,16,1,28,0,0))
    def test_DivisionEnBloc(self):
        self.assertEqual(self.command.DivisionEnBloc("&leo10&",self.command.EncodageDesDonnees("&leo10&")), [[64, 114, 102, 198, 86, 243, 19, 2, 96]])
    def test_AddPolynome(self):
        self.assertEqual(self.command.AddPolynome([1,0,1,1],[0,1,1,1,0]),[1,1,0,0,0])
    def test_AjouteZero(self):
        self.assertEqual(self.command.AjouteZero([10,12,25],3),[10,12,25,0,0,0])
    def test_InfoSurLeFormat(self):
        self.assertEqual(self.command.InfoSurLeFormat(3,"Q"),[0,1,1,1,0,1,0,0,0,0,0,0,1,1,0])
    def test_InfoSurLaVersion(self):
        self.assertEqual(self.command.InfoSurLaVersion(7),[0,0,0,1,1,1,1,1,0,0,1,0,0,1,0,1,0,0])
    def test_MatriceQRcode(self):
        self.command.MatriceQRcode([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],8)
    def test_InModuleReserver(self):
        self.assertEqual(self.command.InModuleReserver(6,6,2),False)
    def test_Entrelacement(self):
        self.assertEqual(self.command.Entrelacement([[10,12,56,24,1],[12,3,6,5,5,12,0]]),[10,12,12,3,56,6,24,5,1,5,12,0])
    def test_Ordonne(self):
        self.assertEqual(self.command.Ordonne(self.command.DivisionEnBloc("Bienvenu a Namur 2022!",self.command.EncodageDesDonnees("Bienvenu a Namur 2022!"))),[[65, 100, 38, 150, 86, 231, 102, 86, 231, 82, 6, 18, 4, 230, 22, 215, 87, 34, 3, 35, 3, 35, 34, 16, 0, 236, 17, 236]])
    def test_Ordonne(self):
        self.assertEqual(self.command.Ordonne([[4,3,2,1],[12,23]]),[[1,2,3,4],[23,12]])
    def test_EntierEnBinaire(self):
        self.assertEqual(self.command.EntierEnBinaire([4]),["00000100"])
    def test_DivisionEuclidienne(self):
        self.assertEqual(self.command.DivisionEuclidienne([83, 67, 19, 155, 35, 91, 115, 27, 107, 155, 39, 179, 107, 27],self.command.Generateur("lkjhgjsklödijhbsdkncmsdömckljbshdcbslkdöljcsnld")),[99,  247,  94  ,77 , 227 , 4 , 80,  248  ,28 , 16  ,200  ,66 , 222 , 2 , 54  ,255  ,145 , 20,  109  ,92  ,115 , 214 , 29 , 157 , 39  ,113])




if __name__ == '__main__':
    unittest.main()






import unittest
from kassapaate import Kassapaate, EDULLINEN, MAUKAS
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_alussa_oikein(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_cheap_cash_enough_money_change_saldot_OK(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(500), 500-EDULLINEN)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000 + EDULLINEN)

    def test_tasty_cash_enough_money_change_saldot_OK(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(500), 500-MAUKAS)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000 + MAUKAS)

    def test_cheap_cash_NOT_enough_money_change_saldot_OK(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(100), 100)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_tasty_cash_NOT_enough_money_change_saldot_OK(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(100), 100)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)





    def test_cheap_credit_enough_money_saldot_OK(self):
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.maukkaat, 0)
        # alla ei kasvata fyysisesti käteisen määrän kassassa, joten poistin sen
        # self.assertEqual(self.kassa.kassassa_rahaa, 100000 + EDULLINEN)
    
    def test_cheap_credit_NOT_enough_money_saldot_OK(self):
        self.kortti.ota_rahaa(1000)
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), False)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)


    def test_tasty_credit_enough_money_saldot_OK(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 1)
        # alla ei kasvata fyysisesti käteisen määrän kassassa, joten poistin sen
        # self.assertEqual(self.kassa.kassassa_rahaa, 100000 + MAUKAS)
    
    def test_tasty_credit_NOT_enough_money_saldot_OK(self):
        self.kortti.ota_rahaa(1000)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), False)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kortille_lataus_OK(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 10)
        self.assertEqual(self.kortti.saldo, 1010)
        self.assertEqual(self.kassa.kassassa_rahaa, 100010)

    def test_kortille_lataus_neg_sum_OK(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -10)
        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
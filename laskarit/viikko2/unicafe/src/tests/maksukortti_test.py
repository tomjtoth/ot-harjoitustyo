import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_Kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_Rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(50)
        self.assertEqual(self.maksukortti.saldo, 1050)

    def test_Saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(50)
        self.assertEqual(self.maksukortti.saldo, 950)

    def test_Saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(500000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_Metodi_palauttaa_True_jos_rahat_riittivät_ja_muuten_False(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500000), False)
        self.assertEqual(self.maksukortti.ota_rahaa(5), True)

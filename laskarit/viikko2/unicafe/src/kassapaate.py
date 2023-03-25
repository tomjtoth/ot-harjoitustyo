EDULLINEN = 240
MAUKAS = 400

class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def syo_edullisesti_kateisella(self, maksu):
        if maksu >= EDULLINEN:
            self.kassassa_rahaa = self.kassassa_rahaa + EDULLINEN
            self.edulliset += 1
            return maksu - EDULLINEN
        else:
            return maksu

    def syo_maukkaasti_kateisella(self, maksu):
        if maksu >= MAUKAS:
            self.kassassa_rahaa = self.kassassa_rahaa + MAUKAS
            self.maukkaat += 1
            return maksu - MAUKAS
        else:
            return maksu

    def syo_edullisesti_kortilla(self, kortti):
        if kortti.saldo >= EDULLINEN:
            kortti.ota_rahaa(EDULLINEN)
            self.edulliset += 1
            return True
        else:
            return False

    def syo_maukkaasti_kortilla(self, kortti):
        if kortti.saldo >= MAUKAS:
            kortti.ota_rahaa(MAUKAS)
            self.maukkaat += 1
            return True
        else:
            return False

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.kassassa_rahaa += summa
        else:
            return

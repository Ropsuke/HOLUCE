from seaded import RUUT
class Kaamera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.sujuvus = 0.25

# Kaamera liigub sujuvalt 25% vahemaa võrra iga frame, kuni jõuab mängija juurde, mis tekitab sujuvuse
    def jälgi(self, mängija, ekraani_w, ekraani_h):
        siht_x = mängija.pix_x + 32 - (ekraani_w // 2)
        siht_y = mängija.pix_y + 64 - (ekraani_h // 2)
        self.x += (siht_x - self.x) * self.sujuvus
        self.y += (siht_y - self.y) * self.sujuvus

# Kaamera ei ole sujuv, vaid läheb kohe player kohale
    def tsentreeri(self, mängija, ekraani_w, ekraani_h):
        self.x = mängija.pix_x - (ekraani_w // 2) + (RUUT // 2)
        self.y = mängija.pix_y - (ekraani_h // 2) + (RUUT // 2)
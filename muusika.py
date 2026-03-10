import pygame
from seaded import (
    MUUSIKA_MENÜÜ, MUUSIKA_CAVE_ALG, MUUSIKA_CAVE_REP,
    KAARDI_INFO
)

LAUL_LÄBI = pygame.USEREVENT + 1

class MuusikaHaldur:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(LAUL_LÄBI)
        self.praegune = None

    def mängi_menüü(self):
        """Menüü muusika."""
        pygame.mixer.music.load(MUUSIKA_MENÜÜ)
        pygame.mixer.music.play(-1)
        self.praegune = "menu"

    def mängi_kaardi_muusika(self, olek):
        """Laeb ja mängib muusikat vastavalt mängu olekule."""
        if olek not in KAARDI_INFO:
            return
        info = KAARDI_INFO[olek]
        pygame.mixer.music.load(info["muusika"])
        pygame.mixer.music.play(-1 if info["loop"] else 0)
        self.praegune = info["laul_nimi"]

    def laul_lõppes(self):
        """Kutsu kui LAUL_LÄBI event tuleb. Haldab cave intro -> loop üleminekut."""
        if self.praegune == "intro":
            pygame.mixer.music.load(MUUSIKA_CAVE_REP)
            pygame.mixer.music.play(-1)
            self.praegune = "loop"
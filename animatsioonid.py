import pygame


class Animatsioon:
    """
    Ühe animatsiooni hoidja.
    frames: list pygame.Surface objektidest
    fps:    mitu kaadrit sekundis animatsioon mängib
    """

    def __init__(self, frames: list[pygame.Surface], fps: int = 8):
        self.frames    = frames
        self.fps       = fps
        self.indeks    = 0.0

    def uuenda(self, dt: float):
        """dt = aeg sekundites (nt 1/60 ühe frame kohta)."""
        self.indeks = (self.indeks + self.fps * dt) % len(self.frames)

    def praegune_kaader(self) -> pygame.Surface:
        return self.frames[int(self.indeks)]

    def reset(self):
        self.indeks = 0.0


class AnimatsioonHaldur:
    """
    Haldab mitut animatsiooni ja vahetab nende vahel.
    Animatsioonid on sõnastikus: {"kõndi_parem": Animatsioon, ...}
    """

    def __init__(self):
        self.animatsioonid: dict[str, Animatsioon] = {}
        self.praegune_nimi: str = ""

    def lisa(self, nimi: str, animatsioon: Animatsioon):
        self.animatsioonid[nimi] = animatsioon

    def sea(self, nimi: str):
        """Vaheta animatsiooni. Kui sama mis praegu, ei muuda midagi."""
        if nimi != self.praegune_nimi and nimi in self.animatsioonid:
            self.animatsioonid[nimi].reset()
            self.praegune_nimi = nimi

    def uuenda(self, dt: float):
        if self.praegune_nimi in self.animatsioonid:
            self.animatsioonid[self.praegune_nimi].uuenda(dt)

    def praegune_kaader(self) -> pygame.Surface | None:
        if self.praegune_nimi in self.animatsioonid:
            return self.animatsioonid[self.praegune_nimi].praegune_kaader()
        return None


def laadi_sprite_sheet(
    path: str,
    kaader_w: int,
    kaader_h: int,
    rida: int = 0,
    skaleeritud_w: int | None = None,
    skaleeritud_h: int | None = None,
) -> list[pygame.Surface]:
    """
    Laeb sprite sheet'i ja tagastab kaadrite listi ühest reast.

    path        : failitee
    kaader_w/h  : ühe kaadri suurus sprite sheetis
    rida        : mitmes rida (0-põhine)
    skaleeritud : soovi korral muudab suurust
    """
    sheet  = pygame.image.load(path).convert_alpha()
    kaadreid = sheet.get_width() // kaader_w
    frames = []

    for i in range(kaadreid):
        rect   = pygame.Rect(i * kaader_w, rida * kaader_h, kaader_w, kaader_h)
        kaader = sheet.subsurface(rect).copy()
        if skaleeritud_w and skaleeritud_h:
            kaader = pygame.transform.scale(kaader, (skaleeritud_w, skaleeritud_h))
        frames.append(kaader)

    return frames


def loo_varukaadrid(
    värv: tuple,
    kaader_w: int,
    kaader_h: int,
    arv: int = 2,
) -> list[pygame.Surface]:
    """
    Loob lihtsad ühevärvilised varukaadrid juhuks kui sprite faili ei leita.
    Annab kerge vilkumise efekti (hele/tume), et oleks näha et animatsioon töötab.
    """
    frames = []
    for i in range(arv):
        surf = pygame.Surface((kaader_w, kaader_h), pygame.SRCALPHA)
        brightness = 1.0 if i % 2 == 0 else 0.7
        c = tuple(min(255, int(ch * brightness)) for ch in värv)
        surf.fill(c)
        frames.append(surf)
    return frames
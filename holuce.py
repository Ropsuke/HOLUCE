import pygame
import os
import json
from kaardid import koobas
from kaardid import spawn_map
from kaardid import minu_poe_kaart

pygame.init()
pygame.mixer.init()
d = 1
# ============================================================
#  MUUSIKA
# ============================================================
MUUSIKA_MENÜÜ    = os.path.join("assets/music", "menu.mp3")
MUUSIKA_CAVE_ALG = os.path.join("assets/music", "cave_begin.mp3")
MUUSIKA_CAVE_REP = os.path.join("assets/music", "cave_rep.mp3")
MUUSIKA_SPAWN    = os.path.join("assets/music", "forest.mp3")
MUUSIKA_POOD     = os.path.join("assets/music", "shop.mp3")

LAUL_LÄBI = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(LAUL_LÄBI)
pygame.mixer.music.load(MUUSIKA_MENÜÜ)
pygame.mixer.music.play(-1)
praeg_laul = "menu"

# ============================================================
#  EKRAAN
# ============================================================
info   = pygame.display.Info()
WIDTH  = info.current_w
HEIGHT = info.current_h - 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED, vsync=1)
pygame.display.set_caption("Holuce")
KELL = pygame.time.Clock()
FPS  = 60
kaamera_x = 0
kaamera_y = 0

SPRITE_ENTITIES_FOLDER = "assets/entities"
SPRITE_PILDID_FOLDER   = "assets/pictures"

# ============================================================
#  VÄRVID
# ============================================================
FONT            = pygame.font.SysFont("arial", 60)
RUUT            = 64
VALGE           = (255, 255, 255)
MUST            = (0,   0,   0)
HALL            = (122, 122, 122)
SININE          = (0,   0,   255)
PRUUN           = (139, 69,  19)
TUME_HALL       = (64,  64,  64)
TUME_ROHELINE   = (0,   70,  0)
TUME_PRUUN      = (100, 50,  0)
TUME_TUME_PRUUN = (65,  30,  0)

# ============================================================
#  PILDID
# ============================================================
grass_pilt = pygame.image.load(
    os.path.join(SPRITE_PILDID_FOLDER, "grassy.png")
).convert_alpha()
grass_pilt = pygame.transform.scale(grass_pilt, (RUUT, RUUT))

# ============================================================
#  OLEKUD
# ============================================================
MENU        = "menu"
MÄNG_KOOBAS = "mäng"
MÄNG_SPAWN  = "spawn"
MÄNG_POOD   = "pood"
VÕIT        = "võit"
P_OLEK      = MENU

# ============================================================
#  KAARTIDE VÄRVITABELID
# ============================================================
SPAWN_VÄRVID = {
    "E":  TUME_ROHELINE,
    "K":  TUME_HALL,
    "T":  PRUUN,
    "TT": TUME_PRUUN,
    "D":  PRUUN,
}
SPAWN_PILDID = {"g", "S"}

KOOBAS_VÄRVID = {
    "W": HALL,
    ".": TUME_HALL,
    "S": TUME_HALL,
    "D": PRUUN,
}
KOOBAS_PILDID = set()

POOD_VÄRVID = {
    "g":  PRUUN,
    "SS": TUME_PRUUN,
    ".":  TUME_PRUUN,
    "S":  TUME_PRUUN,
    "E":  TUME_TUME_PRUUN,
}
POOD_PILDID = set()

# ============================================================
#  JOONISTAMINE
# ============================================================
def joonista_kaart(kaart, värvid, kx, ky, pildid=None):
    if pildid is None:
        pildid = set()
    for y, rida in enumerate(kaart):
        for x, ruut in enumerate(rida):
            sx = x * RUUT - kx
            sy = y * RUUT - ky
            if sx < -RUUT or sx > WIDTH or sy < -RUUT or sy > HEIGHT:
                continue
            if ruut in pildid:
                SCREEN.blit(grass_pilt, (sx, sy))
            elif ruut in värvid:
                pygame.draw.rect(SCREEN, värvid[ruut], (sx, sy, RUUT, RUUT))

# ============================================================
#  VALGUS
# ============================================================
valgus = pygame.Surface((WIDTH, HEIGHT))
def loo_valgus():
    valgus.fill((0, 0, 0))
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.circle(valgus, (50,  50,  50),  (cx, cy), int(RUUT * 2.5))
    pygame.draw.circle(valgus, (150, 150, 150), (cx, cy), RUUT * 2)
    pygame.draw.circle(valgus, (255, 255, 255), (cx, cy), int(RUUT * 1.5))
loo_valgus()

# ============================================================
#  AKTIIVNE KAART
# ============================================================
MAP = spawn_map

# ============================================================
#  PLAYER KLASS — VABA LIIKUMINE
# ============================================================
# Läbitavad ruudud (kasutavad kõik kaardid)
VABAD = {".", "S", "D", "g", "TT", "SS"}

class Player:
    def __init__(self):
        self.pix_x = 1.0 * RUUT
        self.pix_y = 1.0 * RUUT
        self.kiirus = 7

        # ── HITBOX konfig ──
        # Sprite on 64x64, aga hitbox on väiksem:
        #
        #   ┌────────────────┐  64px (sprite)
        #   │                │
        #   │    ┌──────┐    │
        #   │    │HITBOX│    │  <- 32x40, keskele nihutud
        #   │    │      │    │
        #   │    └──────┘    │
        #   └────────────────┘
        #
        self.hb_ox = 16      # hitbox X nihe sprite'i seest
        self.hb_oy = 12      # hitbox Y nihe sprite'i seest
        self.hb_w  = 32      # hitbox laius
        self.hb_h  = 40      # hitbox kõrgus

        # Pildid
        pilt = os.path.join(SPRITE_ENTITIES_FOLDER, "player.png")
        lae = pygame.image.load(pilt).convert_alpha()
        skaleeritud = pygame.transform.scale(lae, (RUUT/2, RUUT))
        self.img_parem = skaleeritud
        self.img_vasak = pygame.transform.flip(skaleeritud, True, False)
        self.image = self.img_parem

    # ── Hitboxi nurkade kontroll ──
    def _on_vaba(self, px, py, kaart):
        """Kas hitbox positsioonil (px, py) on täielikult vabadel ruutudel?"""
        # Hitboxi servad
        vasak  = px + self.hb_ox
        parem  = px + self.hb_ox + self.hb_w
        üleval = py + self.hb_oy
        all_   = py + self.hb_oy + self.hb_h

        # Kontrolli kõiki 4 nurka
        nurgad = [
            (vasak, üleval),   # üleval-vasak
            (parem, üleval),   # üleval-parem
            (vasak, all_),     # all-vasak
            (parem, all_),     # all-parem
        ]

        for nx, ny in nurgad:
            gx = int(nx // RUUT)
            gy = int(ny // RUUT)

            # Kaardi piir = sein
            if gy < 0 or gy >= len(kaart) or gx < 0 or gx >= len(kaart[0]):
                return False
            if kaart[gy][gx] not in VABAD:
                return False

        return True

    # ── Vaba liikumine ──
    def move_vaba(self, dx, dy, kaart):
        """
        Liigutab mängijat pikslite kaupa.
        Libisev kokkupõrge: X ja Y kontrollitakse eraldi.
        Tagastab: 0=tühi, 1=uks, 2=trepp üles, 3=trepp alla
        """
        sammx = dx * self.kiirus
        sammy = dy * self.kiirus

        # ── X-telg eraldi ──
        if self._on_vaba(self.pix_x + sammx, self.pix_y, kaart):
            self.pix_x += sammx
        else:
            astme_suund = 1 if sammx > 0 else -1
            for _ in range(int(abs(sammx))):
                if self._on_vaba(self.pix_x + astme_suund, self.pix_y, kaart):
                    self.pix_x += astme_suund
                else:
                    break
        # ── Y-telg eraldi (kasutab juba uuendatud pix_x!) ──
        if self._on_vaba(self.pix_x, self.pix_y + sammy, kaart):
            self.pix_y += sammy
        else:
            # Sama loogika Y-teljega
            astme_suund = 1 if sammy > 0 else -1
            for _ in range(int(abs(sammy))):
                if self._on_vaba(self.pix_x, self.pix_y + astme_suund, kaart):
                    self.pix_y += astme_suund
                else:
                    break
        # ── Sprite suund ──
        if dx > 0:
            self.image = self.img_parem
        elif dx < 0:
            self.image = self.img_vasak

        # ── Kontroll: millisel ruudul on hitboxi KESKPUNKT? ──
        kesk_x = int((self.pix_x + self.hb_ox + self.hb_w / 2) // RUUT)
        kesk_y = int((self.pix_y + self.hb_oy + self.hb_h / 2) // RUUT)

        if 0 <= kesk_y < len(kaart) and 0 <= kesk_x < len(kaart[0]):
            ruut = kaart[kesk_y][kesk_x]
            if ruut == "D":  return 1
            if ruut == "TT": return 2
            if ruut == "SS": return 3

        return 0

    # ── Joonistamine ──
    def draw(self, kx, ky):
        SCREEN.blit(self.image, (self.pix_x - kx+15, self.pix_y - ky))

    # ── Hitboxi joonistamine (DEBUG) ──
    def draw_hitbox(self, kx, ky):
        """Kutsuge seda kui tahate hitboxi näha (punane kast)."""
        hb = pygame.Rect(
            self.pix_x + self.hb_ox - kx,
            self.pix_y + self.hb_oy - ky,
            self.hb_w, self.hb_h
        )
        pygame.draw.rect(SCREEN, (255, 0, 0), hb, 2)

    # ── Alguspositsioon ──
    def set_start_pos(self, kaart):
        for y, rida in enumerate(kaart):
            for x, ruut in enumerate(rida):
                if ruut == "S":
                    self.pix_x = float(x * RUUT)
                    self.pix_y = float(y * RUUT)
                    return
        self.pix_x = float(RUUT)
        self.pix_y = float(RUUT)

# ============================================================
#  SALVESTA / LAE
# ============================================================
def salvesta_mang():
    andmed = {
        "pix_x": mängija.pix_x,
        "pix_y": mängija.pix_y,
        "olek":  P_OLEK,
        "kaart": MAP if P_OLEK == MÄNG_KOOBAS else None,
    }
    with open("savegame.json", "w") as f:
        json.dump(andmed, f)
    print("Mäng salvestatud!")

def lae_mang():
    global MAP, P_OLEK, praeg_laul
    if not os.path.exists("savegame.json"):
        print("Salvestust ei leitud!")
        return
    with open("savegame.json", "r") as f:
        andmed = json.load(f)

    mängija.pix_x = float(andmed["pix_x"])
    mängija.pix_y = float(andmed["pix_y"])
    P_OLEK = andmed["olek"]

    if P_OLEK == MÄNG_KOOBAS:
        MAP = andmed["kaart"]
        pygame.mixer.music.load(MUUSIKA_CAVE_ALG)
        pygame.mixer.music.play(0)
        praeg_laul = "intro"
    elif P_OLEK == MÄNG_SPAWN:
        MAP = spawn_map
        pygame.mixer.music.load(MUUSIKA_SPAWN)
        pygame.mixer.music.play(-1)
        praeg_laul = "forest"
    elif P_OLEK == MÄNG_POOD:
        MAP = minu_poe_kaart
        pygame.mixer.music.load(MUUSIKA_POOD)
        pygame.mixer.music.play(-1)
        praeg_laul = "shop"
    print("Mäng laetud!")

# ============================================================
#  INIT
# ============================================================
mängija   = Player()
kaamera_x = 0
kaamera_y = 0

nupp1 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 240, 400, 100)
nupp2 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 90,  400, 100)
nupp3 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 60,  400, 100)
nupp4 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 210, 400, 100)

# Debug mode: sea True et näha hitboxi
DEBUG_HITBOX = False

# ============================================================
#  SISEND
# ============================================================
def loe_sisend():
    keys = pygame.key.get_pressed()
    dx, dy = 0.0, 0.0
    if keys[pygame.K_UP]    or keys[pygame.K_w]: dy = -1.0
    if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy =  1.0
    if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx = -1.0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx =  1.0

    # Diagonaali kiiruse parandus
    if dx != 0 and dy != 0:
        dx *= 0.707
        dy *= 0.707

    return dx, dy

# ============================================================
#  MAIN LOOP
# ============================================================
running = True

while running:
    SCREEN.fill(MUST)

    # ==================== SÜNDMUSED ====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD):
                salvesta_mang()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if P_OLEK == MENU:
                if nupp1.collidepoint(event.pos):
                    MAP = spawn_map
                    mängija.set_start_pos(MAP)
                    P_OLEK = MÄNG_SPAWN
                    pygame.mixer.music.load(MUUSIKA_SPAWN)
                    pygame.mixer.music.play(-1)
                    praeg_laul = "forest"
                elif nupp2.collidepoint(event.pos):
                    lae_mang()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD, VÕIT):
                    salvesta_mang()
                    P_OLEK = MENU
                    pygame.mixer.music.load(MUUSIKA_MENÜÜ)
                    pygame.mixer.music.play(-1)
                    praeg_laul = "menu"
            # Debug toggle
            if event.key == pygame.K_F1:
                DEBUG_HITBOX = not DEBUG_HITBOX

        elif event.type == LAUL_LÄBI:
            if praeg_laul == "intro":
                pygame.mixer.music.load(MUUSIKA_CAVE_REP)
                pygame.mixer.music.play(-1)
                praeg_laul = "loop"

    # ==================== MENÜÜ ====================
    if P_OLEK == MENU:
        for nupp, tekst_str in [
            (nupp1, "New Game"), (nupp2, "Continue"),
            (nupp3, "Settings"), (nupp4, "Credits"),
        ]:
            pygame.draw.rect(SCREEN, SININE, nupp, border_radius=20)
            tekst = FONT.render(tekst_str, True, MUST)
            SCREEN.blit(tekst, tekst.get_rect(center=nupp.center))

    # ==================== MÄNG ====================
    elif P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD):

        # ── SISEND + LIIKUMINE ──
        dx, dy  = loe_sisend()
        tulemus = mängija.move_vaba(dx, dy, MAP)

        # ── KAAMERA ──
        siht_x = mängija.pix_x - (WIDTH // 2) + (RUUT // 2)
        siht_y = mängija.pix_y - (HEIGHT // 2) + (RUUT // 2)
        kaamera_x += (siht_x - kaamera_x) * 0.1
        kaamera_y += (siht_y - kaamera_y) * 0.1

        # ── ÜLEMINEKUD ──
        if tulemus != 0:
            if P_OLEK == MÄNG_SPAWN and tulemus == 1:
                MAP = koobas(20, 30)
                mängija.set_start_pos(MAP)
                P_OLEK = MÄNG_KOOBAS
                pygame.mixer.music.load(MUUSIKA_CAVE_ALG)
                pygame.mixer.music.play(0)
                praeg_laul = "intro"

            elif P_OLEK == MÄNG_SPAWN and tulemus == 2:
                MAP = minu_poe_kaart
                mängija.set_start_pos(MAP)
                P_OLEK = MÄNG_POOD
                pygame.mixer.music.load(MUUSIKA_POOD)
                pygame.mixer.music.play(-1)
                praeg_laul = "shop"

            elif P_OLEK == MÄNG_KOOBAS and tulemus == 1:
                P_OLEK = VÕIT

            elif P_OLEK == MÄNG_POOD and tulemus == 3:
                MAP = spawn_map
                mängija.set_start_pos(MAP)
                P_OLEK = MÄNG_SPAWN
                pygame.mixer.music.load(MUUSIKA_SPAWN)
                pygame.mixer.music.play(-1)
                praeg_laul = "forest"

            # Kaamera uuendus pärast üleminekut
            kaamera_x = int(mängija.pix_x - (WIDTH  // 2) + (RUUT // 2))
            kaamera_y = int(mängija.pix_y - (HEIGHT // 2) + (RUUT // 2))

        # ── JOONISTAMINE ──
        if P_OLEK == MÄNG_SPAWN:
            joonista_kaart(MAP, SPAWN_VÄRVID, kaamera_x, kaamera_y, SPAWN_PILDID)
        elif P_OLEK == MÄNG_KOOBAS:
            joonista_kaart(MAP, KOOBAS_VÄRVID, kaamera_x, kaamera_y, KOOBAS_PILDID)
        elif P_OLEK == MÄNG_POOD:
            joonista_kaart(MAP, POOD_VÄRVID, kaamera_x, kaamera_y, POOD_PILDID)

        # Mängija peale kaarti
        if P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD):
            mängija.draw(kaamera_x, kaamera_y)

            # Debug: näita hitboxi (F1 toggle)
            if DEBUG_HITBOX:
                mängija.draw_hitbox(kaamera_x, kaamera_y)

        # Pimedus koopas
        if P_OLEK == MÄNG_KOOBAS:
            SCREEN.blit(valgus, (0, 0), special_flags=pygame.BLEND_MULT)

    # ==================== VÕIT ====================
    elif P_OLEK == VÕIT:
        tekst = FONT.render("Võitsid mängu!", True, VALGE)
        SCREEN.blit(tekst, tekst.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    KELL.tick(FPS)

pygame.quit()
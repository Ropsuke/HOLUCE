import pygame
import os
import time
from kaardid import *
from seaded import *
from mangija import *
from kaamera import *
from muusika import MuusikaHaldur, LAUL_LÄBI
from salvestus import salvesta_mang, lae_mang

pygame.init()

# Ei tea kuhu panna, seega panen siia

FONT = pygame.font.SysFont(FONDI_NIMI, FONDI_SUURUS)
muusika = MuusikaHaldur()
muusika.mängi_menüü()

#  EKRAAN

ekraani_info   = pygame.display.Info()
WIDTH  = ekraani_info.current_w
HEIGHT = ekraani_info.current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED, vsync=1)
pygame.display.set_caption("Holuce")
KELL = pygame.time.Clock()

#  PILDID

grass_pilt = pygame.image.load(
    os.path.join(SPRITE_PILDID_FOLDER, "muru.png")
).convert_alpha()
grass_pilt = pygame.transform.scale(grass_pilt, (RUUT, RUUT))
grass_pilt1 = pygame.image.load(
    os.path.join(SPRITE_PILDID_FOLDER, "muru2.png")
).convert_alpha()
grass_pilt1 = pygame.transform.scale(grass_pilt1, (RUUT, RUUT))

# JOONISTAMINE

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
                SCREEN.blit(grass_pilt1, (sx, sy))
            elif ruut in värvid:
                pygame.draw.rect(SCREEN, värvid[ruut], (sx, sy, RUUT, RUUT))

# VALGUS

valgus = pygame.Surface((WIDTH, HEIGHT))
def loo_valgus():
    valgus.fill((0, 0, 0))
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.circle(valgus, (50,  50,  50),  (cx, cy), int(RUUT * 2.5))
    pygame.draw.circle(valgus, (150, 150, 150), (cx, cy), RUUT * 2)
    pygame.draw.circle(valgus, (255, 255, 255), (cx, cy), int(RUUT * 1.5))
loo_valgus()

# AKTIIVNE KAART

MAP = spawn_map

#  INIT

P_OLEK = MENU
mängija = Player()
kaamera = Kaamera()

nupp1 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 240, 400, 100)
nupp2 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 90,  400, 100)
nupp3 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 60,  400, 100)
nupp4 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 210, 400, 100)

# Debug mode: sea True et näha hitboxi
DEBUG_HITBOX = False


#  SISEND

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

#  MAIN LOOP

running = True

while running:
    SCREEN.fill(MUST)

    # ==================== SÜNDMUSED ====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD):
                salvesta_mang(mängija, P_OLEK, MAP)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if P_OLEK == MENU:
                if nupp1.collidepoint(event.pos):
                    MAP = spawn_map
                    mängija.set_start_pos(MAP)
                    P_OLEK = MÄNG_SPAWN
                    kaamera.tsentreeri(mängija, WIDTH, HEIGHT)
                    SCREEN.fill(MUST)
                    tekst = FONT.render("Loading...", True, VALGE)
                    SCREEN.blit(tekst, tekst.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                    pygame.display.flip()
                    time.sleep(0.3)
                    muusika.mängi_kaardi_muusika(P_OLEK)
                elif nupp2.collidepoint(event.pos):
                    tulemus = lae_mang(mängija)
                    if tulemus:
                        P_OLEK, salvestatud_kaart = tulemus

                        if P_OLEK == MÄNG_KOOBAS:
                            MAP = salvestatud_kaart
                        elif P_OLEK == MÄNG_SPAWN:
                            MAP = spawn_map
                        elif P_OLEK == MÄNG_POOD:
                            MAP = minu_poe_kaart

                        muusika.mängi_kaardi_muusika(P_OLEK)
                        kaamera.tsentreeri(mängija, WIDTH, HEIGHT)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD, VÕIT):
                    salvesta_mang(mängija, P_OLEK, MAP)
                    P_OLEK = MENU
                    muusika.mängi_menüü()
            # Debug toggle
            if event.key == pygame.K_F1:
                DEBUG_HITBOX = not DEBUG_HITBOX

        elif event.type == LAUL_LÄBI:
            muusika.laul_lõppes()

    # MENÜÜ
    if P_OLEK == MENU:
        for nupp, tekst_str in [
            (nupp1, "New Game"), (nupp2, "Continue"),
            (nupp3, "Settings"), (nupp4, "Credits"),
        ]:
            pygame.draw.rect(SCREEN, SININE, nupp, border_radius=20)
            tekst = FONT.render(tekst_str, True, MUST)
            SCREEN.blit(tekst, tekst.get_rect(center=nupp.center))

    # MÄNG 
    elif P_OLEK in (MÄNG_SPAWN, MÄNG_KOOBAS, MÄNG_POOD):

        # SISEND + LIIKUMINE
        dx, dy  = loe_sisend()
        tulemus = mängija.move_vaba(dx, dy, MAP)

        # KAAMERA
        kaamera.jälgi(mängija, WIDTH, HEIGHT)

        # ÜLEMINEKUD
        if tulemus != 0:
            if P_OLEK == MÄNG_SPAWN and tulemus == 1:
                MAP = koobas(20, 30)
                mängija.set_start_pos(MAP)
                P_OLEK = MÄNG_KOOBAS
                muusika.mängi_kaardi_muusika(P_OLEK)
                
            elif P_OLEK == MÄNG_SPAWN and tulemus == 2:
                MAP = minu_poe_kaart
                mängija.set_start_pos(MAP)
                P_OLEK = MÄNG_POOD
                muusika.mängi_kaardi_muusika(P_OLEK)

            elif P_OLEK == MÄNG_KOOBAS and tulemus == 1:
                P_OLEK = VÕIT

            elif P_OLEK == MÄNG_POOD and tulemus == 3:
                MAP = spawn_map
                mängija.set_start_pos(MAP)
                P_OLEK = MÄNG_SPAWN
                muusika.mängi_kaardi_muusika(P_OLEK)
                
            kaamera.tsentreeri(mängija, WIDTH, HEIGHT)

        # ── JOONISTAMINE ──
        info = KAARDI_INFO[P_OLEK]
        joonista_kaart(MAP, info["värvid"], kaamera.x, kaamera.y, info["pildid"])

        mängija.draw(SCREEN, kaamera.x, kaamera.y)

        if DEBUG_HITBOX:
            mängija.draw_hitbox(SCREEN, kaamera.x, kaamera.y)

        # Pimedus koopas
        if P_OLEK == MÄNG_KOOBAS:
            SCREEN.blit(valgus, (0, 0), special_flags=pygame.BLEND_MULT)


    elif P_OLEK == VÕIT:
        tekst = FONT.render("Võitsid mängu!", True, VALGE)
        SCREEN.blit(tekst, tekst.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    KELL.tick(FPS)

pygame.quit()
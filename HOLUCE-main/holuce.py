import pygame
import os
import json
import sys
import math
import random
from kaardid import koobas
from kaardid import spawn_map
from kaardid import minu_poe_kaart
pygame.init()
pygame.mixer.init()

# muusika ja sound effect'id
MUUSIKA_MENÜÜ = os.path.join("assets/music", "menu.mp3")
MUUSIKA_CAVE_ALG = os.path.join("assets/music", "cave_begin.mp3")
MUUSIKA_CAVE_REP = os.path.join("assets/music", "cave_rep.mp3")
MUUSIKA_SPAWN = os.path.join("assets/music", "forest.mp3")
MUUSIKA_POOD = os.path.join("assets/music", "shop.mp3")
LAUL_LÄBI = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(LAUL_LÄBI)
pygame.mixer.music.load(MUUSIKA_MENÜÜ)
pygame.mixer.music.play(-1)
praeg_laul = "menu"
# seaded
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h - 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Holuce")
KELL = pygame.time.Clock()
FPS = 60
MUUSIKA_FOLDER = "assets/music"
SPRITE_TÄHED_FOLDER = "assets/letters"
SPRITE_ENTITIES_FOLDER = "assets/entities"
SPRITE_PILDID_FOLDER = "assets/pictures"
WORD = "HOLUCE"

# visuaal
FONT = pygame.font.SysFont("arial", 60)
RUUT = 64
VALGE = (255, 255, 255)
MUST = (0, 0, 0)
HALL = (122, 122, 122)
PUNANE = (255, 0 , 0)
ROHELINE = (0, 255, 0)
SININE = (0, 0, 255)
PRUUN = (139, 69, 19)
TUME_HALL = (64, 64, 64)
TUME_ROHELINE = (0, 70, 0)
TUME_PRUUN = (100, 50, 0)

#### muru
pilt = os.path.join(SPRITE_PILDID_FOLDER, "grass.png")
lae_pilt = pygame.image.load(pilt).convert_alpha()
scale_pilt = pygame.transform.scale(lae_pilt, (RUUT, RUUT))

def salvesta_mang():
    andmed = {
        "x": mängija.x,
        "y": mängija.y,
        "olek": P_OLEK,
        "kaart": MAP if P_OLEK == MÄNG_KOOBAS else None
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

    mängija.x = andmed["x"]
    mängija.y = andmed["y"]
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
####
# mängu olekud ja menüüd
MENU = "menu"
MÄNG_KOOBAS = "mäng"
MÄNG_SPAWN = "spawn"
MÄNG_POOD = "pood"
VÕIT = "võit"
P_OLEK = MENU

# funktsioonid
valgus = pygame.Surface((WIDTH, HEIGHT))
def loo_valgus():
    valgus.fill((0, 0, 0))
    x, y = WIDTH // 2, HEIGHT // 2
    pygame.draw.circle(valgus, (50, 50, 50), (x, y), RUUT * 2.5)
    pygame.draw.circle(valgus, (150, 150, 150), (x, y), RUUT * 2)
    pygame.draw.circle(valgus, (255, 255, 255), (x, y), RUUT * 1.5)
loo_valgus()
MAP = koobas(20, 30)
# klassid
kas_koobas = 0
class Player:
    def __init__(self):
        self.x, self.y = (1, 1)
        self.move_timer = 0
        self.move_delay = 150
        pilt = os.path.join(SPRITE_ENTITIES_FOLDER, "parem_player.png")
        lae_pilt = pygame.image.load(pilt).convert_alpha()
        scale_pilt = pygame.transform.scale(lae_pilt, (RUUT, RUUT))
        self.img_parem = scale_pilt
        self.img_vasak = pygame.transform.flip(scale_pilt, True, False)
        self.image = self.img_parem
    def draw(self, kaamera_x, kaamera_y):
        screen_x = (self.x * RUUT) - kaamera_x
        screen_y = (self.y * RUUT) - kaamera_y
        SCREEN.blit(self.image, (screen_x, screen_y))
    def move(self, dx, dy):
        target_x = self.x + dx
        target_y = self.y + dy
        see = MAP[target_y][target_x]
        if see == "." or see == "S" or see == "D" or see == "g" or see == "TT" or see == "SS":
            self.x = target_x
            self.y = target_y
            if see == "D": return 1  # Koobas
            if see == "TT": return 2 # Pood
            if see == "SS": return 3 #spawn
            if dx == 1:
                self.image = self.img_parem
            elif dx == -1:
                self.image = self.img_vasak
        return 0
    def set_start_pos(self):
        global MAP
        leitud = False
        for y, rida in enumerate(MAP):
            for x, ruut in enumerate(rida):
                if ruut == "S":
                    self.x = x
                    self.y = y
                    leitud = True
            if not leitud:
                self.x = 1
                self.y = 1
kaamera_x = 0
kaamera_y = 0
mängija = Player()
nupp1 = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 -240, 400, 100, )
nupp2 = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 90, 400, 100, )
nupp3 = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 60, 400, 100, )
nupp4 = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 210, 400, 100, )
# main loop
running = True
while running:
    SCREEN.fill(MUST)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if P_OLEK == MÄNG_SPAWN or P_OLEK == MÄNG_KOOBAS:
                salvesta_mang()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if P_OLEK == MENU and nupp1.collidepoint(event.pos):
                MAP = spawn_map
                mängija.set_start_pos()
                P_OLEK = MÄNG_SPAWN
                pygame.mixer.music.load(MUUSIKA_SPAWN)
                pygame.mixer.music.play(-1)
                praeg_laul = "forest"
                mängija.move_timer = 0
            if P_OLEK == MENU and nupp2.collidepoint(event.pos):
                lae_mang()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and (P_OLEK == MÄNG_SPAWN or P_OLEK == MÄNG_KOOBAS or P_OLEK == VÕIT):
                salvesta_mang()
                P_OLEK = MENU
                pygame.mixer.music.load(MUUSIKA_MENÜÜ)
                pygame.mixer.music.play(-1)
                praeg_laul = "menu"
        if event.type == LAUL_LÄBI:
            if praeg_laul == "intro":
                pygame.mixer.music.load(MUUSIKA_CAVE_REP)
                pygame.mixer.music.play(-1)
                praeg_laul = "loop"
    if P_OLEK == MENU:
        pygame.draw.rect(SCREEN, SININE, nupp1, border_radius=20)
        pygame.draw.rect(SCREEN, SININE, nupp2, border_radius=20)
        pygame.draw.rect(SCREEN, SININE, nupp3, border_radius=20)
        pygame.draw.rect(SCREEN, SININE, nupp4, border_radius=20)
        tekst1 = FONT.render("New game", True, MUST)
        tekst2 = FONT.render("Continue", True, MUST)
        tekst3 = FONT.render("Settings", True, MUST)
        tekst4 = FONT.render("Credits", True, MUST)
        tsenter1 = tekst1.get_rect(center=nupp1.center)
        tsenter2 = tekst2.get_rect(center=nupp2.center)
        tsenter3 = tekst3.get_rect(center=nupp3.center)
        tsenter4 = tekst4.get_rect(center=nupp4.center)
        SCREEN.blit(tekst1, tsenter1)
        SCREEN.blit(tekst2, tsenter2)
        SCREEN.blit(tekst3, tsenter3)
        SCREEN.blit(tekst4, tsenter4)

    if P_OLEK == MÄNG_KOOBAS:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - mängija.move_timer > mängija.move_delay:
            dx = 0
            dy = 0
            if keys[pygame.K_UP]: dy = -1
            elif keys[pygame.K_DOWN]: dy = 1
            elif keys[pygame.K_LEFT]: dx = -1
            elif keys[pygame.K_RIGHT]: dx = 1
            if dx != 0 or dy != 0:
                kas_võit = mängija.move(dx, dy)
                mängija.move_timer = current_time
                if kas_võit == True:
                    P_OLEK = VÕIT
        kaamera_x = (mängija.x * RUUT) - (WIDTH // 2) + (RUUT // 2)
        kaamera_y = (mängija.y * RUUT) - (HEIGHT // 2) + (RUUT // 2)
        for y, rida in enumerate(MAP):
            for x, ruut in enumerate(rida):
                screen_x = (x * RUUT) - kaamera_x
                screen_y = (y * RUUT) - kaamera_y
                if ruut == "W":
                    pygame.draw.rect(SCREEN, HALL,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "D":
                    pygame.draw.rect(SCREEN, PRUUN,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "." or ruut == "S":
                    pygame.draw.rect(SCREEN, TUME_HALL,(screen_x, screen_y, RUUT, RUUT))
        mängija.draw(kaamera_x, kaamera_y)
        SCREEN.blit(valgus, (0, 0), special_flags=pygame.BLEND_MULT)
    if P_OLEK == MÄNG_SPAWN:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - mängija.move_timer > mängija.move_delay:
            dx = 0
            dy = 0
            if keys[pygame.K_UP]: dy = -1
            elif keys[pygame.K_DOWN]: dy = 1
            elif keys[pygame.K_LEFT]: dx = -1
            elif keys[pygame.K_RIGHT]: dx = 1
            if dx != 0 or dy != 0:
                tulemus = mängija.move(dx, dy)
                mängija.move_timer = current_time
                if tulemus == 1:
                    P_OLEK = MÄNG_KOOBAS
                    MAP = koobas(20, 30)
                    mängija.set_start_pos()
                    pygame.mixer.music.load(MUUSIKA_CAVE_ALG)
                    pygame.mixer.music.play(0)
                    praeg_laul = "intro"
                elif tulemus == 2:
                    P_OLEK = MÄNG_POOD
                    MAP = minu_poe_kaart
                    mängija.set_start_pos()
                    pygame.mixer.music.load(MUUSIKA_POOD)
                    pygame.mixer.music.play(0)
                    praeg_laul = "shop"
        kaamera_x = (mängija.x * RUUT) - (WIDTH // 2) + (RUUT // 2)
        kaamera_y = (mängija.y * RUUT) - (HEIGHT // 2) + (RUUT // 2)
        for y, rida in enumerate(spawn_map):
            for x, ruut in enumerate(rida):
                screen_x = (x * RUUT) - kaamera_x
                screen_y = (y * RUUT) - kaamera_y
                if ruut == "E":
                    pygame.draw.rect(SCREEN, TUME_ROHELINE,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "g" or ruut == "S":
                    SCREEN.blit(scale_pilt, (screen_x, screen_y))
                elif ruut == "K":
                    pygame.draw.rect(SCREEN, TUME_HALL,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "T":
                    pygame.draw.rect(SCREEN, PRUUN,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "TT":
                    pygame.draw.rect(SCREEN, TUME_PRUUN,(screen_x, screen_y, RUUT, RUUT))
        mängija.draw(kaamera_x, kaamera_y)
    if P_OLEK == MÄNG_POOD:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - mängija.move_timer > mängija.move_delay:
            dx = 0
            dy = 0
            if keys[pygame.K_UP]: dy = -1
            elif keys[pygame.K_DOWN]: dy = 1
            elif keys[pygame.K_LEFT]: dx = -1
            elif keys[pygame.K_RIGHT]: dx = 1
            if dx != 0 or dy != 0:
                tulemus = mängija.move(dx, dy)
                mängija.move_timer = current_time
                if tulemus == 3:
                    P_OLEK = MÄNG_SPAWN
                    MAP = spawn_map
                    mängija.set_start_pos()
                    pygame.mixer.music.load(MUUSIKA_SPAWN)
                    pygame.mixer.music.play(0)
                    praeg_laul = "forest"
        kaamera_x = (mängija.x * RUUT) - (WIDTH // 2) + (RUUT // 2)
        kaamera_y = (mängija.y * RUUT) - (HEIGHT // 2) + (RUUT // 2)
        for y, rida in enumerate(MAP):
            for x, ruut in enumerate(rida):
                screen_x = (x * RUUT) - kaamera_x
                screen_y = (y * RUUT) - kaamera_y
                if ruut == "g":
                    pygame.draw.rect(SCREEN, PRUUN,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "SS":
                    pygame.draw.rect(SCREEN, TUME_PRUUN,(screen_x, screen_y, RUUT, RUUT))
                elif ruut == "." or ruut == "S":
                    pygame.draw.rect(SCREEN, TUME_PRUUN,(screen_x, screen_y, RUUT, RUUT))
        mängija.draw(kaamera_x, kaamera_y)  
    if P_OLEK == VÕIT:
            tekst = FONT.render("Võitsid mängu", True, VALGE)
            SCREEN.blit(tekst, (WIDTH//2 - 150, HEIGHT//2 - 50))
                
    pygame.display.flip()
    KELL.tick(60)

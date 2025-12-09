import pygame
import os
import sys
import math
import random

pygame.init()
pygame.mixer.init()

# muusika ja sound effect'id
MUUSIKA_MENÜÜ = os.path.join("assets/music", "menu.mp3")
MUUSIKA_CAVE_ALG = os.path.join("assets/music", "cave_begin.mp3")
MUUSIKA_CAVE_REP = os.path.join("assets/music", "cave_rep.mp3")
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

# mängu olekud ja menüüd
MENU = "menu"
MÄNG = "mäng"
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
def loo_kaart(kõrgus, laius):
    grid = []
    x = laius // 2
    y = kõrgus // 2
    for a in range(kõrgus):
        rida = []
        for täht in range(laius):
            rida.append("W")
        grid.append(rida)
    grid[y][x] = "S"
    for i in range(500):
        suund = random.randint(1, 4)
        if suund == 1 and x > 1:
            x -= 1
        elif suund == 2  and x < laius - 2:
            x += 1
        elif suund == 3 and y > 1:
            y -= 1 
        elif suund == 4 and y < kõrgus - 2:
            y += 1
        if grid[y][x] != "S":
            grid[y][x] = "."
    grid[y][x] = "D"
    return grid

MAP = loo_kaart(16, 30)

# klassid
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
        for y, rida in enumerate(MAP):
            for x, ruut in enumerate(rida):
                if ruut == "S":
                    self.x = x
                    self.y = y
    def draw(self, kaamera_x, kaamera_y):
        screen_x = (self.x * RUUT) - kaamera_x
        screen_y = (self.y * RUUT) - kaamera_y
        SCREEN.blit(self.image, (screen_x, screen_y))
    def move(self, dx, dy):
        target_x = self.x + dx
        target_y = self.y + dy
        see = MAP[target_y][target_x]
        if see == "." or see == "S" or see == "D":
            self.x = target_x
            self.y = target_y
            if see == "D":
                return True
            if dx == 1:
                self.image = self.img_parem
            elif dx == -1:
                self.image = self.img_vasak
        return False
    
kaamera_x = 0
kaamera_y = 0
mängija = Player()
nupp = pygame.Rect(WIDTH//2 - 200, HEIGHT//2, 400, 100)
# main loop
running = True
while running:
    SCREEN.fill(MUST)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if P_OLEK == MENU and nupp.collidepoint(event.pos):
                P_OLEK = MÄNG
                pygame.mixer.music.load(MUUSIKA_CAVE_ALG)
                pygame.mixer.music.play(0)
                praeg_laul = "intro"
                mängija.move_timer = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and P_OLEK == MÄNG:
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
        pygame.draw.rect(SCREEN, SININE, nupp)
        tekst = FONT.render("Sisene koopasse", True, MUST)
        tsenter = tekst.get_rect(center=nupp.center)
        SCREEN.blit(tekst, tsenter)
    if P_OLEK == MÄNG:
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
    if P_OLEK == VÕIT:
            tekst = FONT.render("Võitsid mängu", True, VALGE)
            SCREEN.blit(tekst, (WIDTH//2 - 150, HEIGHT//2 - 50))
                
    pygame.display.flip()
    KELL.tick(60)
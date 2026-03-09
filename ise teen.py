import pygame
import sys
pygame.init()
ekraan_info = pygame.display.Info()
laius = ekraan_info.current_w
korgus = ekraan_info.current_h
ekraan = pygame.display.set_mode((laius, korgus), pygame.RESIZABLE | pygame.SCALED, vsync=1)

# Värvid
RUUT = 128
player_kiirus = 5
MUST = (0,0,0)
VALGE = (255,255,255)
PUNANE = (255,0,0)
SININE = (0,0,255)
ROHELINE = (0,255,0)
PRUUN = (120,60,15)
HALL = (128,128,128)
kell = pygame.time.Clock()
fps = 60
run = True
i = 50
kaart = [
    ["W", "W", "W", "W", "W"],
    ["W", ".", ".", ".", "W"],
    ["W", ".", "S", ".", "W"],
    ["W", ".", ".", ".", "W"],
    ["W", "W", "W", "W", "W"]
]

Olek = "spawn"



# 1. Enne tsüklit: Leia alguspunkt ja loo mängija
player_x, player_y = 0, 0
for y, rida in enumerate(kaart):
    for x, täht in enumerate(rida):
        if täht == "S":
            player_x, player_y = x * RUUT, y * RUUT

player = pygame.Rect(player_x, player_y, RUUT, RUUT)
font = pygame.font.SysFont("Arial", 80) # Font loo ka siin, mitte tsüklis

while run:
    ekraan.fill(HALL)
    
    # --- ÜKS sündmuste tsükkel kõige jaoks ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and Olek == "spawn":
            if nupp.collidepoint(event.pos):
                Olek = "mäng"

    if Olek == "spawn":
        nupp = pygame.Rect(950, 600, 600, 150)
        pygame.draw.rect(ekraan, PRUUN, nupp)
        tekst = font.render("Alusta mängu", True, MUST)
        ekraan.blit(tekst, (1050, 630))

    elif Olek == "mäng":
        # 1. Sujuv liikumine (kontrollime nuppe igas kaadris)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= player_kiirus
        if keys[pygame.K_s]: player.y += player_kiirus
        if keys[pygame.K_a]: player.x -= player_kiirus
        if keys[pygame.K_d]: player.x += player_kiirus

        # 2. Joonista kaart
        for y, rida in enumerate(kaart):
            for x, täht in enumerate(rida):
                pos = (x * RUUT, y * RUUT, RUUT, RUUT)
                if täht == "W":
                    pygame.draw.rect(ekraan, MUST, pos)
                elif täht == "." or täht == "S": # Joonistame põranda ka stardi alla
                    pygame.draw.rect(ekraan, VALGE, pos)

        # 3. Joonista mängija (ALATI, mitte ainult nupuvajutusel)
        pygame.draw.rect(ekraan, SININE, player)

    pygame.display.flip()
    kell.tick(fps)
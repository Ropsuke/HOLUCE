import os
import pygame
# EKRAAN

FPS          = 60
RUUT         = 64
PLAYER_RUUT  = 128

# TEKST

FONDI_NIMI = "arial"
FONDI_SUURUS = 60

# VÄRVID

VALGE = (255, 255, 255)
MUST  = (0, 0, 0)
HALL  = (128, 128, 128)
SININE = (0, 0, 255)
PRUUN = (139, 69, 19)
TUME_HALL = (64, 64, 64)
TUME_ROHELINE = (0, 70, 0)
TUME_PRUUN = (100, 50, 0)
TUME_TUME_PRUUN = (65, 30, 0)

# FAILIPATHID

SPRITE_ENTITIES_FOLDER = "assets/entities"
SPRITE_PILDID_FOLDER   = "assets/pictures"
SPRITE_PILDID_TEST   = "assets/pictures_test"

MUUSIKA_MENÜÜ    = os.path.join("assets/music", "menu.mp3")
MUUSIKA_CAVE_ALG = os.path.join("assets/music", "cave_begin.mp3")
MUUSIKA_CAVE_REP = os.path.join("assets/music", "cave_rep.mp3")
MUUSIKA_SPAWN    = os.path.join("assets/music", "forest.mp3")
MUUSIKA_POOD     = os.path.join("assets/music", "shop.mp3")

# MÄNGU OLEKUD

MENU        = "menu"
MÄNG_KOOBAS = "mäng"
MÄNG_SPAWN  = "spawn"
MÄNG_POOD   = "pood"
VÕIT        = "võit"

# KUHU MÄNGIJA SAAB ASTUDA

VABAD = {".", "S", "D", "g", "TT", "SS"}

# KAARTIDE VÄRVID JA PILDID

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

# KAARDI INFO DICT

KAARDI_INFO = {
    MÄNG_SPAWN: {
        "värvid": SPAWN_VÄRVID,
        "pildid": SPAWN_PILDID,
        "muusika": MUUSIKA_SPAWN,
        "laul_nimi": "forest",
        "loop": True,
    },
    MÄNG_KOOBAS: {
        "värvid": KOOBAS_VÄRVID,
        "pildid": KOOBAS_PILDID,
        "muusika": MUUSIKA_CAVE_ALG,
        "laul_nimi": "intro",
        "loop": False,
    },
    MÄNG_POOD: {
        "värvid": POOD_VÄRVID,
        "pildid": POOD_PILDID,
        "muusika": MUUSIKA_POOD,
        "laul_nimi": "shop",
        "loop": True,
    },
}
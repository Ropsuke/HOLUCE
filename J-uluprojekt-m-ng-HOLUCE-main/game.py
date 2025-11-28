import pygame
import os
import sys
import math
pygame.init()
# Ekraan
WIDTH, HEIGHT = 1000, 625
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HOLUCE Title Animation")
CLOCK = pygame.time.Clock()
FPS = 60

# Värvid
VALGE = (255, 255, 255)
MUST = (0, 0, 0)
HALL = (122, 122, 122)
PUNANE = (255, 0 , 0)
ROHELINE = (0, 255, 0)
SININE = (0, 0, 255)

# Sätted
ASSET_FOLDER = "assets/letters"
WORD = "HOLUCE"
DROP_SPEED = 12
FADE_SPEED = 10
LETTER_SPACING = -40
START_OFFSET = 150
DELAY_BETWEEN = 12
LETTER_OFFSETS = {
    'H': 0,
    'O': 0,
    'L': 0,
    'U': -8, 
    'C': -3,
    'E': 0
}

def go_fullscreen():
    global SCREEN, WIDTH, HEIGHT
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    recalc_positions()

def go_windowed():
    global SCREEN, WIDTH, HEIGHT
    WIDTH, HEIGHT = 1500, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    recalc_positions()

# Täht
letters = []
for char in WORD:
    filename = f"{char}.png"
    path = os.path.join(ASSET_FOLDER, filename)
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() // 10, img.get_height() // 10))
    letters.append(img)

class LetterSprite(pygame.sprite.Sprite):
    def __init__(self, image, target_x, target_y, start_delay):
        super().__init__()
        self.original_image = image
        self.image = image.copy()
        self.rect = self.image.get_rect(midbottom=(target_x, -START_OFFSET))
        self.alpha = 0
        self.image.set_alpha(self.alpha)
        self.target_y = target_y
        self.delay = start_delay
        self.active = False
        self.float_amplitude = 20        
        self.float_speed = 0.05          
        self.float_phase = start_delay * 0.1  
        self.base_y = target_y           
    def update(self):
        if self.delay > 0:
            self.delay -= 1
            return

        self.active = True

        if self.alpha < 255:
            self.alpha += FADE_SPEED
            if self.alpha > 255:
                self.alpha = 255
            self.image = self.original_image.copy()
            self.image.set_alpha(self.alpha)

        self.float_phase += self.float_speed
        self.rect.y = self.base_y + int(math.sin(self.float_phase) * self.float_amplitude)

sprites = pygame.sprite.Group()
for img in letters:
    sprite = LetterSprite(img, 0, 0, 0)
    sprites.add(sprite)

# Funktsioon letters ja nupud positsiooni rekalkuleerimiseks
def recalc_positions():
    total_letter_width = sum(img.get_width() for img in letters)
    total_spacing = LETTER_SPACING * (len(letters) - 1)
    total_width = total_letter_width + total_spacing
    start_x = (WIDTH - total_width) // 2

    x = start_x
    for i, sprite in enumerate(sprites.sprites()):
        offset = LETTER_OFFSETS.get(WORD[i], 0)
        sprite.rect.x = x + letters[i].get_width() // 2 + offset
        sprite.base_y = HEIGHT // 4
        x += letters[i].get_width() + LETTER_SPACING

    global Nupud
    Nupud = [(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 75)]

recalc_positions()

# Loop
is_fullscreen = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    go_fullscreen()
                else:
                    go_windowed()

    SCREEN.fill(VALGE)

    for rect in Nupud:
        pygame.draw.rect(SCREEN, PUNANE, rect)
    sprites.update()
    sprites.draw(SCREEN)

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
sys.exit()

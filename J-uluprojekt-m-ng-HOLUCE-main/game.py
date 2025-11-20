import pygame
import os
import sys
import math
pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 1500, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HOLUCE Title Animation")
CLOCK = pygame.time.Clock()
FPS = 60

# Folder containing your letter images
ASSET_FOLDER = "assets/letters"  # <-- change if needed

# Title word
WORD = "HOLUCE"

# Animation settings
DROP_SPEED = 12         # falling speed
FADE_SPEED = 10         # alpha increase speed
LETTER_SPACING = -40      # pixels between letters
START_OFFSET = 150      # how far above the screen letters begin
DELAY_BETWEEN = 12      # frames between each letter's start (wave)
LETTER_OFFSETS = {
    'H': 0,
    'O': 0,
    'L': 0,
    'U': -8,   # move U slightly right
    'C': -3,  # move C slightly left
    'E': 0
}


# --- LOAD LETTER IMAGES ---
letters = []
for char in WORD:
    filename = f"{char}.png"   # files must be H.png, O.png, L.png etc.
    path = os.path.join(ASSET_FOLDER, filename)
    img = pygame.image.load(path).convert_alpha()
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() // 10, img.get_height() // 10))
    letters.append(img)

class LetterSprite(pygame.sprite.Sprite):
    def __init__(self, image, target_x, target_y, start_delay):
        super().__init__()
        self.original_image = image
        self.image = image.copy()
        self.rect = self.image.get_rect(midbottom=(target_x, -START_OFFSET))

        # fade
        self.alpha = 0
        self.image.set_alpha(self.alpha)

        # target position
        self.target_y = target_y

        # timing
        self.delay = start_delay
        self.active = False

        # floating (up and down)
        self.float_amplitude = 20        # how far letters move up/down
        self.float_speed = 0.05          # speed of floating
        self.float_phase = start_delay * 0.1  # phase offset for each letter
        self.base_y = target_y           # the y position around which it floats

    def update(self):
        if self.delay > 0:
            self.delay -= 1
            return

        self.active = True

        # FADE IN
        if self.alpha < 255:
            self.alpha += FADE_SPEED
            if self.alpha > 255:
                self.alpha = 255
            self.image = self.original_image.copy()
            self.image.set_alpha(self.alpha)

        # FLOATING EFFECT (smooth up and down)
        self.float_phase += self.float_speed
        self.rect.y = self.base_y + int(math.sin(self.float_phase) * self.float_amplitude)


# --- CREATE SPRITES WITH CENTERING + CUSTOM OFFSETS ---
sprites = pygame.sprite.Group()

# total width of letters + spacing
total_letter_width = sum(img.get_width() for img in letters)
total_spacing = LETTER_SPACING * (len(letters) - 1)
total_width = total_letter_width + total_spacing
start_x = (WIDTH - total_width) // 2

x = start_x
for i, img in enumerate(letters):
    target_y = HEIGHT // 4

    # get custom offset if exists, else 0
    char = WORD[i]
    offset = LETTER_OFFSETS.get(char, 0)

    # position the letter
    sprite = LetterSprite(img, x + img.get_width() // 2 + offset, target_y, i * DELAY_BETWEEN)
    sprites.add(sprite)

    # move x for next letter
    x += img.get_width() + LETTER_SPACING



# --- MAIN LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    SCREEN.fill((20, 20, 20))

    sprites.update()
    sprites.draw(SCREEN)

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
sys.exit()

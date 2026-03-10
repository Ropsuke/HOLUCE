import os
import pygame
from seaded import *

class Player:
    def __init__(self):
        self.pix_x = 1.0 * RUUT
        self.pix_y = 1.0 * RUUT
        self.kiirus = 7

        # Hitbox seaded
        self.hb_w  = 44
        self.hb_h  = 32
        self.hb_ox = 10
        self.hb_oy = 96

        # Pildi laadimine
        self._laadi_pilt()

    def _laadi_pilt(self):
        pilt_path = os.path.join(SPRITE_ENTITIES_FOLDER, "player.png")
        try:
            lae = pygame.image.load(pilt_path).convert_alpha()
            skaleeritud = pygame.transform.scale(lae, (PLAYER_RUUT // 2, PLAYER_RUUT))
            self.img_parem = skaleeritud
            self.img_vasak = pygame.transform.flip(skaleeritud, True, False)
        except FileNotFoundError:
            print("Hoiatus: player.png ei leitud! Kasutan sinist kasti.")
            skaleeritud = pygame.Surface((PLAYER_RUUT // 2, PLAYER_RUUT))
            skaleeritud.fill(VÄRVID["SININE"])
            self.img_parem = skaleeritud
            self.img_vasak = skaleeritud

        self.image = self.img_parem

    def _on_vaba(self, px, py, kaart):
        vasak  = px + self.hb_ox
        parem  = px + self.hb_ox + self.hb_w
        üleval = py + self.hb_oy
        all_   = py + self.hb_oy + self.hb_h

        nurgad = [
            (vasak, üleval),
            (parem, üleval),
            (vasak, all_),
            (parem, all_),
        ]

        for nx, ny in nurgad:
            gx = int(nx // RUUT)
            gy = int(ny // RUUT)

            if gy < 0 or gy >= len(kaart) or gx < 0 or gx >= len(kaart[0]):
                return False
            if kaart[gy][gx] not in VABAD:
                return False

        return True

    def move_vaba(self, dx, dy, kaart):
        sammx = dx * self.kiirus
        sammy = dy * self.kiirus

        # X-telg
        if self._on_vaba(self.pix_x + sammx, self.pix_y, kaart):
            self.pix_x += sammx
        else:
            astme_suund = 1 if sammx > 0 else -1
            for _ in range(int(abs(sammx))):
                if self._on_vaba(self.pix_x + astme_suund, self.pix_y, kaart):
                    self.pix_x += astme_suund
                else:
                    break

        # Y-telg
        if self._on_vaba(self.pix_x, self.pix_y + sammy, kaart):
            self.pix_y += sammy
        else:
            astme_suund = 1 if sammy > 0 else -1
            for _ in range(int(abs(sammy))):
                if self._on_vaba(self.pix_x, self.pix_y + astme_suund, kaart):
                    self.pix_y += astme_suund
                else:
                    break

        # Suund
        if dx > 0:
            self.image = self.img_parem
        elif dx < 0:
            self.image = self.img_vasak

        # Portaalide kontroll
        return self._kontrolli_portaal(kaart)

    def _kontrolli_portaal(self, kaart):
        kesk_x = int((self.pix_x + self.hb_ox + self.hb_w / 2) // RUUT)
        kesk_y = int((self.pix_y + self.hb_oy + self.hb_h / 2) // RUUT)

        if 0 <= kesk_y < len(kaart) and 0 <= kesk_x < len(kaart[0]):
            ruut = kaart[kesk_y][kesk_x]
            if ruut == "D":  return 1
            if ruut == "TT": return 2
            if ruut == "SS": return 3

        return 0

    def draw(self, screen, kx, ky):
        screen.blit(self.image, (self.pix_x - kx, self.pix_y - ky))

    def draw_hitbox(self, screen, kx, ky):
        hb = pygame.Rect(
            self.pix_x + self.hb_ox - kx,
            self.pix_y + self.hb_oy - ky,
            self.hb_w, self.hb_h,
        )
        pygame.draw.rect(screen, (255, 0, 0), hb, 2)

    def set_start_pos(self, kaart):
        for y, rida in enumerate(kaart):
            for x, ruut in enumerate(rida):
                if ruut == "S":
                    self.pix_x = float(x * RUUT)
                    self.pix_y = float(y * RUUT)
                    return
        self.pix_x = float(RUUT)
        self.pix_y = float(RUUT)
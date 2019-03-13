# Based on https://github.com/fabiensanglard/DoomFirePSX/blob/master/flames.html
# and http://fabiensanglard.net/doom_fire_psx/

import random
import sys

import pygame
from pygame.locals import K_ESCAPE, QUIT


class FireEffect():
    def __init__(self, width, height, fullscreen=False):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        if fullscreen:
            pygame.display.toggle_fullscreen()

    def run(self):
        clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))
        self._init_fire()
        self._update_screen()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self._check_keyboard()
            self._update_screen()
            clock.tick(60)

    @staticmethod
    def _check_keyboard():
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            sys.exit()

    def _update_screen(self):
        self._update_fire()
        for x in range(self.width):
            for y in range(self.height):
                pixel_value = self.palette[self.fire_pixels[self.width * y + x]]
                self.screen.set_at((x, y), (pixel_value))
        pygame.display.flip()

    def _init_fire(self):
        self.palette = [
            (0x07, 0x07, 0x07),
            (0x1F, 0x07, 0x07),
            (0x2F, 0x0F, 0x07),
            (0x47, 0x0F, 0x07),
            (0x57, 0x17, 0x07),
            (0x67, 0x1F, 0x07),
            (0x77, 0x1F, 0x07),
            (0x8F, 0x27, 0x07),
            (0x9F, 0x2F, 0x07),
            (0xAF, 0x3F, 0x07),
            (0xBF, 0x47, 0x07),
            (0xC7, 0x47, 0x07),
            (0xDF, 0x4F, 0x07),
            (0xDF, 0x57, 0x07),
            (0xDF, 0x57, 0x07),
            (0xD7, 0x5F, 0x07),
            (0xD7, 0x5F, 0x07),
            (0xD7, 0x67, 0x0F),
            (0xCF, 0x6F, 0x0F),
            (0xCF, 0x77, 0x0F),
            (0xCF, 0x7F, 0x0F),
            (0xCF, 0x87, 0x17),
            (0xC7, 0x87, 0x17),
            (0xC7, 0x8F, 0x17),
            (0xC7, 0x97, 0x1F),
            (0xBF, 0x9F, 0x1F),
            (0xBF, 0x9F, 0x1F),
            (0xBF, 0xA7, 0x27),
            (0xBF, 0xA7, 0x27),
            (0xBF, 0xAF, 0x2F),
            (0xB7, 0xAF, 0x2F),
            (0xB7, 0xB7, 0x2F),
            (0xB7, 0xB7, 0x37),
            (0xCF, 0xCF, 0x6F),
            (0xDF, 0xDF, 0x9F),
            (0xEF, 0xEF, 0xC7),
            (0xFF, 0xFF, 0xFF)
        ]

        self.fire_pixels = [0 for pos in range(self.width * self.height)]
        for x in range(self.width):
            self.fire_pixels[(self.height - 1) * self.width + x] = 36

    def _update_fire(self):
        for x in range(self.width):
            for y in range(1, self.height):
                self._spread_fire(y * self.width + x)

    # vertical and horizontal deviation
    def _spread_fire(self, source_particle):
        source_pixel = self.fire_pixels[source_particle]
        if source_pixel == 0:
            self.fire_pixels[source_particle - self.width] = 0
        else:
            deviation = random.randint(0, 3)
            destination_particle = source_particle - deviation + 1
            self.fire_pixels[destination_particle - self.width] = self.fire_pixels[source_particle] - (deviation & 1)


if __name__ == "__main__":
    width = 320
    height = 200
    fullscreen = False
    game = FireEffect(width, height, fullscreen)
    game.run()

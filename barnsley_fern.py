from math import sin, cos
from random import random
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, QUIT


class BarnsleyFern():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

        self.resolution = 1
        self.stopped = False

    def start(self):
        self.screen.fill((0, 0, 0))

    def run(self):
        clock = pygame.time.Clock()

        self._draw_frame()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self._check_keyboard()
            if not self.stopped:
                self._draw_frame()
            clock.tick(30)

    def _check_keyboard(self):
        key = pygame.key.get_pressed()
        if key[K_ESCAPE] or key[K_SPACE]:
            sys.exit()

    def _draw_frame(self):
        self.screen.fill((0, 0, 0))
        self._draw_fern()
        pygame.display.flip()

    @staticmethod
    def _w_values(w_pass):
        # https://en.wikipedia.org/wiki/Barnsley_fern

        if w_pass == 1:
            return (0, 0, 0, 0.16, 0, 0)
        elif w_pass == 2:
            return (0.85, 0.04, -0.04, 0.85, 0, 1.6)
        elif w_pass == 3:
            return (0.2, -0.26, 0.23, 0.22, 0, 1.6)
        elif w_pass == 4:
            return (-0.15, 0.28, 0.26, 0.24, 0, 0.44)

    def _draw_pixel(self, x, y):
        x_correct = 150
        y_correct = 150
        scale = 50

        self.screen.set_at((int(x*scale) + x_correct, int(y*scale) + y_correct), (0, 255, 0))

    def _draw_fern(self):
        x = 0
        y = 0
        self._draw_pixel(x, y)

        for step in range(self.resolution + 1):
            chance = random()
            if chance > 0.93:
                w_pass = 4
            elif chance > 0.87:
                w_pass = 3
            elif chance > 0.1:
                w_pass = 2
            else:
                w_pass = 1

            a, b, c, d, e, f = self._w_values(w_pass)

            # f(x,y) = [ a b ] [ x ]  + [ e ]
            #            c d     y        f
            w_x = a * x + b * y
            w_y = c * x + d * y + f

            self._draw_pixel(w_x, w_y)
            x = w_x
            y = w_y

        if self.resolution < 50000:
            self.resolution += 500
        else:
            self.stopped = True


if __name__ == "__main__":
    width = 800
    height = 800
    game = BarnsleyFern(width, height)
    game.start()
    game.run()

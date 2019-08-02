import random
import sys

from grid_linebuffer import Grid

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, QUIT


class GameOfLife():
    def __init__(self, width, height, fullscreen=False):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.paused = True
        if fullscreen:
            pygame.display.toggle_fullscreen()

    def start(self):
        self.screen.fill((0, 0, 0))
        self.grid = Grid(self.width, self.height)
        self.rows_range = range(self.grid.height)
        self.cols_range = range(self.grid.width)

        # self._random_populated_cells(self.width, self.height)
        self._create_r_pentomino(63, 30)
        self._create_r_pentomino(63, 60)

    def run(self):
        clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))
        self._draw_grid()
        pygame.display.flip()

        while self.paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self._check_keyboard()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self._check_keyboard()
            self._update_grid()
            clock.tick(30)

    def _draw_grid(self):
        for y in self.rows_range:
            for x in self.cols_range:
                if self.grid.get_cell(x, y) == 1:
                    self.screen.set_at((x, y), (0, 255, 0))

    def _update_grid(self):
        self.grid.advance_generation()
        self.screen.fill((0, 0, 0))
        self._draw_grid()
        pygame.display.flip()

    def _check_keyboard(self):
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            sys.exit()
        elif key[K_SPACE]:
            self.paused = False

    def _random_populated_cells(self, grid_width, grid_height, num_cells=None):
        cells = []
        if num_cells is None:
            min_cells = grid_width + grid_height - 1
            max_cells = ((grid_width - 1) * (grid_height - 1)) // 4
            num_cells = random.randint(min_cells, max_cells)
        for index in range(num_cells):
            cells.append((random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)))
        self.grid.populate_cells(cells)

    # More patterns here: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Examples_of_patterns
    def _create_r_pentomino(self, start_x, start_y):
        cells = []
        cells.append((start_x + 1, start_y))
        cells.append((start_x + 2, start_y))
        cells.append((start_x, start_y + 1))
        cells.append((start_x + 1, start_y + 1))
        cells.append((start_x + 1, start_y + 2))
        self.grid.populate_cells(cells)


if __name__ == "__main__":
    width = 150
    height = 150
    fullscreen = False
    game = GameOfLife(width, height, fullscreen)
    game.start()
    game.run()

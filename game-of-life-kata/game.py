import pygame
from pygame.locals import *
import sys
import random

from grid import *


class GameOfLife():
    def __init__(self, width, height, fullscreen=False):
        self.screen = pygame.display.set_mode((width, height))
        self.paused = True
        if fullscreen:
            pygame.display.toggle_fullscreen()

    def start(self, grid_width, grid_height):
        self.screen.fill((0, 0, 0))
        self.grid = Grid(grid_width, grid_height)

        self._random_populated_cells(grid_width, grid_height)
        self.rows_range = range(self.grid.height)
        self.cols_range = range(self.grid.width)

    def run(self):
        clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))
        self._draw_grid()
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self._check_keyboard()
            if not self.paused:
                self._update_grid()
                clock.tick(30)

    def _draw_grid(self):
        for y in self.rows_range:
            for x in self.cols_range:
                if self.grid.get_cell(x, y) == 1:
                    self.screen.set_at((x, y), (0, 255, 0))
                    # Alternative: fill(color, (position, rect)
                    # self.screen.fill((0, 255, 0), ((x, y), (1, 1)))

    def _update_grid(self):
        self.grid.advance_generation()
        self.screen.fill((0, 0, 0))
        self._draw_grid()
        pygame.display.flip()

    def _check_keyboard(self):
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            sys.exit()
        if key[K_SPACE]:
            self.paused = not self.paused

    def _random_populated_cells(self, grid_width, grid_height, num_cells=None):
        cells = []
        if num_cells is None:
            min_cells = grid_width + grid_height - 1
            max_cells = ((grid_width-1) * (grid_height-1)) // 4
            num_cells = random.randint(min_cells, max_cells)
        for index in range(num_cells):
            cells.append((random.randint(0, grid_width-1), random.randint(0, grid_height-1)))

        self.grid.populate_cells(cells)


if __name__ == "__main__":
    width = 160
    height = 120
    game = GameOfLife(width, height)
    game.start(width, height)
    game.run()

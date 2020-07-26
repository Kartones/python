import random
import sys

import pygame
from pygame.locals import DOUBLEBUF, HWSURFACE, RESIZABLE, K_RIGHT, K_LEFT, K_ESCAPE, K_SPACE, QUIT, VIDEORESIZE


MOVEMENT_DELTA = 2


class Entity():

    def __init__(self, width, start_x, start_y, scale_x, scale_y, original_screen_width):
        self._width = width
        self._original_screen_width = original_screen_width
        self._x = start_x
        self._y = start_y
        self.rescale(scale_x, scale_y)

    def rescale(self, scale_x, scale_y):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self._move_x(0)
        self._scaled_y = int(self._y * scale_y)

    def can_move_left(self, delta):
        return self._x >= 0 + delta

    def can_move_right(self, delta):
        return self._x <= (self._original_screen_width - self._width - delta)

    def move_left(self, delta):
        self._move_x(-delta)

    def move_right(self, delta):
        self._move_x(delta)

    def _move_x(self, delta):
        self._x = self._x + delta
        self._scaled_x = int(self._x * self.scale_x)

    @property
    def x(self):
        return self._scaled_x

    @property
    def y(self):
        return self._scaled_y


class Player(Entity):
    pass


class Enemy(Entity):

    def __init__(self, width, start_x, start_y, scale_x, scale_y, original_screen_width):
        super().__init__(width, start_x, start_y, scale_x, scale_y, original_screen_width)

        # TODO: move to  constants: 0 stopped, 1 left, 2 right
        self.direction = 0

    def process_ai(self, movement_delta):
        chance = random.randint(0, 100)

        # if already moving:
        #   50% -> keeps moving
        #   10% -> stops (and might change direction)
        #   40% -> does not move
        # if stopped:
        #   30% -> changes direction to left
        #   30% -> changes direction to right

        if self.direction == 1 and self.can_move_left(movement_delta):
            if chance < 50:
                self.move_left(movement_delta)
            elif chance < 60:
                self.direction = 0
        elif self.direction == 2 and self.can_move_right(movement_delta):
            if chance < 50:
                self.move_right(movement_delta)
            elif chance < 60:
                self.direction = 0
        # also will land here if can't move further in curent direction
        else:
            if chance < 30:
                self.direction = 1
            elif chance < 60:
                self.direction = 2


class TransarcticaBattles():

    def __init__(self, width, height):
        self.stopped = True

        self.original_width = width
        self.original_height = height
        self.width = width
        self.height = height
        self._calculate_scale()
        self.screen = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)

        self.original_resources = {}
        self.resources = {}

    def setup(self):
        self.screen.fill((0, 0, 0))
        self._load_resources()

        self.enemy_train = Enemy(
            self.resources["enemy"][0].get_width(), 100, 4, self.scale_x, self.scale_y, self.original_width
        )
        self.player_train = Player(
            self.resources["player"][0].get_width(), 100, 129, self.scale_x, self.scale_y, self.original_width
        )

    def run(self):
        self.stopped = False
        clock = pygame.time.Clock()

        self._draw_frame()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict["size"], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    self.width, self.height = event.dict["size"]
                    self._calculate_scale()
                    self._resize_resources()

            self._check_keyboard()

            if not self.stopped:
                self._move_enemy()
                self._draw_frame()

            clock.tick(30)

    def _move_enemy(self):
        self.enemy_train.process_ai(MOVEMENT_DELTA)

    def _calculate_scale(self):
        self.scale_x = float(self.width) / self.original_width
        self.scale_y = float(self.height) / self.original_height

    def _check_keyboard(self):
        key = pygame.key.get_pressed()
        if key[K_ESCAPE] or key[K_SPACE]:
            self.stopped = True
            pygame.display.quit()
            sys.exit()
        elif key[K_RIGHT] and self.player_train.can_move_right(MOVEMENT_DELTA):
            self.player_train.move_right(MOVEMENT_DELTA)
        elif key[K_LEFT] and self.player_train.can_move_left(MOVEMENT_DELTA):
            self.player_train.move_left(MOVEMENT_DELTA)

    def _resize_resources(self):
        scenario = self.original_resources["scenario"][0]
        self.resources["scenario"][0] = pygame.transform.scale(
                scenario,
                (int(scenario.get_width() * self.scale_x), int(scenario.get_height() * self.scale_y))
            )

        self.enemy_train.rescale(self.scale_x, self.scale_y)
        enemy = self.original_resources["enemy"][0]
        self.resources["enemy"][0] = pygame.transform.scale(
            enemy,
            (int(enemy.get_width() * self.scale_x), int(enemy.get_height() * self.scale_y))
        )

        self.player_train.rescale(self.scale_x, self.scale_y)
        player = self.original_resources["player"][0]
        self.resources["player"][0] = pygame.transform.scale(
            player,
            (int(player.get_width() * self.scale_x), int(player.get_height() * self.scale_y))
        )

    def _draw_frame(self):
        # TODO: apply
        """
        Blitting is one of the slowest operations in any game, so you need to be careful not to blit too much onto the screen in every frame. If you have a background image, and a ball flying around the screen, then you could blit the background and then the ball in every frame, which would cover up the ball's previous position and render the new ball, but this would be pretty slow. A better solution is to blit the background onto the area that the ball previously occupied, which can be found by the ball's previous rectangle, and then blitting the ball, so that you are only blitting two small areas.
        """

        self.screen.blit(self.resources["scenario"][0], (0, 0))

        self.screen.blit(self.resources["enemy"][0], (self.enemy_train.x, self.enemy_train.y))

        self.screen.blit(self.resources["player"][0], (self.player_train.x, self.player_train.y))

        pygame.display.flip()

    def _load_resources(self):
        self.resources = {
            # TODO: Create constants, align player and enemy wagon types
            "enemy": [
                pygame.image.load("assets/bad_engine.png").convert_alpha(),
            ],
            "player": [
                pygame.image.load("assets/good_engine.png").convert_alpha(),
            ],
            # 320x164
            "scenario": [
                pygame.image.load("assets/battlefield.png").convert(),
            ]
        }

        # TODO: dedup
        self.original_resources = {
            "enemy": [
                pygame.image.load("assets/bad_engine.png").convert_alpha(),
            ],
            "player": [
                pygame.image.load("assets/good_engine.png").convert_alpha(),
            ],
            "scenario": [
                pygame.image.load("assets/battlefield.png").convert(),
            ]
        }


if __name__ == "__main__":
    width = 320
    height = 164  # 240, but no UI for now, so only battlefield
    game = TransarcticaBattles(width, height)
    game.setup()
    game.run()

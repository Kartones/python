from random import randint
import pgzrun
import pygame as pg

# These need to be global
WIDTH = 1000
HEIGHT = 600


class FlappyKirbyGame():

    # pixel movement per frame
    PIPE_SPEED = 2
    # gap between top and bottom pipes
    PIPE_GAP = 150

    PIPE_WIDTH = 64

    FLAP_VELOCITY = -5

    GRAVITY = 0.2

    NUM_PIPES = 4

    def __init__(self):
        self.player = Actor("kirby02", (100, 400))
        self.player.y_velocity = 0
        self.player.score = 0

        self.pipe_top_image = pg.image.load("images/top_pipe.png")
        self.pipe_top_image.convert()
        self.pipe_bottom_image = pg.image.load("images/bottom_pipe.png")
        self.pipe_bottom_image.convert()

        self.top_pipes = []

        self.bottom_pipes = []

        for _ in range(self.NUM_PIPES):
            self.add_new_pipe_pair()

    def create_top_pipe(self, left, height):
        rectangle = self.pipe_top_image.get_rect()
        rectangle.x = left
        rectangle.y = 0 - (rectangle.height - height)
        return rectangle

    def create_bottom_pipe(self, left, top):
        rectangle = self.pipe_bottom_image.get_rect()
        rectangle.x = left
        rectangle.y = top
        return rectangle

    def add_new_pipe_pair(self):
        screen_sector = WIDTH / self.NUM_PIPES

        left = screen_sector + screen_sector*len(self.top_pipes)
        height = randint(150, 350)
        self.top_pipes.append(self.create_top_pipe(left, height))
        self.bottom_pipes.append(
            self.create_bottom_pipe(left, height + self.PIPE_GAP)
        )

    def begin_game(self):
        self.playing = True

    def draw(self):
        global screen

        if self.playing:
            screen.clear()
            screen.blit("background", (0, 0))

            for pipe in self.top_pipes:
                screen.blit(self.pipe_top_image, pipe)
            for pipe in self.bottom_pipes:
                screen.blit(self.pipe_bottom_image, pipe)

            screen.draw.text(str(self.player.score), (20, 20), fontsize=40, color="white")

            self.player.draw()
        else:
            screen.draw.text("Game Over!", (WIDTH / 2 - 80, HEIGHT / 2 - 20), fontsize=40, color="white")

    def update(self):
        global keyboard

        if keyboard.RETURN:
            exit()

        if not self.playing:
            return

        if keyboard.SPACE and self.player.y_velocity > 0:
            self.player.y_velocity = self.FLAP_VELOCITY

        # acceleration is rate of change of velocity
        self.player.y_velocity += self.GRAVITY
        # velocity is rate of change of position
        self.player.y += self.player.y_velocity

        # player image depends on velocity
        if self.player.y_velocity > 0:
            self.player.image = "kirby02"
        else:
            self.player.image = "kirby01"

        # advance pipes
        for pipe_list in self.top_pipes, self.bottom_pipes:
            for pipe in pipe_list:
                pipe.x -= self.PIPE_SPEED
                if pipe.x < -self.PIPE_WIDTH:
                    pipe_list.remove(pipe)

        if len(self.top_pipes) < self.NUM_PIPES:
            self.player.score += 1
            self.add_new_pipe_pair()

        # game over conditions
        for pipe in self.top_pipes + self.bottom_pipes:
            if self.player.colliderect(pipe):
                self.playing = False
        if self.player.y <= 0 or self.player.y >= HEIGHT:
            self.playing = False


game = FlappyKirbyGame()


# Pygame Zero is less structured than normal pygame

def draw():
    game.draw()


def update():
    game.update()


game.begin_game()
pgzrun.go()

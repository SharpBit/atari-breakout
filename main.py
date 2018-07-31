import sys
import os
username = os.environ['LOGNAME']
new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
sys.path.insert(0, new_path)

import pygame
from pygame.locals import *
import math


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        self.color = color
        self.dimensions = [width, height]
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 1920 / 2 - 150
        self.rect.y = 800

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > 1920 - self.dimensions[0]:
            self.rect.x = 1920 - self.dimensions[0]


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, speed):
        self.color = color
        self.width = width
        self.speed = 10
        self.direction = 200  # direction of ball in degrees
        self.x = 0
        self.y = 180
        super().__init__()

        self.image = pygame.Surface((width, width))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def bounce(self, difference):
        """Bounces the ball off horizontal surfaces only."""
        self.direction = (180 - self.direction) % 360
        self.direction -= difference

    def update(self):
        # ######### #
        # This is from some stuff about ball physics about how it bounces
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        # move the image to x and y
        self.rect.x = self.x
        self.rect.y = self.y
        # ########## #
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        if self.x > 1920 - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = 1920 - self.width - 1

        if self.y > 1080:
            return True
        return False


pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (50, 150, 255)

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Atari Breakout')
pygame.mouse.set_visible(0)  # makes mouse disappear
background = pygame.Surface(screen.get_size())

blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()  # all sprites have to be in a group
all_sprites = pygame.sprite.Group()

# Initialize all sprites
paddle = Paddle(blue, 300, 30)
all_sprites.add(paddle)

ball = Ball(white, 30, 30)
balls.add(ball)
all_sprites.add(ball)

clock = pygame.time.Clock()
game_over = False
running = True

while running:
    clock.tick(60)  # 60 fps
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        paddle.update()
        game_over = ball.update()

    if game_over:
        # do game over stuff
        pass

    if pygame.sprite.spritecollide(paddle, balls, False):
        # diff lets you try to bounce the ball in a certain direction depending on
        # where on the paddle you hit the ball
        diff = (paddle.rect.x + paddle.dimensions[0] / 2) - (ball.rect.x + ball.rect.height / 2)
        # set the ball's y if the edge of the paddle
        ball.rect.y = screen.get_height() - paddle.dimensions[1] - ball.rect.height
        ball.bounce(diff)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
quit()

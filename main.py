# import sys
# import os
# username = os.environ['LOGNAME']
# new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
# sys.path.insert(0, new_path)

import pygame
from pygame.locals import *
import random
import math

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (50, 150, 255)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

# change numbers below to affect resolution of game
disp_width = 1920
disp_height = 1080

disp_x = disp_width / 1920  # creates a scale for width of game (customizable)
disp_y = disp_height / 1080  # creates a scale for height of game (customizable)

screen = pygame.display.set_mode((disp_width, disp_height), pygame.FULLSCREEN)
screen.fill(black)
pygame.display.set_caption('Atari Breakout')
clock = pygame.time.Clock()


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        self.color = color
        self.dimensions = [width, height]
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = ((1920 / 2) * disp_x) - (150 * disp_x)
        self.rect.y = (930 * disp_y)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > (1920 * disp_x) - self.dimensions[0]:
            self.rect.x = (1920 * disp_x) - self.dimensions[0]

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            return game_intro()


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, speed):
        self.color = color
        self.width = width
        self.speed = 10
        self.direction = random.randint(-50, 50)  # direction of ball in degrees
        self.x = ((1920 / 2) * disp_x)
        self.y = (700 * disp_y)
        super().__init__()

        self.image = pygame.Surface((width, width))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def bounce(self, difference):
        """Bounces the ball off horizontal surfaces only."""
        self.direction = (180 - self.direction) % 360
        self.direction -= difference

    def change_speed(self, multiplier):
        """Lets you update the speed from the main loop"""
        self.speed = self.speed * 1.5

    def update(self, lives):
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

        if self.x > (1920 * disp_x) - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = (1920 * disp_x) - self.width - 1

        if self.y > 1080 * disp_y:
            self.x = ((1920 / 2) * disp_x)
            self.y = (700 * disp_y)
            self.direction = random.randint(-50, 50)
            return lives - 1
        return lives


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x, y):
        self.color = color
        self.width = width
        self.height = height
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def QUIT():  # makes the quit button work
    pygame.quit()
    quit()


def button(msg, x, y, w, h, ic, ac, action=None):
        # msg = text, x/y = pos of button, w/h = width height, ic = color when mouse not hover, ac = color when mouse hover, action = function to execute
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.Font("assets/PressStart2P.ttf", int(35 * disp_x))
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


def game_intro():  # title screen for breakout
    intro = True
    pygame.mouse.set_visible(1)  # makes the mouse appear
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(black)
        large_text = pygame.font.Font('assets/PressStart2P.ttf', int(150 * disp_x))
        TextSurf, TextRect = text_objects('ATARI', large_text)
        TextRect.center = (((1920 / 2) * disp_x), ((300) * disp_x))
        screen.blit(TextSurf, TextRect)

        large_text = pygame.font.Font('assets/PressStart2P.ttf', int(150 * disp_x))
        TextSurf, TextRect = text_objects('BREAKOUT', large_text)
        TextRect.center = (((1920 / 2) * disp_x), ((500) * disp_x))
        screen.blit(TextSurf, TextRect)

        button('START', 560 * disp_x, 650 * disp_y, 200, 100, green, bright_green, main_game)
        button('QUIT', 1160 * disp_x, 650 * disp_y, 200, 100, red, bright_red, QUIT)

        pygame.display.update()
        clock.tick(60)


# Initialize all sprites
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

paddle = Paddle(blue, (300 * disp_x), (30 * disp_y))
all_sprites.add(paddle)

ball = Ball(white, 30 * disp_x, 30 * disp_y)
balls.add(ball)
all_sprites.add(ball)

top = 80  # y of top layer of blocks

# Five rows of blocks
for row in range(5):
    for column in range(8):
        block = Block(red, (240 * disp_x), (54 * disp_y), column * (240 * disp_x + 2), top)
        blocks.add(block)
        all_sprites.add(block)
    # Move the top of the next row down
    top += 54 * disp_y + 2


def main_game():
    lives = 10
    running = True
    while running:
        pygame.mouse.set_visible(0)  # makes mouse disappear
        clock.tick(60)  # 60 fps
        screen.fill(black)
        paddle.handle_keys()  # checks for ESC button (then goes back to main menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if lives > 0:
            paddle.update()
            lives = ball.update(lives)

        if lives == 0:
            running = False

        if pygame.sprite.spritecollide(paddle, balls, False):
            # diff lets you try to bounce the ball in a certain direction depending on
            # where on the paddle you hit the ball
            diff = (paddle.rect.x + paddle.dimensions[0] / 2) - (ball.rect.x + ball.rect.height / 2)
            # set the ball's y if the edge of the paddle
            ball.rect.y = screen.get_height() - paddle.dimensions[1] - ball.rect.height
            ball.bounce(diff)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Check for collisions between the ball and the blocks
        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

        # makes the game more fast paced with 15 blocks left
        if len(blocks) < 15:
            ball.change_speed(1.5)

        # If we actually hit a block, bounce the ball
        if len(deadblocks) > 0:
            ball.bounce(0)

            # Game ends if all the blocks are gone
            if len(blocks) == 0:
                running = False

    pygame.quit()
    quit()


game_intro()

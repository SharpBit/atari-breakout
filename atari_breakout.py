import sys
import os
username = os.environ['LOGNAME']
new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
sys.path.insert(0, new_path)

import pygame
from pygame.locals import *

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode((1920, 1080))
screen.fill(black)
pygame.display.set_caption('Atari Breakout')
clock = pygame.time.Clock()
running = True


class Paddle:

    def __init__(self, screen, color, width=300, height=30):
        self.screen = screen
        self.color = color
        self.rect = pygame.rect.Rect((1920 / 2 - 150, 800, width, height))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                key = event.key
                if key == K_LEFT:
                    self.rect.move_ip(-10, 0)
                elif key == K_RIGHT:
                    self.rect.move_ip(10, 0)
                elif key == K_ESCAPE:
                    pygame.quit()
                    exit()

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    paddle = Paddle(screen, white)
    paddle.draw()
    paddle.handle_keys()
    pygame.display.update()

    clock.tick(60)



import sys
import os
username = os.environ['LOGNAME']
new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
sys.path.insert(0, new_path)

import pygame
from pygame.locals import *

pygame.init()
width = 1920
height = 1080

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode((width, height))
screen.fill(black)
pygame.display.set_caption('Atari Breakout')
clock = pygame.time.Clock()

while True:
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()
    paddle = pygame.draw.rect(screen, white, [width / 2, 800, 300, 30])
    pygame.display.flip()

    clock.tick(60)

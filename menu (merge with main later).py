#import sys
#import os
#username = os.environ['LOGNAME']
#new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
#sys.path.insert(0, new_path)
import pygame
from pygame.locals import *

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

disp_x = 1366/1920
disp_y = 768/1920

screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
screen.fill(black)
pygame.display.set_caption('Atari Breakout')
clock = pygame.time.Clock()

pygame.display.toggle_fullscreen()

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(black)
        largeText = pygame.font.Font('PressStart2P.ttf',150)
        TextSurf, TextRect = text_objects('ATARI', largeText)
        TextRect.center = ((1920/2),(300))
        screen.blit(TextSurf, TextRect)

        largeText = pygame.font.Font('PressStart2P.ttf',150)
        TextSurf, TextRect = text_objects('BREAKOUT', largeText)
        TextRect.center = ((1920/2),(500))
        screen.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        print(mouse)

        if 560+200 > mouse[0] > 560 and 650+100 > mouse[1] > 650:
            pygame.draw.rect(screen, bright_green, (560,650,200,100))
            pygame.draw.rect(screen, red, (1160,650,200,100))

        elif 1160+200 > mouse[0] > 1160 and 650+100 > mouse[1] > 650:
            pygame.draw.rect(screen, green, (560,650,200,100))
            pygame.draw.rect(screen, bright_red, (1160,650,200,100))

        else:
            pygame.draw.rect(screen, green, (560,650,200,100))
            pygame.draw.rect(screen, red, (1160,650,200,100))

        buttonText = pygame.font.Font('PressStart2P.ttf',35)
        TextSurf, TextRect = text_objects('START', buttonText)
        TextRect.center = ((660),(700))
        screen.blit(TextSurf, TextRect)

        buttonText = pygame.font.Font('PressStart2P.ttf',35)
        TextSurf, TextRect = text_objects('QUIT', buttonText)
        TextRect.center = ((1260),(700))
        screen.blit(TextSurf, TextRect)
        
        pygame.display.update()
        clock.tick(60)

game_intro()

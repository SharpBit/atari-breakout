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

disp_x = 1280/1920
disp_y = 720/1080

screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
screen.fill(black)
pygame.display.set_caption('Atari Breakout')
clock = pygame.time.Clock()

pygame.display.toggle_fullscreen()

def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()

def START():
	return

def QUIT():
	pygame.quit()
	quit()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    small_text = pygame.font.Font("PressStart2P.ttf",int(35*disp_x))
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(text_surf, text_rect)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(black)
        large_text = pygame.font.Font('PressStart2P.ttf',int(150*disp_x))
        TextSurf, TextRect = text_objects('ATARI', large_text)
        TextRect.center = (((1920/2)*disp_x),((300)*disp_x))
        screen.blit(TextSurf, TextRect)

        large_text = pygame.font.Font('PressStart2P.ttf',int(150*disp_x))
        TextSurf, TextRect = text_objects('BREAKOUT', large_text)
        TextRect.center = (((1920/2)*disp_x),((500)*disp_x))
        screen.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        button('START', 560*disp_x, 650*disp_y, 200, 100, green, bright_green, main_game)
        button('QUIT', 1160*disp_x,650*disp_y,200,100, red, bright_red, QUIT)

        pygame.display.update()
        clock.tick(60)

game_intro()


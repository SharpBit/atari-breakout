# import sys
# import os
# username = os.environ['LOGNAME']
# new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
# sys.path.insert(0, new_path)

import math
import pygame
import random
import time

from screeninfo import get_monitors

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (50, 150, 255)
dark_blue = (40, 120, 215)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
dim_white = (200, 200, 200)

res = str(get_monitors()[0])
print(res)

disp_width = int(res[8:12])
disp_height = int(res[13:17]) if disp_width >= 1920 else int(res[13:16])

disp_x = disp_width / 1920  # creates a scale for width of game (customizable)
disp_y = disp_height / 1080  # creates a scale for height of game (customizable)

screen = pygame.display.set_mode((disp_width, disp_height), pygame.FULLSCREEN)
screen.fill(black)
pygame.display.set_caption('Atari Breakout')
clock = pygame.time.Clock()

sound = True
music = True


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
        self.y = (900 * disp_y)
        super().__init__()

        self.image = pygame.Surface((width, width))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def bounce(self, difference):
        """Bounces the ball off horizontal surfaces only."""
        self.direction = (180 - self.direction) % 360
        self.direction -= difference

    def set_speed(self, speed):
        self.speed = speed

    def change_speed(self, multiplier):
        """Lets you update the speed from the main loop"""
        self.speed *= multiplier

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


def text_objects(text, font):  # renders text
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def text_box(msg, x, y, size=35):  # makes a text box
    small_text = pygame.font.Font("assets/PressStart2P.ttf", int(size * disp_x))
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x), (y))
    screen.blit(text_surf, text_rect)


def QUIT():  # makes the quit button work
    pygame.quit()
    quit()


def button(msg, x, y, w, h, ic, ac, action=None): #creates a button
    # msg = text, x/y = pos of button, w/h = width height, ic = color when mouse not hover, ac = color when mouse hover, action = function to execute
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action:
        	if sound: # triggers sound effect
	        	pygame.mixer.music.load('assets/button_click.mp3')
	        	pygame.mixer.music.play(0)
	        action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.Font('assets/PressStart2P.ttf', int(50 * disp_x))
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


def icon(img, x, y, w, h, ic, ac, action=None):  # loads the icon/button
    # x/y = pos of button, w/h = width height, ic = color when mouse not hover, ac = color when mouse hover, action = function to execute
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, white, (x, y, w, h), 10)
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action:
        	action()
        	if sound: # triggers sound effect
	        	pygame.mixer.music.load('assets/button_click.mp3')
	        	pygame.mixer.music.play(0)
    else:
        pygame.draw.rect(screen, dim_white, (x, y, w, h), 10)
        pygame.draw.rect(screen, ic, (x, y, w, h))

    # draws image into the surface
    screen.blit(img, (x, y))


def s_on():
    global sound
    sound = False

def s_off():  # music config
    global sound
    sound = True

def m_on():
    global music
    music = False

def m_off():  # sound config
    global music
    music = True


def options():  # pops up the resolution options
    oprunning = True
    while oprunning:
        clock.tick(60)
        screen.fill(black)
        paddle.handle_keys()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        soundImg = pygame.image.load('assets/sound.png')
        soundImg = pygame.transform.scale(soundImg, (int(400 * disp_x), int(400 * disp_x)))

        musicImg = pygame.image.load('assets/music.png')
        musicImg = pygame.transform.scale(musicImg, (int(400 * disp_x), int(400 * disp_x)))

        nsoundImg = pygame.image.load('assets/sound_mute.png')
        nsoundImg = pygame.transform.scale(nsoundImg, (int(400 * disp_x), int(400 * disp_x)))  

        nmusicImg = pygame.image.load('assets/music_mute.png')
        nmusicImg = pygame.transform.scale(nmusicImg, (int(400 * disp_x), int(400 * disp_x)))

        s_ind = 'On' if sound else 'Off'
        m_ind = 'On' if music else 'Off'

        icon(nsoundImg, (1400 * disp_x), (((1080 / 4) - 200) * disp_y), 400 * disp_x, 400 * disp_y, dark_blue, blue, s_on)
        icon(soundImg, (925 * disp_x), (((1080 / 4) - 200)* disp_y), 400 * disp_x, 400 * disp_y, dark_blue, blue, s_off)
        icon(nmusicImg, (1400 * disp_x), (((1080 / 4) + 275) * disp_y), 400 * disp_x, 400 * disp_y, dark_blue, blue, m_on)
        icon(musicImg, (925 * disp_x), (((1080 / 4) + 275) * disp_y), 400 * disp_x, 400 * disp_y, dark_blue, blue, m_off)

        text_box('Sound : ' + s_ind, 400 * disp_x, 500 * disp_y, 60)
        text_box('Music : ' + m_ind, 400 * disp_x, 600 * disp_y, 60)

        button('X', 25 * disp_x, 25 * disp_y, 100 * disp_x, 100 * disp_y, red, bright_red, game_intro)  # button is slow rn, so use esc
        text_box('Press ESC or click X to leave this menu', 700 * disp_x, 1050 *disp_y)
        pygame.display.flip()  # allows options windows to actually stay


def game_intro():  # title screen for breakout
    gearImg = pygame.image.load('assets/gear.png')
    gearImg = pygame.transform.scale(gearImg, (int(100 * disp_x), int(100 * disp_y)))
    intro = True
    pygame.mouse.set_visible(1)  # makes the mouse appear
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # title of the game
        screen.fill(black)
        large_text = pygame.font.Font('assets/PressStart2P.ttf', int(150 * disp_x))
        TextSurf, TextRect = text_objects('ATARI', large_text)
        TextRect.center = (((1920 / 2) * disp_x), ((300) * disp_x))
        screen.blit(TextSurf, TextRect)

        large_text = pygame.font.Font('assets/PressStart2P.ttf', int(150 * disp_x))
        TextSurf, TextRect = text_objects('BREAKOUT', large_text)
        TextRect.center = (((1920 / 2) * disp_x), ((500) * disp_x))
        screen.blit(TextSurf, TextRect)

        # start/quit buttons
        button('START', 580 * disp_x, 650 * disp_y, 300 * disp_x, 150 * disp_y, green, bright_green, main_game)
        button('QUIT', 1040 * disp_x, 650 * disp_y, 300 * disp_x, 150 * disp_y, red, bright_red, QUIT)

        # options gear button
        icon(gearImg, 25 * disp_x, 25 * disp_y, 100 * disp_x, 100 * disp_y, dim_white, white, options)

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


def setup_blocks():
    global disp_y
    top = 80  # y of top layer of blocks
    # Five rows of blocks
    for row in range(5):
        for column in range(8):
            block = Block(red, (240 * disp_x), (54 * disp_y), column * (240 * disp_x + 2), top)
            blocks.add(block)
            all_sprites.add(block)
        # Move the top of the next row down
        top += 54 * disp_y + 2


def main_game(level=1):
    running = True
    sped_up = False
    lives = 10
    screen.fill(black)
    setup_blocks()
    text_box('LIVES: ' + str(lives), (175 * disp_x), (40 * disp_x))
    text_box('LEVEL ' + str(level), (disp_width - (145 * disp_x)), (40 * disp_x))
    text_box('LEVEL ' + str(level), 1000 * disp_x, 500 * disp_y, 150)
    pygame.display.flip()
    time.sleep(3)
    ball.set_speed(10)
    if level == 1:
        pass
    elif level == 2:
        ball.set_speed(12)
    elif level == 3:
        ball.set_speed(14)
    else:
        running = False  # only up to level 3 for now
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

        text_box('LIVES: ' + str(lives), (175 * disp_x), (40 * disp_x))
        text_box('LEVEL ' + str(level), (disp_width - (145 * disp_x)), (40 * disp_x))

        if pygame.sprite.spritecollide(paddle, balls, False):
            # diff lets you try to bounce the ball in a certain direction depending on
            # where on the paddle you hit the ball
            diff = (paddle.rect.x + paddle.dimensions[0] / 2) - (ball.rect.x + ball.rect.height / 2)
            # set the ball's y if the edge of the paddle
            ball.rect.y = screen.get_height() - paddle.dimensions[1] - ball.rect.height
            ball.bounce(diff)
            if sound:
            	pygame.mixer.music.load('assets/paddle_sound.mp3')
            	pygame.mixer.music.play(0)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Check for collisions between the ball and the blocks
        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

        # makes the game more fast paced with 15 blocks left
        if len(blocks) < 15 and not sped_up:
            ball.change_speed(1.5)
            sped_up = True

        # If we actually hit a block, bounce the ball
        if len(deadblocks) > 0:
            ball.bounce(0)
            pygame.mixer.music.load('assets/brick_break.mp3')
            pygame.mixer.music.play(0)

            # Game ends if all the blocks are gone
            if len(blocks) == 0:
                if level == 3:
                    running = False
                # resets ball position
                ball.direction = random.randint(-50, 50)
                ball.x = ((1920 / 2) * disp_x)
                ball.y = (900 * disp_y)
                # loads the next level (faster ball speed)
                main_game(level + 1)

    pygame.quit()
    quit()


game_intro()

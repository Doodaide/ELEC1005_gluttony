# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018
@author: zou
"""
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 25, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def small_message_display(text, x, y, color=white):
    large_text = pygame.font.SysFont('comicsansms', 20)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None, parameter2=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter, parameter2)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)


snakebackground = {'green': pygame.image.load('images/snakeicongreen.png'),
                    'blue': pygame.image.load('images/snakeiconblue.png'),
                    'red': pygame.image.load('images/snakeiconred.png'),
                    'purple': pygame.image.load('images/snakeiconpurple.png'),
                    'orange': pygame.image.load('images/snakeiconorange.png'),
                    'yellow': pygame.image.load('images/snakeiconyellow.png')}

def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        screen.blit(snakebackground['green'], (game.settings.width * 5, game.settings.height / 3))
        
        message_display('Snake Game', 350, game.settings.height * 6, white)

        button('Go!', 230, 240, 80, 40, green, bright_green, game_loop_easy, 'human', 'green')
        button('Quit', 390, 240, 80, 40, red, bright_red, quitgame)

        #settings interface link
        button('Settings', 310, 300, 80, 40, yellow, bright_yellow, settings_interface,'human', 'green')

        pygame.display.update()
        pygame.time.Clock().tick(15)
        
def settings_interface(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        
        pygame.display.set_mode((game.settings.width * 25, game.settings.height * 15)).fill(white)
        screen.fill(black)

        #Snake icon to change colour
        button('', 150, 40, 350, 70, black, black, color_interface)
        screen.blit(snakebackground[color], (game.settings.width * 5, game.settings.height / 3))


        message_display('Customise game', 350, game.settings.height * 6, white)
        small_message_display('*click me*', 155, 75, white)
        
        #Customise Game Modes
        button('Over and Under', 180, 200, 100, 40, green, green, game_loop_over_and_under, 'human', color)
        button('No Boundaries', 300, 200, 100, 40, green, green, game_loop_no_boundaries, 'human', color)
        button('Progressive', 420, 200, 100, 40, green, green, game_loop_progressive, 'human', color)

        button('Easy', 180, 260, 100, 40, green, green, game_loop_easy, 'human', color)
        button('Medium', 300, 260, 100, 40, green, green, game_loop_medium, 'human', color)
        button('Hard', 420, 260, 100, 40, green, green, game_loop_hard, 'human', color)

        button('Exit', 300, 340, 100, 30, red, red, initial_interface)

        pygame.display.update()
        pygame.time.Clock().tick(20)

def color_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        
        message_display('Choose Your Snake', 350, game.settings.height * 2, white)

        #Colour interface
        button('Blue:', 60, 120, 80, 40, blue, bright_blue, settings_interface, 'player', 'blue')
        small_message_display('*insert image of blue*', 240, 140, white)

        button('Red:', 60, 180, 80, 40, blue, bright_blue, settings_interface, 'player', 'red')
        small_message_display('*insert image of red*', 240, 200, white)

        button('Yellow:', 60, 240, 80, 40, blue, bright_blue, settings_interface, 'player', 'yellow')
        small_message_display('*insert image of red*', 240, 260, white)

        button('Green:', 60, 300, 80, 40, blue, bright_blue, settings_interface, 'player', 'green')

        # button('Option 5:', 340, 120, 80, 40, blue, bright_blue, settings_interface)
        # button('Option 6:', 340, 180, 80, 40, blue, bright_blue, settings_interface)
        # button('Option 7:', 340, 240, 80, 40, blue, bright_blue, settings_interface)

        pygame.display.update()
        pygame.time.Clock().tick(15)

def game_loop_over_and_under(player, color, fps=10): #WONT DIE FROM HITTING SELF
    game.restart_game(color)
    while not game.game_end_over_and_under():
        screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
        pygame.event.pump()
        move = human_move()
        fps = 10
        game.do_move_normal(move)
        screen.fill(black)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)
    
    crash()

def game_loop_no_boundaries(player, color, fps=10): #CAN CROSS OVER WALLS
    game.restart_game(color)
    while not game.game_end():
        screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
        pygame.event.pump()
        move = human_move()
        fps = 10
        game.do_move_no_boundaries(move)
        screen.fill(black)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

def game_loop_progressive(player, color, fps=10):
    game.restart_game(color)
    i = 0
    while not game.game_end():
        screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
        pygame.event.pump()
        move = human_move()
        fps = 10 + i
        game.do_move_normal(move)
        screen.fill(black)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)
        i += 0.02

    crash()


def game_loop_easy(player, color, fps=10):
    game.restart_game(color)
    while not game.game_end():
        screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
        pygame.event.pump()
        move = human_move()
        fps = 5
        game.do_move_normal(move)
        screen.fill(black)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

def game_loop_medium(player, color, fps=10):
    game.restart_game(color)
    while not game.game_end():
        screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
        pygame.event.pump()
        move = human_move()
        fps = 10
        game.do_move_normal(move)
        screen.fill(black)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

def game_loop_hard(player, color, fps=10):
    game.restart_game(color)
    while not game.game_end():
        screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
        pygame.event.pump()
        move = human_move()
        fps = 15
        game.do_move_normal(move)
        screen.fill(black)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move

if __name__ == "__main__":
    initial_interface()

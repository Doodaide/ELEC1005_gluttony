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
from game import Snake

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

game = Game(Snake('green'))
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 25, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')

# Renders text 
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Displays a text message in comic sans size 50 (large text)
# centres text (probably)
def message_display(text, x, y, color=white):
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
                    'yellow': pygame.image.load('images/snakeiconyellow.png'),
                    'pink': pygame.image.load('images/snakeiconpink.png')}


# Sets up the initial interface with the customization buttons, skin selection, etc. 
def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        question = pygame.image.load('images/help.png')

        screen.fill(black)
        screen.blit(snakebackground['green'], (game.settings.width * 5, game.settings.height / 3))
        
        message_display('Snake Game', 350, game.settings.height * 6, white)

        button('Go!', 230, 240, 80, 40, green, bright_green, game_loop_easy, 'human', 'green')
        button('Quit', 390, 240, 80, 40, red, bright_red, quitgame)

        #settings interface link
        button('Settings', 310, 300, 80, 40, yellow, bright_yellow, settings_interface,'human', 'green')
        
        button('', 0,0,80,40, black, black, help_interface, 'human', 'green')
        small_message_display('Help', 25, 20, white)
        questionn = pygame.transform.scale(question, (20,20))
        screen.blit(questionn, (45,10))

        pygame.display.update()
        pygame.time.Clock().tick(15)

def settings_interface(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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

        #Green Snake
        button('', 120,120,200,60,black,black, settings_interface, 'player', 'green')
        snakegreen = pygame.transform.scale(snakebackground['green'], (200,50))
        screen.blit(snakegreen, (game.settings.width * 4, game.settings.height * 4))

        #Blue Snake
        button('', 120,180,200,60,black,black, settings_interface, 'player', 'blue')
        snakeblue = pygame.transform.scale(snakebackground['blue'], (200,50))
        screen.blit(snakeblue, (game.settings.width * 4, game.settings.height * 6))

        #Red Snake
        button('', 120,240,200,60,black,black, settings_interface, 'player', 'red')
        snakered = pygame.transform.scale(snakebackground['red'], (200,50))
        screen.blit(snakered, (game.settings.width * 4, game.settings.height * 8))

        #Yellow Snake
        button('', 120,300,200,60,black,black, settings_interface, 'player', 'yellow')
        snakeyellow = pygame.transform.scale(snakebackground['yellow'], (200,50))
        screen.blit(snakeyellow, (game.settings.width * 4, game.settings.height * 10))

        #Purple Snake
        button('', 380,120,200,60,black,black, settings_interface, 'player', 'purple')
        snakepurple = pygame.transform.scale(snakebackground['purple'], (200,50))
        screen.blit(snakepurple, (game.settings.width * 13, game.settings.height * 4))

        #Pink Snake
        button('', 380,180,200,60,black,black, settings_interface, 'player', 'pink')
        snakepink = pygame.transform.scale(snakebackground['pink'], (200,50))
        screen.blit(snakepink, (game.settings.width * 13, game.settings.height * 6))

        #Orange Snake
        button('', 380,240,200,60,black,black, settings_interface, 'player', 'orange')
        snakeorange = pygame.transform.scale(snakebackground['orange'], (200,50))
        screen.blit(snakeorange, (game.settings.width * 13, game.settings.height * 8))

        pygame.display.update()
        pygame.time.Clock().tick(15)
        
        
# all the introductions        
def help_interface(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        message_display('introduction of the game', 350, game.settings.height * 2, white)
        small_message_display('Welcome to Gluttony!', 350, game.settings.height * 3, white)
        small_message_display('Control an ever-hungry ever-growing snake and eat strawberries to get bigger', 350,
                              game.settings.height * 4, white)
        small_message_display('Use (wasd) or the arrow keys to navigate the screen', 350, game.settings.height * 5,
                              white)
        small_message_display('But beware, hitting yourself will leave devastating effects', 350,
                              game.settings.height * 6, white)

        button('Over and Under', 180, 200, 100, 40, green, green, introduction_of_over_and_under, 'human', color)
        button('No Boundaries', 300, 200, 100, 40, green, green, introduction_of_no_boundaries, 'human', color)
        button('Progressive', 420, 200, 100, 40, green, green, introduction_of_progressive, 'human', color)

        button('Easy', 180, 260, 100, 40, green, green, introduction_of_easy, 'human', color)
        button('Medium', 300, 260, 100, 40, green, green, introduction_of_medium, 'human', color)
        button('Hard', 420, 260, 100, 40, green, green, introduction_of_hard, 'human', color)

        button('Exit', 300, 340, 100, 30, red, red, initial_interface)

        pygame.display.update()
        pygame.time.Clock().tick(20)

def introduction_of_over_and_under(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display('introduction of Over and Under', 350, game.settings.height * 2, white)

        small_message_display(' If you hit yourself, you will pass over/under instead of immediately dying', 350,
                              game.settings.height * 8, white)

        button("Exit", 620, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 300, 340, 100, 30, green, bright_green, game_loop_over_and_under, 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)

def introduction_of_no_boundaries(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display('introduction of No boundaries', 350, game.settings.height * 2, white)

        small_message_display('The boundaries of the arena connect to each other.', 350, game.settings.height * 6,
                              white)
        small_message_display('Thus, passing through one side brings you out the other.', 350,
                              game.settings.height * 8, white)

        button("Exit", 620, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 300, 340, 100, 30, green, bright_green, game_loop_no_boundaries, 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)

def introduction_of_progressive(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display('introduction of Progressive', 350, game.settings.height * 2, white)

        small_message_display('The speed of the snake will slowly increase as the game continues.', 350, game.settings.height * 6,
                              white)
        small_message_display('While the beginning may seem easy, watch for the end', 350,
                              game.settings.height * 8, white)

        button("Exit", 620, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 300, 340, 100, 30, green, bright_green, game_loop_progressive, 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)


def introduction_of_easy(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display('introduction of Easy', 350, game.settings.height * 2, white)
        small_message_display('For a nice, slow introduction to the game', 350, game.settings.height * 8, white)


        button("Exit", 620, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 300, 340, 100, 30, green,bright_green, game_loop_easy, 'human', color)


        pygame.display.update()
        pygame.time.Clock().tick(20)

def introduction_of_medium(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display('introduction of Medium', 350, game.settings.height * 2, white)

        small_message_display('For the experienced players looking for a moderately paced game', 350,
                              game.settings.height * 8, white)

        button("Exit", 620, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 300, 340, 100, 30, green,bright_green, game_loop_medium, 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)

def introduction_of_hard(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display('introduction of Hard', 350, game.settings.height * 2, white)

        small_message_display('Only for seasoned experts', 350, game.settings.height * 8, white)

        button("Exit", 620, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 300, 340, 100, 30, green,bright_green, game_loop_hard, 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)

# Gamemodes: 
# Over and under - don't die from hitting yourself
def game_loop_over_and_under(player, color, fps=10): 
    
    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    while not gamee.game_end_over_and_under():
        pygame.event.pump()
        move = human_move()
        fps = 10
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)
    
    crash()

# No boundaries - CAN CROSS OVER WALLS
def game_loop_no_boundaries(player, color, fps=10): 
    
    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake
    
    gamee.restart_game()
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 10
        gamee.do_move_no_boundaries(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

# Progressive difficulty - increases difficulty as time increments
def game_loop_progressive(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    i = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 10 + i
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)
        i += 0.02

    crash()

# Easy difficulty - slow snake
def game_loop_easy(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 5
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

# Medium difficulty - faster snake
def game_loop_medium(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 10
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

# Hard difficulty - fastest snake
def game_loop_hard(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 15
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        pygame.display.flip()
        fpsClock.tick(fps)

    crash()

# returns the corresponding move detected by human input
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
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018
@author: zou
"""
from cgitb import text
from email import message
#from turtle import screensize #Pretty sure this causes problems as I need tkinter for it to work
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
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')

leaderboard = []

file_dictionary = {'green': '_g',
                    'red': '_r',
                    'blue': '_b',
                    'yellow': '_y',
                    'purple': '_lp',
                    'orange': '_o',
                    'pink': '_p'}

# Renders text 
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Displays a text message in default comic sans size 50 (large text)
# centres text (probably)
# Added new parameter to make fonts fit properly
def message_display(text, x, y, color=white, size=50):
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

def small_message_display(text, x, y, color=white, size = 20):
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

# Added a text size parameter for button function. Ensures the whole message fits
def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None, parameter2=None, parameter3=None, text_size = 20):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h), border_radius=8)
        if click and click[0] == 1 and action != None:
            if parameter3 != None:
                action(parameter, parameter2, parameter3)
            elif parameter != None:
                action(parameter, parameter2)
            else:
                action()

    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h), border_radius=8)

    smallText = pygame.font.SysFont('comicsansms', text_size)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)

def quitgame():
    pygame.quit()
    quit()

def crash(score, color):
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white, 50)
    time.sleep(1)

    #Sorting algorithm to keep top snakes at front of list
    global leaderboard
    leaderboard.append([score, color])
    leaderboard.sort(key=lambda x:x[0])
    leaderboard.reverse()
    print(leaderboard)


snakebackground = {'green': pygame.image.load('images/snakeicongreen.png'),
                    'blue': pygame.image.load('images/snakeiconblue.png'),
                    'red': pygame.image.load('images/snakeiconred.png'),
                    'purple': pygame.image.load('images/snakeiconpurple.png'),
                    'orange': pygame.image.load('images/snakeiconorange.png'),
                    'yellow': pygame.image.load('images/snakeiconyellow.png'),
                    'pink': pygame.image.load('images/snakeiconpink.png')}

medals = [pygame.image.load('images/goldmedal.bmp'), pygame.image.load('images/silvermedal.bmp'), pygame.image.load('images/bronzemedal.bmp')]

# Sets up the initial interface with the customization buttons, skin selection, etc. 
def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        question = pygame.image.load('images/help.png')

        screen.fill(black)
        screen.blit(snakebackground['green'], (game.settings.width * 1.5, game.settings.height / 3))
        
        message_display('Snake Game', game.settings.width * 7.5, game.settings.height * 6, white, 50)

        button('Go!', game.settings.width * 7.5 - 120, 240, 80, 40, green, bright_green, game_loop_easy, 'human', 'green')
        button('Quit', game.settings.width * 7.5 + 40, 240, 80, 40, red, bright_red, quitgame)

        #settings interface link
        button('Settings', game.settings.width * 7.5 - 40, 300, 80, 40, yellow, bright_yellow, settings_interface,'human', 'green')
        
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
        button('', 100, 40, 350, 70, black, black, color_interface)
        screen.blit(snakebackground[color], (game.settings.width * 1.5, game.settings.height / 3))


        message_display('Customise game', game.settings.width * 7.5, game.settings.height * 6, white, 50)
        small_message_display('*click me*', 67, 80, white)
        
        widthvar = game.settings.width * 7.5

        #Customise Game Modes
        button('Over and Under', widthvar - 170, 200, 100, 40, green, green, game_loop_over_and_under, 'human', color, 13)
        button('No Boundaries', widthvar - 50, 200, 100, 40, green, green, game_loop_no_boundaries, 'human', color, 13)
        button('Progressive', widthvar + 70, 200, 100, 40, green, green, game_loop_progressive, 'human', color, 13)

        button('Easy', widthvar - 170, 260, 100, 40, green, green, game_loop_easy, 'human', color)
        button('Medium', widthvar - 50, 260, 100, 40, green, green, game_loop_medium, 'human', color)
        button('Hard', widthvar + 70, 260, 100, 40, green, green, game_loop_hard, 'human', color)

        button('Exit', widthvar - 50, 340, 100, 30, red, red, initial_interface)
        button('leaderboard', 320, 340, 100, 30, red, red, leaderboard_ui)


        pygame.display.update()
        pygame.time.Clock().tick(20)

def color_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        
        message_display('Choose Your Snake', game.settings.width * 7.5, game.settings.height * 2, white, 50)

        widthvar = game.settings.width * 7.5

        #Colour interface

        #Green Snake
        button('', 80,120,180,60,black,black, settings_interface, 'player', 'green')
        snakegreen = pygame.transform.scale(snakebackground['green'], (200,50))
        screen.blit(snakegreen, (widthvar - 200, game.settings.height * 4))

        #Blue Snake
        button('', 80,180,180,60,black,black, settings_interface, 'player', 'blue')
        snakeblue = pygame.transform.scale(snakebackground['blue'], (200,50))
        screen.blit(snakeblue, (widthvar - 200, game.settings.height * 6))

        #Red Snake
        button('', 80,240,180,60,black,black, settings_interface, 'player', 'red')
        snakered = pygame.transform.scale(snakebackground['red'], (200,50))
        screen.blit(snakered, (widthvar - 200, game.settings.height * 8))

        #Yellow Snake
        button('', 80,300,180,60,black,black, settings_interface, 'player', 'yellow')
        snakeyellow = pygame.transform.scale(snakebackground['yellow'], (200,50))
        screen.blit(snakeyellow, (widthvar - 200, game.settings.height * 10))

        #Purple Snake
        button('', 300,120,180,60,black,black, settings_interface, 'player', 'purple')
        snakepurple = pygame.transform.scale(snakebackground['purple'], (200,50))
        screen.blit(snakepurple, (game.settings.width * 8, game.settings.height * 4))

        #Pink Snake
        button('', 300,180,180,60,black,black, settings_interface, 'player', 'pink')
        snakepink = pygame.transform.scale(snakebackground['pink'], (200,50))
        screen.blit(snakepink, (game.settings.width * 8, game.settings.height * 6))

        #Orange Snake
        button('', 300,240,180,60,black,black, settings_interface, 'player', 'orange')
        snakeorange = pygame.transform.scale(snakebackground['orange'], (200,50))
        screen.blit(snakeorange, (game.settings.width * 8, game.settings.height * 8))

        pygame.display.update()
        pygame.time.Clock().tick(15)

def leaderboard_ui():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #initialise static screen
        screen.fill(black)
        message_display('Highscores', game.settings.width * 7.5, game.settings.height * 2, white, 50)
        button('Exit', game.settings.width * 7.5 - 50, 340, 100, 30, red, red, initial_interface)

        #state variables
        head = pygame.image.load('skin/head_left_g.bmp')
        tail = pygame.image.load('skin/tail_left_g.bmp')
        body = pygame.image.load('skin/body_g.bmp')
        snakehead = pygame.transform.scale(head, (20,20))
        snaketail = pygame.transform.scale(tail, (20,20))
        snakebody = pygame.transform.scale(body, (20,20))

        widthvar = game.settings.width * 7.5

        for i in range(0, len(leaderboard)):
            if i > 5:
                break

            #Retrieve the colouring of the recently played snake
            head = pygame.image.load('skin/head_left' + file_dictionary[leaderboard[i][1]] + '.bmp')
            tail = pygame.image.load('skin/tail_left' + file_dictionary[leaderboard[i][1]] + '.bmp')
            body = pygame.image.load('skin/body' + file_dictionary[leaderboard[i][1]] + '.bmp')
            snakehead = pygame.transform.scale(head, (20,20))
            snaketail = pygame.transform.scale(tail, (20,20))
            snakebody = pygame.transform.scale(body, (20,20))

            #Display ranking
            if i <= 2:
                #Medal icon for top 3
                screen.blit(pygame.transform.scale(medals[i], (20,25)), (widthvar - 160, game.settings.height * 4 + i*40))
            else:
                small_message_display(str(str(i+1) + "th "), widthvar - 150, game.settings.height * 4 + i*40 + 10)

            #Snake icon = head + body * score * value + tail
            #head
            screen.blit(snakehead, (widthvar - 130, game.settings.height * 4 + i*40))

            #1 body icon for every 5 points
            for j in range(0, leaderboard[i][0] // 5):
                if j > 16:
                    break
                screen.blit(snakebody, (widthvar - 110 + 20*j, game.settings.height * 4 + i*40))

            #Tail
            screen.blit(snaketail, (widthvar - 110 + (20*(leaderboard[i][0] // 5)), game.settings.height * 4 + i*40))

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
    sum = 0
    while not gamee.game_end_over_and_under():
        pygame.event.pump()
        move = human_move()
        fps = 10
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)
    
    crash(sum - 3, snake.color)

# No boundaries - CAN CROSS OVER WALLS
def game_loop_no_boundaries(player, color, fps=10): 
    
    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake
    
    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 10
        gamee.do_move_no_boundaries(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

    crash(sum - 3, snake.color)

# Progressive difficulty - increases difficulty as time increments
def game_loop_progressive(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    i = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 5 + i
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)
        i += 0.01

    crash(sum - 3, snake.color)

# Easy difficulty - slow snake
def game_loop_easy(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 5
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

    crash(sum - 3, snake.color)

# Medium difficulty - faster snake
def game_loop_medium(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 10
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

    crash(sum - 3, snake.color)

# Hard difficulty - fastest snake
def game_loop_hard(player, color, fps=10):

    global game
    gamee = Game(Snake(color))

    global snake
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 15
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

    crash(sum - 3, snake.color)

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

# all the introductions        
def help_interface(player, color):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        widthvar = game.settings.width * 7.5
        message_display('Introduction of the game', widthvar, game.settings.height * 2, white, 40)
        small_message_display('Welcome to Gluttony!', widthvar, game.settings.height * 3.1, white)
        small_message_display('Control an ever-hungry ever-growing snake', widthvar,
                              game.settings.height * 4, white)
        small_message_display('Eat strawberries to get bigger', widthvar,
                              game.settings.height * 5, white)                      
        small_message_display('Use (wasd) or the arrow keys to navigate the screen', widthvar, game.settings.height * 6,
                              white)
        small_message_display('But beware, hitting yourself is bad >:)', widthvar,
                              game.settings.height * 7, white)
        

        button('Over and Under', widthvar - 170, 220, 100, 40, green, green, introductions, 'human', color, 'Over and Under', 13)
        button('No Boundaries', widthvar - 50, 220, 100, 40, green, green, introductions, 'human', color, 'No Boundaries', 13)
        button('Progressive', widthvar + 70, 220, 100, 40, green, green, introductions, 'human', color, 'Progressive', 13)

        button('Easy', widthvar - 170, 280, 100, 40, green, green, introductions, 'human', color, 'Easy')
        button('Medium', widthvar - 50, 280, 100, 40, green, green, introductions, 'human', color, 'Medium')
        button('Hard', widthvar + 70, 280, 100, 40, green, green, introductions, 'human', color, 'Hard')

        button('Exit', widthvar - 50, 340, 100, 30, red, red, initial_interface)

        pygame.display.update()
        pygame.time.Clock().tick(20)

message_dictionary = {'Over and Under': ["If you hit yourself, you will pass over/under instead of dying", None], 
                    'No Boundaries': ["The boundaries of the arena act as portals", "Thus, passing through one side, brings you out the other"],
                    'Progressive': ["The speed of the snake will slowly increase as the game continues", "While the beginning may seem easy, it gets harder later on"],
                    'Easy': ["For a nice, slow introduction to the game", None],
                    'Medium': ["For the experienced players looking for a moderately paced game", None],
                    'Hard': ["Only for seasoned experts", None]}

#Python doesn't like declaring functions below their reference(s), so introductions must be defined at the bottom
game_loop_dictionary = {'Over and Under': game_loop_over_and_under, 
                    'No Boundaries': game_loop_no_boundaries,
                    'Progressive': game_loop_progressive,
                    'Easy': game_loop_easy,
                    'Medium': game_loop_medium,
                    'Hard': game_loop_hard}

def introductions(player, color, gamemode):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display("Introduction to " + gamemode, game.settings.width * 7.5, game.settings.height * 2, white, 35)

        small_message_display(message_dictionary[gamemode][0], game.settings.width * 7.5, game.settings.height * 6, white)
        small_message_display(message_dictionary[gamemode][1], game.settings.width * 7.5, game.settings.height * 8, white)

        button("Exit", 445, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 445/2, 340, 100, 30, green, bright_green, game_loop_dictionary[gamemode], 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)

if __name__ == "__main__":
    initial_interface()
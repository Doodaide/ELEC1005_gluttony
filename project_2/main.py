# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018
@author: zou
"""

#from turtle import screensize #Pretty sure this causes problems as I need tkinter for it to work
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
from game import Game
from game import Snake
import random

# Mostly initialization of the colours, and backgrounds used 
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
greyy = pygame.Color(80,80,80)

# Sets up the stuff we can see like the snake on the home screen, game-ticks, and the caption
game = Game(Snake('green'))
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

# Default crash sound
crash_sound = pygame.mixer.Sound('./sound/crash.wav')

# Initially, the leaderboard is set to a blank list.
leaderboard = []

# Tries to read the saved data 
try: 
    a = 0 # Score counter 
    b = 1 # colour counter 
    leaderboard_obj = open("level_files/leaderboard.txt", "r") #opens file 
    temp_leaderboard = leaderboard_obj.readlines() # grabs everyting from the file 
    while a < len(temp_leaderboard) :
        small_boi = [int(temp_leaderboard[a].strip()), temp_leaderboard[b].strip()]
        leaderboard.append(small_boi)
        a += 2 
        b += 2
    leaderboard_obj.close()    
# If some error is met, the entire process is skipped, and the leaderboard starts blank.     
except Exception:
    pass 


try:
    level_file = open("level_files/level.txt", "r")
    read_level = level_file.readline()

    if read_level != "":
        progress_bar_value = int(read_level)
        level_file.close()
        level_file = open("level_files/level.txt", "r")

    elif read_level == "":
        raise TypeError

except Exception:
    level_file = open("level_files/level.txt", "w")
    level_file.write("0")
    level_file.close()
    progress_bar_value = 0
    level_file = open("level_files/level.txt", "r")


progress_bar_intervals = [0, 50, 100, 200, 400, 800]
level_intervals = {0: 'Level 1', 50: 'Level 2', 100: 'Level 3',\
     200: 'Level 4', 400: 'Level 5', 800: ''}


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

# The small message display function also writes text, 
# But literally just writes smaller text
def small_message_display(text, x, y, color=white, size = 20):
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

# Added a text size parameter for button function. Ensures the whole message fits
def button(msg, x, y, w, h, inactive_color, active_color, action=None,\
     parameter=None, parameter2=None, parameter3=None, text_size = 20):

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

def playmusic(filename):
    filepath = rf"{filename}"
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)



# Exits the game and saves the progress of the user in a file
def quitgame():
    pygame.quit()
    
    # # Write the player's new level to a new file
    # # This is done before quitting
    # new_level_file = open("level_files/level.txt", "w")
    # new_level_file.write(str(progress_bar_value))
    # new_level_file.close()
    # level_file.close()

    try: 
        leaderboard_file = open("level_files/leaderboard.txt", "w")

        for score in leaderboard:
            leaderboard_file.write(str(score[0]))
            leaderboard_file.write("\n")
            leaderboard_file.write(str(score[1]))
            leaderboard_file.write("\n")

        leaderboard_file.close()   
    except Exception:
        pass 

    quit()
    
# Plays a sound and ends the current game due to the snake crashing
# Saves score in leaderboard
def crash(score, color):
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15,\
         game.settings.height / 3 * 15, white, 50)
    time.sleep(1)

    global progress_bar_value

    #Sorting algorithm to keep top snakes at front of list
    global leaderboard
    leaderboard.append([score, color])

    #Sort in descending order
    leaderboard.sort(key=lambda x:x[0])
    leaderboard.reverse()

    #Neglect any zero point snakes
    if [0, color] in leaderboard:
        leaderboard.remove([0,color])

# Loads background images
snakebackground = {'green': pygame.image.load('images/snakeicongreen.png'),
                    'blue': pygame.image.load('images/snakeiconblue.png'),
                    'red': pygame.image.load('images/snakeiconred.png'),
                    'purple': pygame.image.load('images/snakeiconpurple.png'),
                    'orange': pygame.image.load('images/snakeiconorange.png'),
                    'yellow': pygame.image.load('images/snakeiconyellow.png'),
                    'pink': pygame.image.load('images/snakeiconpink.png'),
                    'blackandwhite': pygame.image.load('images/snakeiconblackandwhite.png'),
                    'rainbow': pygame.image.load('images/snakeiconrainbow.png')}

# Loads medal images
medals = [pygame.image.load('images/goldmedal.bmp'),
            pygame.image.load('images/silvermedal.bmp'),
            pygame.image.load('images/bronzemedal.bmp')]

# Sets up the initial interface with the customization buttons, skin selection, etc. 
def initial_interface():
    while True:
        playmusic("sound/Scott Lloyd Shelly - Overworld Night.mp3")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        global progress_bar_value

        if progress_bar_value < 800:
            left_progress = next(x for x, val in enumerate(progress_bar_intervals) if val > progress_bar_value)
            left_progress_value = progress_bar_intervals[left_progress - 1]
            right_progress_value = progress_bar_intervals[left_progress]
        else:
            progress_bar_value = 800
            left_progress_value = 400
            right_progress_value = 800

        fractional_progress = int( ((right_progress_value - progress_bar_value)/(right_progress_value - left_progress_value)) * 240 )

        
        question = pygame.image.load('images/help.png')

        screen.fill(black)
        screen.blit(snakebackground['green'], (game.settings.width * 1.5, game.settings.height / 3))
        
        message_display('Snake Game', 262.5, game.settings.height * 5.5, white, 50)

        #progress bar
        small_message_display(level_intervals[left_progress_value], 112.5, 205, white )
        pygame.draw.rect(screen, greyy, (142.5, 205, 240, 5), border_radius=4)
        pygame.draw.rect(screen, green, (142.5, 205, 240 - fractional_progress, 5), border_radius=4)
        small_message_display(level_intervals[right_progress_value], 412.5, 205, white )

        # Leaderboard "trophy" icon
        smalltrophy = pygame.image.load('images/trophy.png')
        trophy = pygame.transform.scale(smalltrophy, (35,35))
        button('', 245, 250, 40,40, black, black, leaderboard_ui)
        screen.blit(trophy, (245, 250))

        button('Go!', 142.5, 250, 80, 40, green, bright_green, game_loop_easy, 'human', 'green')
        button('Quit', 302.5, 250, 80, 40, red, bright_red, quitgame)

        #settings interface link
        button('Settings', 222.5, 310, 80, 40, yellow, bright_yellow, settings_interface,'human', 'green')
        
        button('', 0,0,80,40, black, black, help_interface, 'human', 'green')
        small_message_display('Help', 25, 20, white)
        questionn = pygame.transform.scale(question, (20,20))
        screen.blit(questionn, (45,10))

        pygame.display.update()
        pygame.time.Clock().tick(15)

# Renders the initial buttons which customize game modes
# and difficulties, 
def settings_interface(player, color):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)

        #Snake icon to change colour
        button('', 100, 30, 350, 67, black, black, color_interface)
        screen.blit(snakebackground[color], (game.settings.width * 1.5, game.settings.height / 10))


        message_display('Customise game', 262.5, game.settings.height * 5.5, white, 50)
        small_message_display('*click me*', 67, 72, white)
        
        #Customise Game Modes
        button('Over and Under', 92.5, 200, 100, 40, green, green, game_loop_over_and_under, 'human', color,'Over and Under', 20)
        button('No Boundaries', 212.5, 200, 100, 40, green, green, game_loop_no_boundaries, 'human', color, 'No Boundaries',20)
        button('Progressive', 332.5, 200, 100, 40, green, green, game_loop_progressive, 'human', color, 'Progressive', 20)

        button('Easy', 92.5, 270, 100, 40, green, green, game_loop_easy, 'human', color)
        button('Medium', 212.5, 270, 100, 40, green, green, game_loop_medium, 'human', color)
        button('Hard', 332.5, 270, 100, 40, green, green, game_loop_hard, 'human', color)

        button('Exit', 212.5, 350, 100, 30, red, red, initial_interface)

        pygame.display.update()
        pygame.time.Clock().tick(20)
        
# Prompts the user for a snake colour
def color_interface():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        
        message_display('Choose Your Snake', 262.5, game.settings.height * 2, white, 50)

        widthvar = 262.5

        #Colour interface
        global progress_bar_value

        #Green Snake
        button('', widthvar - 200,100,185,40,black,black, settings_interface, 'player', 'green')
        snakegreen = pygame.transform.scale(snakebackground['green'], (200,50))
        screen.blit(snakegreen, (widthvar - 220, 90))

        #Blue Snake
        button('', widthvar - 200,170,180,40,black,black, settings_interface, 'player', 'blue')
        snakeblue = pygame.transform.scale(snakebackground['blue'], (200,50))
        screen.blit(snakeblue, (widthvar - 220, game.settings.height * 6 - 10))

        #Red Snake
        button('', widthvar - 200,240,180,40,black,black, settings_interface, 'player', 'red')
        snakered = pygame.transform.scale(snakebackground['red'], (200,50))
        screen.blit(snakered, (widthvar - 220, game.settings.height * 8))

        #Yellow Snake
        button('', widthvar - 200,310,180,40,black,black, settings_interface, 'player', 'yellow')
        snakeyellow = pygame.transform.scale(snakebackground['yellow'], (200,50))
        screen.blit(snakeyellow, (widthvar - 220, game.settings.height * 10 + 10))


        #MUST UNLOCK THESE SNAKES
        snakegrey = pygame.transform.scale(snakebackground['blackandwhite'], (200,50))
        lockicon = pygame.transform.scale(pygame.image.load('images/lockicon.png'), (25,25))

        #Purple Snake
        if progress_bar_value >= 50:
            button('', 300,100,180,40,black,black, settings_interface, 'player', 'purple')
            snakepurple = pygame.transform.scale(snakebackground['purple'], (200,50))
            screen.blit(snakepurple, (290, 90))
        else:
            screen.blit(snakegrey, (290, 90))
            screen.blit(lockicon, (270, game.settings.height * 4 - 5))
            small_message_display('level 2', 284, game.settings.height * 4 + 28)

        #Pink Snake
        if progress_bar_value >= 100:
            button('', 300,170,180,40,black,black, settings_interface, 'player', 'pink')
            snakepink = pygame.transform.scale(snakebackground['pink'], (200,50))
            screen.blit(snakepink, (290, game.settings.height * 6 - 10))
        else:
            screen.blit(snakegrey, (290, game.settings.height * 6 - 10))
            screen.blit(lockicon, (290 - 20, game.settings.height * 6 + 7))
            small_message_display('level 3', 290 - 6, game.settings.height * 6 + 40)

        #Orange Snake
        if progress_bar_value >= 200:
            button('', 300,240,180,40,black,black, settings_interface, 'player', 'orange')
            snakeorange = pygame.transform.scale(snakebackground['orange'], (200,50))
            screen.blit(snakeorange, (290, game.settings.height * 8))
        else:
            screen.blit(snakegrey, (290, game.settings.height * 8))
            screen.blit(lockicon, (290 - 20, game.settings.height * 8 + 17))
            small_message_display('level 4', 290 - 6, game.settings.height * 8 + 50)

        #Rainbow snake
        if progress_bar_value >= 400:
            button('', 300, 310, 180, 40, black, black, settings_interface, 'player', 'rainbow')
            snakerainbow = pygame.transform.scale(snakebackground['rainbow'], (200,50))
            screen.blit(snakerainbow, (290, game.settings.height * 10 + 10))
        else:
            screen.blit(snakegrey, (290, game.settings.height * 10 + 10))
            screen.blit(lockicon, (290 - 20, game.settings.height * 10 + 27))
            small_message_display('level 5', 290 - 6, game.settings.height * 10 + 60)


        pygame.display.update()
        pygame.time.Clock().tick(15)

# Shows the current
def leaderboard_ui():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #initialise static screen
        screen.fill(black)
        message_display('Leaderboard', 262.5, game.settings.height * 2, white, 50)
        button('Exit', 262.5 - 50, 340, 100, 30, red, red, initial_interface)

        #state variables
        head = pygame.image.load('skin/head_left_g.bmp')
        tail = pygame.image.load('skin/tail_left_g.bmp')
        body = pygame.image.load('skin/body_g.bmp')
        snakehead = pygame.transform.scale(head, (20,20))
        snaketail = pygame.transform.scale(tail, (20,20))
        snakebody = pygame.transform.scale(body, (20,20))

        widthvar = 262.5

        for i in range(0, len(leaderboard)):
            if i >= 5:
                break

            #Retrieve the colouring of the recently played snake
            if leaderboard[i][1] != 'rainbow':
                head = pygame.image.load('skin/head_left' + file_dictionary[leaderboard[i][1]] + '.bmp')
                tail = pygame.image.load('skin/tail_left' + file_dictionary[leaderboard[i][1]] + '.bmp')
                body = pygame.image.load('skin/body' + file_dictionary[leaderboard[i][1]] + '.bmp')

            elif leaderboard[i][1] == 'rainbow':
                head = pygame.image.load('skin/head_left' + file_dictionary['blue'] + '.bmp')
                tail = pygame.image.load('skin/tail_left' + file_dictionary['pink'] + '.bmp')


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

            if leaderboard[i][0] // 5 == 0:
                screen.blit(snakehead, (widthvar - 130, game.settings.height * 4 + i*40))
                screen.blit(snaketail, (widthvar - 110, game.settings.height * 4 + i*40))
                small_message_display(str(leaderboard[i][0]), widthvar - 110 + 40, game.settings.height * 4 + i*40 + 10)

            else:
                screen.blit(snakehead, (widthvar - 130, game.settings.height * 4 + i*40))
                if leaderboard[i][0] // 5 >= 14: 
                    endvalue =  14
                else:
                    endvalue = leaderboard[i][0] // 5

                for j in range(0, endvalue):
                    if leaderboard[i][1] == 'rainbow':
                        body = random.choice([pygame.image.load('skin/body_b.bmp'),
                                            pygame.image.load('skin/body_g.bmp'),
                                            pygame.image.load('skin/body_lp.bmp'),
                                            pygame.image.load('skin/body_o.bmp'),
                                            pygame.image.load('skin/body_p.bmp'),
                                            pygame.image.load('skin/body_r.bmp'),
                                            pygame.image.load('skin/body_y.bmp')])
                        snakebody = pygame.transform.scale(body, (20,20))

                    screen.blit(snakebody, (widthvar - 110 + 20*j, game.settings.height * 4 + i*40))
                    if j == endvalue - 1:
                        screen.blit(snaketail, (widthvar - 90 + 20*j, game.settings.height * 4 + i*40))
                        small_message_display(str(leaderboard[i][0]), widthvar - 90 + 20*j + 40, game.settings.height * 4 + i*40 + 10)


        pygame.display.update()
        pygame.time.Clock().tick(20)


# Gamemodes: 
# Over and under - don't die from hitting yourself
def game_loop_over_and_under(player, color, fps=10): 
    playmusic("sound/Scott Lloyd Shelly - Overworld Night.mp3")
    global game, snake, progress_bar_value
    gamee = Game(Snake(color))
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
        
    pygame.mixer.music.fadeout(1)
    playmusic("sound/Scott Lloyd Shelly - Overworld Day.mp3")

    #Set score valut (easier game mode = 1 point)
    progress_bar_value += (sum - 3)
    crash((sum - 3), snake.color)

# No boundaries - CAN CROSS OVER WALLS
def game_loop_no_boundaries(player, color, fps=10): 
    playmusic("sound/Scott Lloyd Shelly - The Hallow.mp3")

    #Retrieve global variables
    global game, snake, progress_bar_value
    gamee = Game(Snake(color))
    snake = gamee.snake
    
    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        fps = 10

        #Customised move function
        gamee.do_move_no_boundaries(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)
        
    pygame.mixer.music.fadeout(1)
    playmusic("sound/Scott Lloyd Shelly - Overworld Day.mp3")

    #Customise score (easier game mode = 1 point)
    progress_bar_value += (sum - 3)
    crash(sum - 3, snake.color)

# Progressive difficulty - increases difficulty as time increments
def game_loop_progressive(player, color, fps=10):
    playmusic("sound/Scott Lloyd Shelly - Boss 3.mp3")

    #Retrieve global variables
    global game, snake, progress_bar_value
    gamee = Game(Snake(color))
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    speed = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()
        
        #Speed
        fps = 5 + speed

        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

        #Increment Speed
        speed += 0.01
        
    pygame.mixer.music.fadeout(1)
    playmusic("sound/Scott Lloyd Shelly - Overworld Day.mp3")

    #Set score (medium level game mode = 2 points)
    progress_bar_value += (sum - 3)*2
    crash((sum - 3), snake.color)

# Easy difficulty - slow snake
def game_loop_easy(player, color, fps=10):
    playmusic("sound/T_Space.mp3")

    #Fetch global variables
    global game, snake, progress_bar_value
    gamee = Game(Snake(color))
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()

        #Slowest speed = easier
        fps = 5
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)
    
    pygame.mixer.music.fadeout(1)
    playmusic("sound/Scott Lloyd Shelly - Overworld Day.mp3")

    #Set score (easier game mode = 1 point)
    progress_bar_value += (sum - 3)
    crash((sum - 3), snake.color)

# Medium difficulty - faster snake
def game_loop_medium(player, color, fps=10):
    playmusic("sound/Ballad_of_the_Cats.mp3")

    #Fetch global variables
    global game, snake, progress_bar_value
    gamee = Game(Snake(color))
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()

        #Increase speed
        fps = 10
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

    pygame.mixer.music.fadeout(1)
    playmusic("sound/Scott Lloyd Shelly - Overworld Day.mp3")

    #Set score (medium game mode = 2 points)
    progress_bar_value += (sum - 3)*2
    crash((sum - 3), snake.color)

# Hard difficulty - fastest snake
def game_loop_hard(player, color, fps=10):
    playmusic("sound/01. Hell On Earth.mp3")

    #Fetch global variables
    global game, snake, progress_bar_value
    gamee = Game(Snake(color))
    snake = gamee.snake

    gamee.restart_game()
    sum = 0
    while not gamee.game_end():
        pygame.event.pump()
        move = human_move()

        #Hardest game mode = 3x speed = 15
        fps = 15
        gamee.do_move_normal(move)
        screen.fill(black)
        gamee.snake.blit(rect_len, screen)
        gamee.strawberry.blit(screen)
        gamee.blit_score(white, screen)
        sum = gamee.snake.getsize()
        pygame.display.flip()
        fpsClock.tick(fps)

    pygame.mixer.music.fadeout(1)
    playmusic("sound/Scott Lloyd Shelly - Overworld Day.mp3")

    #Set score (Hardest game mode = 3 points)
    progress_bar_value += (sum - 3)*3
    crash((sum - 3), snake.color)

# returns the corresponding move detected by human input
def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        #Retrieve user inputs
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

# Displays a help manual to teach new users how to play        
def help_interface(player, color):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(black)
        widthvar = 262.5
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
        button('No Boundaries', widthvar - 50, 220, 100, 40, green, green, introductions, 'human', color, 'No Boundaries', 14)
        button('Progressive', widthvar + 70, 220, 100, 40, green, green, introductions, 'human', color, 'Progressive', 15)

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

# Displays the introductory message
def introductions(player, color, gamemode):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(black)
        message_display("Introduction to " + gamemode, 262.5, game.settings.height * 2, white, 35)

        small_message_display(message_dictionary[gamemode][0], 262.5, game.settings.height * 6, white, 15)
        small_message_display(message_dictionary[gamemode][1], 262.5, game.settings.height * 8, white, 15)

        button("Exit", 445, 380, 80, 40, red, bright_red, help_interface, 'human', 'green')
        button('Go', 445/2, 340, 100, 30, green, bright_green, game_loop_dictionary[gamemode], 'human', color)

        pygame.display.update()
        pygame.time.Clock().tick(20)

if __name__ == "__main__":
    initial_interface()
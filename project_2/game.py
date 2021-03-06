# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np

# Settings class initialises the width, height, and length of the settings object
# No other class methods 
class Settings:
    def __init__(self):
        # 屏幕属性
        self.width = 35
        self.height = 28
        self.rect_len = 15

# Snake class - makes the controllable snake object the player interacts with
class Snake:
    def __init__(self, color):
        
        # Attribute of snake object: colour 
        self.color = color
        self.settings = Settings()

        file_dictionary = {'green': '_g',
                            'red': '_r',
                            'blue': '_b',
                            'yellow': '_y',
                            'purple': '_lp',
                            'orange': '_o',
                            'pink': '_p'}

        # This section controls the snake's customizable colouring 
        if self.color.lower() == 'rainbow':
            filesource = random.choice(list(file_dictionary.values()))
        else:
            filesource = file_dictionary[self.color.lower()]
        

        #create subfolders in the images folder for each distinct snake colour
        self.image_up = pygame.image.load('skin/head_up' + filesource + '.bmp')
        self.image_down = pygame.image.load('skin/head_down' + filesource + '.bmp')
        self.image_left = pygame.image.load('skin/head_left' + filesource + '.bmp')
        self.image_right = pygame.image.load('skin/head_right' + filesource + '.bmp')

        self.tail_up = pygame.image.load('skin/tail_up' + filesource + '.bmp')
        self.tail_down = pygame.image.load('skin/tail_down' + filesource + '.bmp')
        self.tail_left = pygame.image.load('skin/tail_left' + filesource + '.bmp')
        self.tail_right = pygame.image.load('skin/tail_right' + filesource + '.bmp')
            
        self.image_body = pygame.image.load('skin/body' + filesource + '.bmp')

        # starts the snake game facing right, and the game begins
        self.facing = "right"

        #starts the snake at a pre-determined position at default 0 score
        self.initialize()
        
    #resets the position and score to the initial value
    def initialize(self):
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0
        
        #returns the length of the snake
    def getsize(self):
        return len(self.segments)

    # Visualises the snake on the map 
    def blit_body(self, x, y, screen):
        if self.color.lower() == 'rainbow':
            self.image_body = random.choice([pygame.image.load('skin/body_b.bmp'),
                                            pygame.image.load('skin/body_g.bmp'),
                                            pygame.image.load('skin/body_lp.bmp'),
                                            pygame.image.load('skin/body_o.bmp'),
                                            pygame.image.load('skin/body_p.bmp'),
                                            pygame.image.load('skin/body_r.bmp'),
                                            pygame.image.load('skin/body_y.bmp')])

        screen.blit(self.image_body, (x, y))
         
    #defines the movement of the head
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y)) 
            
    #defines the movement of the tail        
    def blit_tail(self, x, y, screen):
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        
        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  
    
    def blit(self, rect_len, screen):
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
        
    #updates the position of the snake
    def update(self):
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))

    # A special function for the no_boundaries gamemode 
    # When the snake encounters a "boundary position", 
    # reset its head position to the other side of the "arena"
    # Giving it the illusion that it passed through the side 
    def update_no_boundaries(self):
        if self.facing == 'right':
            if self.position[0] == self.settings.width - 1:
                self.position[0] = 0
            else:
                self.position[0] += 1
        
        if self.facing == 'left':
            if self.position[0] == 0:
                self.position[0] = self.settings.width - 1
            else:
                self.position[0] -= 1

        if self.facing == 'up':
            if self.position[1] == 0:
                self.position[1] = self.settings.height - 1
            else:
                self.position[1] -= 1

        if self.facing == 'down':
            if self.position[1] == self.settings.height - 1:
                self.position[1] = 0
            else:
                self.position[1] += 1

        self.segments.insert(0, list(self.position))

# Strawberry class - makes food objects the snake consumes         
class Strawberry():
    def __init__(self, settings):
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')        
        self.initialize()
        
    # This method loads the food-item in a pseudo-random position on the map    
    def random_pos(self, snake):
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')           
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        # self.position[0] = random.randint(0, 46)
        # self.position[1] = random.randint(0, 28)
        
        #reposition the food item if it is repositioned inside the snake
        if self.position in snake.segments:
            self.random_pos(snake)
    
    #updates the food objects in the map
    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    # The position of the first strawberry
    def initialize(self):
        self.position = [15, 10]

# Game class          
class Game:

    def __init__(self, snake):
        # starts settings, makes snake, strawberries, and assigns movement 
        self.settings = Settings()
        self.snake = snake
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
    # This method restarts the game and re-initialises the snake and food item      
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()

    #returns the current state of the game    
    def current_state(self):         
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    #returns the direction of the snake as an integer
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    # This method moves the snake based on inputs     
    def do_move_normal(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()
        
        if self.snake.position == self.strawberry.position:
            self.strawberry.random_pos(self.snake)
            reward = 1
            self.snake.score += 1
        else:
            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward

    # For the no_boundaries gamemode, a new set of movements must be defined
    def do_move_no_boundaries(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        #New line
        self.snake.update_no_boundaries()
        
        if self.snake.position == self.strawberry.position:
            self.strawberry.random_pos(self.snake)
            reward = 1
            self.snake.score += 1
        else:
            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward
        
    # If the snake hits itself, game over
    def game_end(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end

    # For the over_and_under gammode, if the snake hits itself the game shouldn't end
    # Thus, a new method must be defined
    def game_end_over_and_under(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True

        return end
    
    #This method renders a score for the user to see at a certain position on screen. 
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))




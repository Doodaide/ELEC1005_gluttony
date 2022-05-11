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
        self.width = 28
        self.height = 28
        self.rect_len = 15

# Snake class - makes the controllable snake object the player interacts with
class Snake:
    def __init__(self, color):
        
        # Attribute of snake object: colour 
        self.color = color

        # This section controls the snake's customizable colouring 
        if self.color.lower() == 'green':
            filesource = '_g'
        if self.color.lower() == 'red':
            filesource = '_r'
        if self.color.lower() == 'blue':
            filesource = '_b'
        if self.color.lower() == 'yellow':
            filesource = '_y'
        if self.color.lower() == 'purple':
            filesource = '_lp'
        if self.color.lower() == 'orange':
            filesource = '_o'
        if self.color.lower() == 'pink':
            filesource = '_p'
        

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

    def initialize(self):
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0
   
    
    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
            
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

    def update_no_boundaries(self):
        if self.facing == 'right':
            if self.position[0] == 27:
                self.position[0] = 0
            else:
                self.position[0] += 1
        
        if self.facing == 'left':
            if self.position[0] == 0:
                self.position[0] = 27
            else:
                self.position[0] -= 1

        if self.facing == 'up':
            if self.position[1] == 0:
                self.position[1] = 27
            else:
                self.position[1] -= 1

        if self.facing == 'down':
            if self.position[1] == 27:
                self.position[1] = 0
            else:
                self.position[1] += 1

        self.segments.insert(0, list(self.position))
        
class Strawberry():
    def __init__(self, settings):
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')        
        self.initialize()
        
    def random_pos(self, snake):
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')           
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self):
        self.position = [15, 10]
              
class Game:

    def __init__(self):
        self.settings = Settings()
        self.snake = Snake('green')
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
        
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()

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
    
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
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
        
    
    def game_end(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end

    def game_end_over_and_under(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True

        return end
    
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))


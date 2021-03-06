import math

import pygame, sys,os,random,csv # import pygame and sys
import numpy as np
import pathlib
from pathlib import *
clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
import time
import zmq
import pandas as pd

pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

name = joystick.get_name()

force_feedback = True

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

##Gamevariables
run =True

directory_time = Path.cwd() /'Data_Time'
user_input=input("What's your name and trialnumber?:")
filepath_time = directory_time / user_input

# directory_collision="/home/isurana/Desktop/Robotics/Quarter-4/AEM/My_version/v1/Data_Collision/"
# user_input=input("What's your name?:")
# filepath_collision = directory_collision + user_input


def load_map(path):
    f=open(path+'.txt',"r")
    data=f.read()
    f.close()
    data=data.split('\n')
    game_map=[]
    for row in data:
        game_map.append(list(row))
    return game_map

game_map=load_map('map')


## Check for collision

def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    
            #print(hit_list)
    return hit_list





def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:

        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    # print("Hit List",hit_list)
    # np.save(pathlib.Path(filepath_collision),hit_list) # save
    return rect, collision_types

time_list=[]
def score_display(game_state):
    if game_state=='main_game':
        score_surface=game_font.render(f'Time: {int(score)}',True,(255,255,255))
        score_rect=score_surface.get_rect(center=(525,50))
        display.blit(score_surface,score_rect)
        # print("Score",score)
        time_list.append(score)
        # print(time_list)

def force(x,y):
    y_force = dfforce.iat[y,x]
    x_force = dfforce2.iat[y,x]
    gain = 2
    y_force = round(np.clip(y_force*99*gain,-99,99))
    y_force = y_force*1000
    return y_force

dfforce = pd.read_csv('ytest.csv')  # load force files
dfforce2 = pd.read_csv('xtest.csv')


pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (1200,800) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((600, 400))


pygame.mixer.music.load('music/music.wav')
pygame.mixer.music.play(-1)

player_image = pygame.image.load('images/drone_16.png')


roof_image = pygame.image.load('images/roof.png')
TILE_SIZE = roof_image.get_width()




dirt_image = pygame.image.load('images/tile2-m.png')
platform_image_up=pygame.image.load('images/tile-u.png')
platform_image_down=pygame.image.load('images/tile-d.png')
platform_image=pygame.image.load('images/platform.png')
coin_image=pygame.image.load('images/coin1.png')





clock=pygame.time.Clock()
game_font=pygame.font.Font('04B_19.TTF',20)

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0
true_scroll=[0,0]
scroll=[0,0]
player_rect = pygame.Rect(50, 250, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)
collision_sound_timer=0
score=0
high_score=0
game_active=True

x_joystick=0
y_joystick=0
counter=0

timer=0

df1 = df = pd.DataFrame({'time':[0], 'collisions':[0],'collision_type':[0], 'x_joystick':[0], 'y_joystick':[0]})

while run: # game loop

        
    true_scroll[0]+=(player_rect.x-scroll[0]-352)/20
    true_scroll[1]+=(player_rect.y-scroll[1]-206)/20
    scroll=true_scroll.copy()
    scroll[0]=int(scroll[0])
    scroll[1]=int(scroll[1])    
    
    display.fill((25,25,25))
    

    
        
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(roof_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '3':
                display.blit(platform_image_up, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '4':
                display.blit(platform_image_down, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '5':
                display.blit(platform_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '6':
                display.blit(coin_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
    
            x += 1
        y += 1
        
    np.save(pathlib.Path(filepath_time),time_list) # save
    
    player_movement = [0, 0]
    player_movement[0] += x_joystick*5
    player_movement[1] += y_joystick*10
    player_y_momentum += 0
    # if player_y_momentum > 3:
        # player_y_momentum = 3

    # game_end(player_rect,tile_rects)


    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if player_rect[0] >= 6040:
        run = False

    F_y = force(player_rect[0],player_rect[1])
    if F_y <= 0:
        F_y = np.abs(F_y)
    else:
        F_y = F_y+180
    if force_feedback:
        message = socket.recv()
        socket.send(bytes(str(F_y), 'utf8'))

    print(player_rect)
    ################################# collisions
    if collisions['bottom']:
        counter=0
        collide=1
        player_y_momentum=-0.5
    elif collisions['top']:
        counter=0
        collide = 1
        player_y_momentum=1
    elif collisions['left']:
        counter = 0
        collide = 1
        player_y_momentum = 1
    elif collisions['right']:
        counter = 0
        collide = 1
        player_y_momentum = 1
    else:
        counter+=1
        collide=0


    df2 = pd.DataFrame({'time': [timer], 'collisions': [collide],'collision_type': [collisions], 'x_joystick': [x_joystick], 'y_joystick': [y_joystick]})

    frames = [df1, df2]
    df1 = pd.concat(frames)
    timer+=1
        
    if game_active:
        score+=0.024
        score_display('main_game')



    ## Joystick
    x_joystick = joystick.get_axis(0)
    y_joystick=joystick.get_axis(1)

    display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key==K_w:   ## Press w to fade the music put
                pygame.mixer.music.fadeout(1000)
            if event.key==K_ESCAPE:
                run=False





    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(80) # maintain 90 fps

if force_feedback:
    csv_name_string = 'results/results_of_{}_with_haptic_.csv'.format(user_input)
else:
    csv_name_string = 'results/results_of_{}_without_haptic_.csv'.format(user_input)
df1.to_csv(csv_name_string)
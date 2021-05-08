import pygame, sys,os,random # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (1200,800) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((600, 400))

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

pygame.mixer.music.load('music/music.wav')
pygame.mixer.music.play(-1)

player_image = pygame.image.load('images/drone_16.png')
player_image.set_colorkey((255, 255, 255))

grass_image = pygame.image.load('images/grass.png')
TILE_SIZE = grass_image.get_width()



dirt_image = pygame.image.load('images/dirt.png')



def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
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
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0
true_scroll=[0,0]
scroll=[0,0]
player_rect = pygame.Rect(50, 250, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

collision_sound_timer=0

while True: # game loop



    
    true_scroll[0]+=(player_rect.x-scroll[0]-352)/20
    true_scroll[1]+=(player_rect.y-scroll[1]-206)/20
    scroll=true_scroll.copy()
    scroll[0]=int(scroll[0])
    scroll[1]=int(scroll[1])    
    
    display.fill((25,25,25)) 
    
    
    if collision_sound_timer>0:
        collision_sound_timer-=1
        
        
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0
    # if player_y_momentum > 3:
        # player_y_momentum = 3



    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

        

    display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key==K_w:   ## Press w to fade the music out
                pygame.mixer.music.fadeout(1000)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                player_y_momentum =-1
            if event.key==K_DOWN:
                player_y_momentum=+1
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key==K_UP:
                    player_y_momentum += 0.2
                    if player_y_momentum > 3:
                        player_y_momentum = 3
            if event.key==K_DOWN:
                    player_y_momentum += 0.2
                    if player_y_momentum > 3:
                        player_y_momentum = 3
            
                
            

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps

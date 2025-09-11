import pygame
import sys
import random

# init Pygame
pygame.init()

# set up display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fleater")

# player info
player_width, player_height = 50, 50
player_x, player_y = 375, 500
player_speed = 5
player_color = (65, 145, 65)

# falling things to eat
object_width, object_height = 30, 30
object_color = (200, 50, 50)
falling_objects = []
object_speed = 3
spawn_timer = 0

# clock
clock = pygame.time.Clock()

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # get key strokes
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    
    # fill the screen with black
    screen.fill((0, 0, 0))
    
    # spawn falling objects
    spawn_timer += 1
    if spawn_timer > 360:
        spawn_timer = 0
        object_x = random.randint(0, WIDTH - object_width) # x value for where object should start; random
        falling_objects.append(pygame.Rect(object_x, 0, object_width, object_height))
        # 0 is y value, so top of screen
        # object_width and object_height are the size of the object
        # append adds a new object to falling_objects list
        
    # update falling objects
    for object in falling_objects[:]:
        object.y += object_speed
        pygame.draw.rect(screen, object_color, object)

        # check for collisions
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if player_rect.colliderect(object):
            falling_objects.remove(object)
            # if player collides with object, remove it from the list
        
        # remove objects that fall off the screen
        elif object.y > HEIGHT:
            falling_objects.remove(object)
        
    # player visual
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # update the display
    pygame.display.flip()
    
    # cap the frame rate
    clock.tick(60) 
    
# quit Pygame
pygame.quit()
sys.exit()
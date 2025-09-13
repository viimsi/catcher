import pygame
import sys
import random
from other_screens import show_start_screen, show_game_over_screen

# init Pygame
pygame.init()

# set up display
WIDTH = 828
HEIGHT = 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fleater")

# background image
bg_sprite = pygame.image.load("resources/bg.png").convert()

frame_width, frame_height = 207, 144
frame_1_x, frame_1_y = 0, 0
frame_2_x, frame_2_y = frame_width, 0

bg1_frame = bg_sprite.subsurface((frame_1_x, frame_1_y, frame_width, frame_height))
bg2_frame = bg_sprite.subsurface((frame_2_x, frame_2_y, frame_width, frame_height))

bg_1_scaled = pygame.transform.scale(bg1_frame, (frame_width * 4, frame_height * 4))
bg_2_scaled = pygame.transform.scale(bg2_frame, (frame_width * 4, frame_height * 4))

current_bg_frame = bg_1_scaled
last_switch_time = 0

# player info
player_width, player_height = 50, 50
player_x, player_y = 375, 500
player_speed = 5
player_color = (65, 145, 65)

player_health = 5
heart_width, heart_height = 30, 30
heart_color = (247, 31, 31)

# falling things to eat
object_width, object_height = 30, 30
falling_objects = []
object_speed = 3
spawn_timer = 0

# clock
clock = pygame.time.Clock()

# show start screen
show_start_screen(screen, WIDTH, HEIGHT)

# game reset
def reset_game():
    global player_health, falling_objects, spawn_timer, player_x, player_y
    player_health = 5
    falling_objects.clear()
    player_x, player_y = 375, 500

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
    
    # draw the background
    frame_switch_interval = random.randint(200, 800) # milliseconds
    
    current_bg_frame_time = pygame.time.get_ticks()
    if current_bg_frame_time - last_switch_time > frame_switch_interval:
        last_switch_time = current_bg_frame_time
        current_bg_frame = bg_2_scaled if current_bg_frame == bg_1_scaled else bg_1_scaled
        
    screen.blit(current_bg_frame, (0, 0))
    
    # draw health
    for i in range(player_health):
        pygame.draw.rect(screen, heart_color, (10 + i * (heart_width + 5), 10, heart_width, heart_height))

    # spawn falling objects
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_timer = 0
        object_x = random.randint(0, WIDTH - object_width) # x value for where object should start; random
        object_type = random.choice(["bad", "good"])
        object_color = (200, 50, 50) if object_type == "bad" else (50, 200, 50)
        falling_objects.append({
                                "rect": pygame.Rect(object_x, 0, object_width, object_height),
                                "type": object_type,
                                "color": object_color})
        # 0 is y value, so top of screen
        # object_width and object_height are the size of the object
        # append adds a new object to falling_objects list

    # update falling objects
    remaining_objects = []
    for object in falling_objects[:]:
        object["rect"].y += object_speed
        pygame.draw.rect(screen, object["color"], object["rect"])

        # check for collisions
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if player_rect.colliderect(object["rect"]):
            if object["type"] == "good":
                print("Caught a good object!")
            elif object["type"] == "bad":
                print("Caught a bad object!")
                player_health -= 1
                if player_health <= 0:
                    print("Game Over!")
                    show_game_over_screen(screen, WIDTH, HEIGHT)
                    reset_game()
        elif object["rect"].y > HEIGHT:
            pass
        else:
            remaining_objects.append(object)
    
    falling_objects = remaining_objects

    # player visual
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)

# quit Pygame
pygame.quit()
sys.exit()
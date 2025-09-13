import pygame
import sys
import random
import math
from other_screens import show_start_screen, show_game_over_screen

# init Pygame
pygame.init()
pygame.mixer.init()

# sounds
food_sound = pygame.mixer.Sound("resources/pickupCoin.wav")
star_sound = pygame.mixer.Sound("resources/powerUp.wav")
hurt_sound = pygame.mixer.Sound("resources/hitHurt.wav")
gameover_sound = pygame.mixer.Sound("resources/explosion.wav")

# set up display
WIDTH = 828
HEIGHT = 576
PLAYER_X, PLAYER_Y = 400, 420
MAX_HEALTH = 5
FONT = "resources/DigitalDisco.ttf"
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

# score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score, high_score):
    if score > high_score:
        with open("high_score.txt", "w") as file:
            file.write(str(score))
        return score
    return high_score

score = 0
score_font = pygame.font.Font(FONT, 36)
high_score = load_high_score()

# player info
player_width, player_height = 100, 100
player_x, player_y = PLAYER_X, PLAYER_Y
player_speed = 5

player_health = MAX_HEALTH
heart_width, heart_height = 30, 30
heart_color = (247, 31, 31)

player_sprite = pygame.image.load("resources/flea.png").convert_alpha()
player_frame_width, player_frame_height = 100, 100

p_standing_1_x, p_standing_1_y = player_frame_width, 0
p_standing_1n_x, p_standing_1n_y = player_frame_width * 2, 0 # head nodded
p_walking_left_1_x, p_walking_left_1_y = player_frame_width * 3, 0 
p_walking_left_1n_x, p_walking_left_1n_y = player_frame_width * 4, 0 # head nodded
p_walking_left_2_x, p_walking_left_2_y = player_frame_width * 5, 0
p_walking_left_2n_x, p_walking_left_2n_y = player_frame_width * 6, 0 # head nodded
p_walking_right_1_x, p_walking_right_1_y = player_frame_width * 7, 0
p_walking_right_1n_x, p_walking_right_1n_y = player_frame_width * 8, 0 # head nodded
p_walking_right_2_x, p_walking_right_2_y = player_frame_width * 9, 0
p_walking_right_2n_x, p_walking_right_2n_y = player_frame_width * 10, 0 # head nodded

p_standing = player_sprite.subsurface((p_standing_1_x, p_standing_1_y, player_frame_width, player_frame_height))
p_standing_nod = player_sprite.subsurface((p_standing_1n_x, p_standing_1n_y, player_frame_width, player_frame_height))

p_walking_left_1 = player_sprite.subsurface((p_walking_left_1_x, p_walking_left_1_y, player_frame_width, player_frame_height))
p_walking_left_1n = player_sprite.subsurface((p_walking_left_1n_x, p_walking_left_1n_y, player_frame_width, player_frame_height))
p_walking_left_2 = player_sprite.subsurface((p_walking_left_2_x, p_walking_left_2_y, player_frame_width, player_frame_height))
p_walking_left_2n = player_sprite.subsurface((p_walking_left_2n_x, p_walking_left_2n_y, player_frame_width, player_frame_height))
p_walking_right_1 = player_sprite.subsurface((p_walking_right_1_x, p_walking_right_1_y, player_frame_width, player_frame_height))
p_walking_right_1n = player_sprite.subsurface((p_walking_right_1n_x, p_walking_right_1n_y, player_frame_width, player_frame_height))
p_walking_right_2 = player_sprite.subsurface((p_walking_right_2_x, p_walking_right_2_y, player_frame_width, player_frame_height))
p_walking_right_2n = player_sprite.subsurface((p_walking_right_2n_x, p_walking_right_2n_y, player_frame_width, player_frame_height))

# scale sprite
def scale_sprite(sprite):
    scale_factor = float(1.2)
    width = int(sprite.get_width() * scale_factor)
    height = int(sprite.get_height() * scale_factor)
    return pygame.transform.scale(sprite, (width, height))

p_standing = scale_sprite(p_standing)
p_standing_nod = scale_sprite(p_standing_nod)
p_walking_left_1 = scale_sprite(p_walking_left_1)
p_walking_left_1n = scale_sprite(p_walking_left_1n)
p_walking_left_2 = scale_sprite(p_walking_left_2)
p_walking_left_2n = scale_sprite(p_walking_left_2n)
p_walking_right_1 = scale_sprite(p_walking_right_1)
p_walking_right_1n = scale_sprite(p_walking_right_1n)
p_walking_right_2 = scale_sprite(p_walking_right_2)
p_walking_right_2n = scale_sprite(p_walking_right_2n)

walking_left_frames = [p_walking_left_1, p_walking_left_1, p_walking_left_1n, p_walking_left_1, p_walking_left_1, 
                       p_walking_left_2, p_walking_left_2, p_walking_left_2n, p_walking_left_2, p_walking_left_2]

walking_right_frames = [p_walking_right_1, p_walking_right_1, p_walking_right_1n, p_walking_right_1, p_walking_right_1, 
                        p_walking_right_2, p_walking_right_2, p_walking_right_2n, p_walking_right_2, p_walking_right_2,]

standing_frames = [p_standing, p_standing, p_standing_nod, p_standing_nod]

player_state = "standing" # can be "standing", "walking_left", "walking_right"
p_current_frame_index = 0
p_last_animation_time = 0
p_animation_interval = 50

# player is hit
HIT_FLASH_DURATION = 200  # milliseconds
last_hit_time = 0

# player is healed
HEALED_FLASH_DURATION = 200  # milliseconds
last_healed_time = 0

# player shadow
shadow_width = int(player_width * 0.5)
shadow_height = int(player_height * 0.2)
shadow_colour = (0, 0, 0, 100)

# falling things to eat
object_width, object_height = 75, 75
falling_objects = []
object_speed = 3
spawn_timer = 0

speed_increment = 0.0005
max_speed = 10

bad_objects_sprite = pygame.image.load("resources/trash.png").convert_alpha()
good_objects_sprite = pygame.image.load("resources/food.png").convert_alpha()
star_sprite = pygame.image.load("resources/starcatch.png").convert_alpha()

good_sprites = [
    good_objects_sprite.subsurface((0, 0, object_width, object_height)),
    good_objects_sprite.subsurface((object_width, 0, object_width, object_height)),
    good_objects_sprite.subsurface((object_width * 2, 0, object_width, object_height))
]

bad_sprites = [
    bad_objects_sprite.subsurface((0, 0, object_width, object_height)),
    bad_objects_sprite.subsurface((object_width, 0, object_width, object_height)),
    bad_objects_sprite.subsurface((object_width * 2, 0, object_width, object_height))
]

star_sprite_1 = star_sprite.subsurface((0, 0, object_width, object_height))
star_sprite_2 = star_sprite.subsurface((object_width, 0, object_width, object_height))
star_sprite_3 = star_sprite.subsurface((object_width * 2, 0, object_width, object_height))

star_sprites = [star_sprite_1, star_sprite_2, star_sprite_3, star_sprite_2]

s_current_frame_index = 0
s_last_animation_time = 0
s_animation_interval = 150

# score thresholds and corresponding bad object probabilities
bad_prob_schedule = [
    (0, 0.3),    # from score 0 → 30% bad
    (20, 0.4),   # from 20 → 40% bad
    (50, 0.5),   # from 30 → 50% bad
    (80, 0.55),  # from 35 → 55% bad
    (110, 0.6),   # from 40 → 60% bad
    (130, 0.65),  # from 41 → 65% bad
    (160, 0.7),   # from 45 → 70% bad
]

def get_bad_probability(score):
    current_prob = 0.3  # default
    for threshold, prob in bad_prob_schedule:
        if score >= threshold:
            current_prob = prob
        else:
            break
    return current_prob

# health
health_width, health_height = 75, 75
health_sprite = pygame.image.load("resources/starhealth.png").convert_alpha()
health_sprite_resized = pygame.transform.scale(health_sprite, (50, 50))

# clock
clock = pygame.time.Clock()

# show start screen
show_start_screen(screen, WIDTH, HEIGHT, high_score)

# game reset
def reset_game():
    global player_health, falling_objects, spawn_timer, player_x, player_y, score
    player_health = MAX_HEALTH
    falling_objects.clear()
    score = 0
    player_x, player_y = PLAYER_X, PLAYER_Y

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
        player_state = "walking_left"
    elif keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
        player_state = "walking_right"
    else:
        player_state = "standing"
    
    # update player animation
    p_current_time = pygame.time.get_ticks()
    if p_current_time - p_last_animation_time > p_animation_interval:
        p_last_animation_time = p_current_time
        p_current_frame_index = (p_current_frame_index + 1) % len(walking_left_frames)

    # fill the screen with black
    screen.fill((0, 0, 0))
    
    # draw the background
    frame_switch_interval = random.randint(200, 800) # milliseconds
    
    current_bg_frame_time = pygame.time.get_ticks()
    if current_bg_frame_time - last_switch_time > frame_switch_interval:
        last_switch_time = current_bg_frame_time
        current_bg_frame = bg_2_scaled if current_bg_frame == bg_1_scaled else bg_1_scaled
        
    screen.blit(current_bg_frame, (0, 0))
    
    # draw player shadow
    shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surface, shadow_colour, (0, 0, shadow_width, shadow_height))
    shadow_x = player_x + 35
    shadow_y = player_y + player_height + 5
    
    screen.blit(shadow_surface, (shadow_x, shadow_y))
    
    # draw player based on state
    if player_state == "standing":
        p_current_frame = standing_frames[p_current_frame_index % len(standing_frames)]
    elif player_state == "walking_left":
        p_current_frame = walking_left_frames[p_current_frame_index]
    elif player_state == "walking_right":
        p_current_frame = walking_right_frames[p_current_frame_index]
    
    screen.blit(p_current_frame, (player_x, player_y))
    
    current_hit_time = pygame.time.get_ticks()
    player_sprite_to_draw = p_current_frame
    if current_hit_time - last_hit_time < HIT_FLASH_DURATION:
        tinted_sprite = player_sprite_to_draw.copy()
        tinted_sprite.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        player_sprite_to_draw = tinted_sprite
        
    screen.blit(player_sprite_to_draw, (player_x, player_y))
    
    current_heal_time = pygame.time.get_ticks()
    player_sprite_to_draw = p_current_frame
    if current_heal_time - last_healed_time < HEALED_FLASH_DURATION:
        tinted_sprite = player_sprite_to_draw.copy()
        tinted_sprite.fill((38, 215, 35, 100), special_flags=pygame.BLEND_RGBA_MULT)
        player_sprite_to_draw = tinted_sprite
        
    screen.blit(player_sprite_to_draw, (player_x, player_y))

    # update star animation
    current_star_frame_time = pygame.time.get_ticks()
    if current_star_frame_time - s_last_animation_time > s_animation_interval:
        s_last_animation_time = current_star_frame_time
        s_current_frame_index = (s_current_frame_index + 1) % len(star_sprites)

    # spawn falling objects
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_timer = 0
        bad_weight = get_bad_probability(score)
        good_weight = 1 - bad_weight - 0.1  # keep star at 10%
        object_x = random.randint(0, WIDTH - object_width) # x value for where object should start; random
        object_type = random.choices(["bad", "good", "star"],
                                    weights = [bad_weight, good_weight, 0.1],
                                    k=1)[0]
        
        if object_type == "bad":
            object_sprite = random.choice(bad_sprites)
        elif object_type == "good":
            object_sprite = random.choice(good_sprites)
        elif object_type == "star":
            object_sprite = star_sprites[s_current_frame_index]
        
        falling_objects.append({
                                "rect": pygame.Rect(object_x, 0, object_width, object_height),
                                "type": object_type,
                                "sprite": object_sprite})
        # 0 is y value, so top of screen
        # object_width and object_height are the size of the object
        # append adds a new object to falling_objects list

    # update falling objects
    print(f"Object speed: {object_speed:.2f}")
    remaining_objects = []
    for object in falling_objects[:]:
        object["rect"].y += object_speed
        
        if object["type"] == "star":
            object["sprite"] = star_sprites[s_current_frame_index]
        
        screen.blit(object["sprite"], object["rect"])

        # check for collisions
        hitbox_offset_x, hitbox_offset_y = 40, 50
        hitbox_width = 40
        hitbox_height = 20

        player_rect = pygame.Rect(
            player_x + hitbox_offset_x,
            player_y + hitbox_offset_y,
            hitbox_width,
            hitbox_height
        )
        
        # pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)  # draw player hitbox for debugging

        if player_rect.colliderect(object["rect"]):
            if object["type"] == "good":
                print("Caught a good object!")
                food_sound.play()
                score += 1
                object_speed = min(object_speed + math.sqrt(score) * speed_increment, max_speed)
            elif object["type"] == "bad":
                print("Caught a bad object!")
                hurt_sound.play()
                player_health -= 1
                last_hit_time = pygame.time.get_ticks()
                if player_health <= 0:
                    print("Game Over!")
                    gameover_sound.play()
                    new_high = score > high_score
                    if new_high:
                        high_score = save_high_score(score, high_score)
                    show_game_over_screen(screen, WIDTH, HEIGHT, score, high_score, new_high)
                    high_score = save_high_score(score, high_score)
                    reset_game()
            elif object["type"] == "star":
                star_sound.play()
                print("Caught a star!")
                player_health = min(player_health + 1, MAX_HEALTH)
                last_healed_time = pygame.time.get_ticks()
                score += 5
        elif object["rect"].y > HEIGHT:
            pass
        else:
            remaining_objects.append(object)
    
    falling_objects = remaining_objects
    
    # draw health
    for i in range(player_health):
        screen.blit(health_sprite_resized, (10 + i * 55, 10))
        
    # render score
    score_text = score_font.render(f"{score}", False, (255, 255, 255))
    score_x, score_y = WIDTH - score_text.get_width()- 10, 10
    screen.blit(score_text, (score_x, score_y))

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)

# quit Pygame
pygame.quit()
sys.exit()
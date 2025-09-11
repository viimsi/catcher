import pygame
import sys

# init Pygame
pygame.init()

# set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fleater")

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with black
    screen.fill((0, 0, 0))

    # update the display
    pygame.display.flip()
    
# quit Pygame
pygame.quit()
sys.exit()
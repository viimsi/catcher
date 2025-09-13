import pygame
import sys

def show_start_screen(screen, width, height):
    font = pygame.font.Font(None, 74)
    text = font.render("Press any key to start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
            
def show_game_over_screen(screen, width, height):
    font = pygame.font.Font(None, 30)
    text = font.render("Game Over! Press Q to Quit or any key to restart", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                else:
                    return
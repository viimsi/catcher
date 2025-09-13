import pygame
import sys

FONT = "resources/DigitalDisco.ttf"

def show_start_screen(screen, width, height, high_score):
    font = pygame.font.Font(FONT, 35)
    text = font.render("Press any key to start", False, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    
    highscore_font = pygame.font.Font(FONT, 25)
    highscore_text = highscore_font.render(f"High Score: {high_score}", False, (255, 255, 0))
    highscore_rect = highscore_text.get_rect(center=(width // 2, height // 2 + 50))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        screen.blit(highscore_text, highscore_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
            
def show_game_over_screen(screen, width, height, score, high_score, new_high=False):
    font = pygame.font.Font(FONT, 30)
    text = font.render("Game Over! Press Q to Quit or R to restart", False, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    
    score_font = pygame.font.Font(FONT, 25)
    score_text = score_font.render(f"Score: {score}", False, (255, 255, 255))
    score_rect = score_text.get_rect(center=(width // 2, height // 2 + 50))

    high_text = score_font.render(f"High Score: {high_score}", False, (255, 255, 0))
    high_rect = high_text.get_rect(center=(width // 2, height // 2 + 90))

    if new_high:
        new_high_text = score_font.render("NEW HIGH SCORE!", False, (0, 255, 0))
        new_high_rect = new_high_text.get_rect(center=(width // 2, height // 2 + 130))
    else:
        new_high_text, new_high_rect = None, None
    
    while True:
        screen.fill((0, 0, 0, 100))
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(high_text, high_rect)
        if new_high_text:
            screen.blit(new_high_text, new_high_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
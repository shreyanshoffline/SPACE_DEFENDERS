
import pygame
import sys
import random
from utils import settings # for WIN_WIDTH and WIN_HEIGHT

def start_screen(screen, defender_img, bg_img):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 60)
    running = True

    # Button setup
    button_rect = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() - 150, 200, 70)

    while running:
        # Draw background
        screen.blit(bg_img, (0, 0))

        # Title
        title = font.render(" SPACE DEFENDERS ", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Place the sprites at preset positions
        defendermod_img = pygame.transform.scale(defender_img, (100, 100))
        screen.blit(defendermod_img, (480, 420))    
        # PLAY Button
        pygame.draw.rect(screen, (50, 150, 255), button_rect, border_radius=20)
        btn_text = font.render("PLAY", True, (0, 0, 0))
        screen.blit(btn_text, (button_rect.centerx - btn_text.get_width() // 2, button_rect.centery - btn_text.get_height() // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Start the game

        pygame.display.update()
        clock.tick(60)

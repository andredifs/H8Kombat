import pygame
import sys

pygame.init()

# Importing constants
from constants import colors, window

# Include classes
from include.button import menu_button

# Window setup
WIN = pygame.display.set_mode((window.WIDTH, window.HEIGHT))
pygame.display.set_caption(window.TITLE)

# Set the game clock
FPS = 60

BG = pygame.image.load("assets/ita.png")

def draw_window():
    WIN.fill(colors.CYAN)
    pygame.display.update()


def get_font(size: int):
    return pygame.font.Font("assets/font.ttf", size)

def menu():
    while True:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(window.WIDTH/2, window.HEIGHT/4))

        PLAY_BUTTON = menu_button(text_input="PLAY", pos=(window.WIDTH/2, window.HEIGHT/2))
        OPTIONS_BUTTON = menu_button(text_input="OPTIONS", pos=(window.WIDTH/2, window.HEIGHT/2 + 80))
        QUIT_BUTTON = menu_button(text_input="QUIT", pos=(window.WIDTH/2, window.HEIGHT/2 + 160))

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Play game")
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Open options")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False        
        
        draw_window()

        menu()


    pygame.quit()

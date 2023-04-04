import pygame
import sys

# Importing constants
from constants import window

# Include classes
from include.button import menu_button
from include.fighter import Fighter

pygame.init()

# Window setup
WIN_MENU = pygame.display.set_mode((window.WIDTH, window.HEIGHT))
pygame.display.set_caption(window.TITLE)

# Window for choice chars

WIN_CHOICE = pygame.display.set_mode((window.WIDTH, window.HEIGHT))

# Window for game

WIN_GAME = pygame.display.set_mode((window.WIDTH, window.HEIGHT))

# Create a two fighters for game

fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# Set the game clock
FPS = 60

BG_MENU = pygame.image.load("assets/ita.png")
# BG_CHAR = pygame.image.load("assets/ita.png")
# BG_GAME = pygame.image.load("assets/ita.png")

def get_font(size: int):
    return pygame.font.Font("assets/font.ttf", size)


def menu():
    while True:
        WIN_MENU.blit(BG_MENU, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(window.WIDTH / 2, window.HEIGHT / 4))

        # Botões
        PLAY_BUTTON = menu_button(text_input="PLAY", pos=(window.WIDTH / 2, window.HEIGHT / 2))
        OPTIONS_BUTTON = menu_button(text_input="OPTIONS", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 80))
        QUIT_BUTTON = menu_button(text_input="QUIT", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 160))

        WIN_MENU.blit(MENU_TEXT, MENU_RECT)

        # Muda a cor do botão quando o mouse está em cima
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN_MENU)

        # Verifica se o botão foi clicado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game()
                    print("Play game")
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Open options")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Create a window for choice of chars

def choice():
    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WIN_CHOICE.blit(BG_MENU, (0, 0))

        pygame.display.update()

# Create a window for game

def game():
    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WIN_GAME.blit(BG_MENU, (0, 0))
        # move
        fighter_1.move(window.WIDTH, window.HEIGHT)
        # fighter_2.move()

        # draw fighters
        fighter_1.draw(WIN_GAME)
        fighter_2.draw(WIN_GAME)

        pygame.display.update()

# Main function
def main(dev=False):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if dev:
            game()
        else:
            menu()

        pygame.display.update()

    pygame.quit()

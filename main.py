import pygame
import sys

# Importing constants
from constants import window
from constants import colors
from constants import controls

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

# Set the game clock
FPS = 60

PICTURE_MENU = pygame.image.load("assets/ita.png")
BG_MENU = pygame.transform.scale(PICTURE_MENU, (window.WIDTH, window.HEIGHT))
PICTURE_GAME = pygame.image.load("assets/tatame.jpg")
BG_GAME = pygame.transform.scale(PICTURE_GAME, (window.WIDTH, window.HEIGHT))
# BG_CHAR = pygame.image.load("assets/ita.png")

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

        WIN_CHOICE.blit(BG_GAME, (0, 0))

        pygame.display.update()

# Create a window for game
def game():
    # Create a two fighters for game
    fighter_1 = Fighter(200, 310, WIN_GAME, colors.BLUE)
    fighter_2 = Fighter(700, 310, WIN_GAME, colors.ORANGE)

    # Defining oponent
    fighter_1.set_target(fighter_2)
    fighter_2.set_target(fighter_1)

    # Defining controls
    fighter_1.set_controls(controls.PLAYER1)
    fighter_2.set_controls(controls.PLAYER2)

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WIN_GAME.blit(BG_GAME, (0, 0))

        # Player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)

        # Move
        fighter_1.move(window.WIDTH, window.HEIGHT)
        fighter_2.move(window.WIDTH, window.HEIGHT)

        # Draw fighters
        fighter_1.draw()
        fighter_2.draw()

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

# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(WIN_GAME, colors.BLACK, (x - 2, y - 2, 204, 34))
    pygame.draw.rect(WIN_GAME, colors.GREY, (x, y, 200, 30))

    if health > 40:
        pygame.draw.rect(WIN_GAME, colors.GREEN, (x, y, 200 * ratio, 30))
    elif health > 20:
        pygame.draw.rect(WIN_GAME, colors.YELLOW, (x, y, 200 * ratio, 30))
    else:
        pygame.draw.rect(WIN_GAME, colors.RED, (x, y, 200 * ratio, 30))

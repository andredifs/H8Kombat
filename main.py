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

# Window for victory
WIN_VICTORY = pygame.display.set_mode((window.WIDTH, window.HEIGHT))

# Set the game clock
FPS = 60

# Backgrounds
PICTURE_MENU = pygame.image.load("assets/menu.png")
BG_MENU = pygame.transform.scale(PICTURE_MENU, (window.WIDTH, window.HEIGHT))

PICTURE_GAME = pygame.image.load("assets/tatame.jpg")
BG_GAME = pygame.transform.scale(PICTURE_GAME, (window.WIDTH, window.HEIGHT))

PICTURE_VICTORY = pygame.image.load("assets/fatality.jpg")
BG_VICTORY = pygame.transform.scale(PICTURE_VICTORY, (window.WIDTH, window.HEIGHT))

run = True

def menu(dev=False):
    global run

    while run:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                quit()

        WIN_MENU.blit(BG_MENU, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("H8 Kombat", True, colors.WHITE)
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
                quit()

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
    global run

    while run:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                quit()

        WIN_CHOICE.blit(BG_GAME, (0, 0))

        pygame.display.update()

# Create a window for game
def game(dev=False):
    global run

    round_over = False
    intro_count = 3
    ROUND_OVER_COOLDOWN = 500

    # Create a two fighters for game
    fighter_1 = Fighter(100, 310, WIN_GAME, colors.BLUE)
    fighter_2 = Fighter(800 - 180, 310, WIN_GAME, colors.ORANGE)

    # Defining oponent
    fighter_1.set_target(fighter_2)
    fighter_2.set_target(fighter_1)

    # Defining controls
    fighter_1.set_controls(controls.PLAYER1)
    fighter_2.set_controls(controls.PLAYER2)

    while run:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                quit()

        TEXT_SURFACE = WIN_GAME.subsurface(pygame.Rect(0, 0, window.WIDTH, window.HEIGHT))
        TEXT_SURFACE.fill(colors.BLACK)
        WIN_GAME.blit(BG_GAME, (0, 0))

        # Draw fighters
        fighter_1.draw()
        fighter_2.draw()

        # Player stats
        health_bar(fighter_1.health, 20, 20)
        health_bar(fighter_2.health, 580, 20)
        draw_text(TEXT_SURFACE, f'P1: {fighter_1.score}', 30, colors.RED, 55, 70)
        draw_text(TEXT_SURFACE, f'P2: {fighter_2.score}', 30, colors.RED, window.WIDTH - 55, 70)

        # update countdown
        if intro_count >= 0:
            text = str(intro_count) if intro_count > 0 else "FIGHT!"

            draw_text(TEXT_SURFACE, text, 100, colors.RED, window.WIDTH / 2, window.HEIGHT / 2)

            pygame.time.delay(1100)
            intro_count -= 1

        elif round_over is False:
            fighter_1.move(window.WIDTH, window.HEIGHT)
            fighter_2.move(window.WIDTH, window.HEIGHT)

        # check for player defeat
        if round_over is False:
            if fighter_1.dead or fighter_2.dead:
                alive = fighter_1 if not fighter_1.dead else fighter_2
                alive.score += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()

                reset_fighters([fighter_1, fighter_2])

        elif pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            reset_fighters([fighter_1, fighter_2])

        # display victory image
        if (fighter_1.score == 2) or (fighter_2.score == 2):
            WIN_VICTORY.blit(BG_VICTORY, (0, 0))

        pygame.display.update()

# Main function
def main(dev=False):
    global run
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if dev:
            game(dev)
        else:
            menu(dev)

        pygame.display.update()

    quit()

# function for drawing fighter health bars
def health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(WIN_GAME, colors.BLACK, (x - 2, y - 2, 204, 34))
    pygame.draw.rect(WIN_GAME, colors.GREY, (x, y, 200, 30))

    if health > 40:
        color = colors.GREEN
    elif health > 20:
        color = colors.YELLOW
    else:
        color = colors.RED

    pygame.draw.rect(WIN_GAME, color, (x, y, 200 * ratio, 30))

def draw_text(surface: pygame.Surface, text, size, text_col, x, y):
    img = get_font(size).render(text, True, text_col)
    img_rect = img.get_rect(center=(x, y))
    return surface.blit(img, img_rect)

def get_font(size: int):
    return pygame.font.Font("assets/font.ttf", size)

def reset_fighters(fighter: list[Fighter]):
    for fighter in fighter:
        fighter.reset()

def quit():
    global run
    run = False
    pygame.quit()
    sys.exit()
